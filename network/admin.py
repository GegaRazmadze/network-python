from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import User, Post, Like, Follow

class PostAdmin(admin.ModelAdmin):
    list_display = ('post', 'user_id', 'username' , 'body', 'date')
    search_fields = ('user_id', 'username')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'post_id')

class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower_id', 'following_id')


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follow, FollowAdmin)