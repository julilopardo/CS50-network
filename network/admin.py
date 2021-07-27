from network.models import Following, Like, Post, User
from django.contrib import admin

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Following)
