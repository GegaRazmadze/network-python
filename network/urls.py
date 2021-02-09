
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("all_posts/", views.all_posts, name="all_posts"),
    path("add_post/", views.add_post, name="add_post"),

    path("<int:user_id>/profile_page", views.profile_page, name="profile_page"),

    path("<int:pro_user_id>/add_follower", views.add_follower, name="add_follower"),
    path("<int:pro_user_id>/remove_follower", views.remove_follower, name="remove_follower"),

    path("following_page/", views.following_page, name="following_page"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),

    path("like_post/", views.like_post, name="like_post"),
]


