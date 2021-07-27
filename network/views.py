import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.request import HttpHeaders
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Like, Following


def index(request):
    #Get all posts
    posts= Post.objects.all()

    #Return post in reverse chronological order
    posts= posts.order_by("-timestamp").all()

    if request.user != AnonymousUser():
    #Get posts that the actual user likes for button format
        try:
            liked = Like.objects.filter(user=request.user)
            liked_posts= []
            for post in liked:
                liked_post= post.post
                liked_posts.append(liked_post)

        except Like.DoesNotExist:
            liked_posts=[]
    else:
        liked_posts=[]

    paginator= Paginator(posts, 10)
    page_number= request.GET.get('page')
    page_obj= paginator.get_page(page_number)

    return render(request, "network/index.html", {"page_obj": page_obj, "liked_posts": liked_posts})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def new_post(request):
    if request.method == "POST":
        if request.POST["content"]:
            post = Post.objects.create(user = request.user, content= request.POST["content"])
            post.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            message = "Cannot publish an empty post"
            return render(request, "network/index.html", {"message": message, "posts": Post.objects.order_by("-timestamp").all()})

def profile(request, username):
    profile_name= User.objects.get(username=username)
    name= profile_name.username

    #Get all user's posts
    try:
        user_posts= Post.objects.filter(user=profile_name.id)
        user_posts= user_posts.order_by("-timestamp").all()
    
    except Post.DoesNotExist:
        user_posts= []
    
    #Get number of users the actual user is following
    try:
        following_users= Following.objects.filter(follower=profile_name.id)
        followed= []
        if len(following_users) > 0:
            for follow in following_users:
                followed_user = follow.following
                followed.append(followed_user)

    except Following.DoesNotExist:
        followed= []

    num_of_following= len(followed)

    #Get number of followers the user has
    try:
        followers= Following.objects.filter(following=profile_name.id)
        followby= []
        for follow in followers:
            follower_user = follow.follower
            followby.append(follower_user)

    except Following.DoesNotExist:
        followby= []
    
    if request.user in followby:
        following = "Unfollow"
    else:
        following = "Follow" 

    num_of_followers= len(followby)

    #Get posts that the actual user likes for button format
    if request.user != AnonymousUser():
        try:
            liked = Like.objects.filter(user=request.user)
            liked_posts= []
            for post in liked:
                liked_post= post.post
                liked_posts.append(liked_post)
                
        except Like.DoesNotExist:
            liked_posts=[]
    else:
        liked_posts=[]

    paginator= Paginator(user_posts, 10)
    page_number= request.GET.get('page')
    page_obj= paginator.get_page(page_number)


    return render(request, "network/profile.html", {
        "name":name,
        "username": username,
        "num_of_following": num_of_following,
        "num_of_followers": num_of_followers,
        "page_obj": page_obj,
        "liked_posts": liked_posts,
        "following": following
    })

@login_required
def following(request):
    #Get all followed users
    following = Following.objects.filter(follower= request.user).values('following_id')

    posts= Post.objects.filter(user__in=following).order_by('-timestamp')
    for post in posts:
        post.likes = Like.objects.filter(post=post.id).count()
        post.save()

    if len(following) == 0:
        message= "You are not following anyone yet. Go to your favorite users profiles and start following them so you don't miss a thing!"
    else:
        message= None

    #Get posts that the actual user likes for button format
    try:
        liked = Like.objects.filter(user=request.user)
        liked_posts= []
        for post in liked:
            liked_post= post.post
            liked_posts.append(liked_post)
            
    except Like.DoesNotExist:
        liked_posts=[]

    paginator= Paginator(posts, 10)
    page_number= request.GET.get('page')
    page_obj= paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "len_following": len(following),
        "page_obj": page_obj,
        "message": message,
        "liked_posts": liked_posts
    })


@login_required
@csrf_exempt
def like(request, post_id):
    post= Post.objects.get(id=post_id)

    if request.method == "GET":
        return JsonResponse({"likes": post.likes})

    if request.method == "PUT":
        data = json.loads(request.body)
        print(data.get("like"))
        if data.get("like") is True:
            Like.objects.create(user= request.user, post= post)
            post.likes = Like.objects.filter(post= post).count()
    
        else:
            Like.objects.filter(user= request.user, post= post).delete()
            post.likes = Like.objects.filter(post= post).count()
        
        post.save()
        likes= post.likes
        return JsonResponse({"likes": likes})

@login_required
@csrf_exempt
def follow(request, user_id):

    user = User.objects.get(username = user_id)
    if request.method == "PUT":
        data= json.loads(request.body)
        print(data.get("follow"))
        if data.get("follow") is True:
            Following.objects.create(follower= request.user, following= user)
            followers= Following.objects.filter(following=user).count()
        else:
            Following.objects.filter(follower= request.user, following=user).delete()
            followers= Following.objects.filter(following=user).count()

        return JsonResponse({"followers": followers})

    if request.method == "GET":
        followers= Following.objects.filter(following=user).count()
        return JsonResponse({"followers": followers})

@csrf_exempt
def edit(request, post_id):
    post= Post.objects.get(id= post_id)

    if request.method =="PUT":
        data= json.loads(request.body)
        if data.get("post") is not None:
            post.content = data["post"]
        post.save()
        return HttpResponse(status=204)
