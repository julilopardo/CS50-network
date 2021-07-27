
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.new_post, name="newpost"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    # API routes
    path("like/<str:post_id>", views.like, name="like"),
    path("follow/<str:user_id>", views.follow, name="follow"),
    path("edit/<str:post_id>", views.edit, name="edit")
]
