from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

import json
from django.http import JsonResponse
from django.db.models import Count


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.core.paginator import Paginator

from .models import User, Post, Follow, Like

from .forms import PostForm, FollowForm


def index(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        return  HttpResponseRedirect(reverse('profile_page',  args=(user_id,)))
    else:
        return render(request, "network/index.html", {
            "message": "You Must Log In !"
        })


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

@login_required
def all_posts(request):
    current_user_id = request.user.id
    # Save Post
    # Create Post Form
    post_form = PostForm(initial={"user_id":request.user.id, "username": request.user.username})
    
    posts = Post.objects.all().order_by('date').reverse()

    paginator  = Paginator(posts ,10)
    
    # paginator
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'post_form': post_form,
        
        'current_user_id':request.user.id,
        'page_obj': page_obj,
    }

    return render(request, "network/all_posts.html", context)

@login_required
def add_post(request):
    if request.method == "POST":
        post = PostForm(request.POST or None)
    #Save Post
        if post.is_valid() and post is not None:
            post.save()
            return HttpResponseRedirect(reverse('all_posts'))
        else:
            posts = Post.objects.all().order_by('date').reverse()
            return render(request, "network/all_posts.html", {
                "message": "Post is not Valid.",
                'posts': posts
            })


    else:
        return  HttpResponseRedirect(reverse('all_posts'))

# form permissen || 403 forbiden
@csrf_exempt
@login_required
def edit_post(request, post_id):
    current_user_id = request.user.id
    # Query for requested post
    try:
        post = Post.objects.get(user_id=current_user_id, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)
    
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("body") is not None:
            post.body = data["body"]
       
        post.save()
        return HttpResponse(status=204)
    
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@login_required
def profile_page(request, user_id):
    # for following button check
    current_user_id = request.user.id

    pro_user_id = user_id
    pro_followers = len(Follow.objects.filter(following_id= pro_user_id))
    pro_following = len(Follow.objects.filter(follower_id = pro_user_id))

    
    
    if Follow.objects.filter(following_id = user_id, follower_id = current_user_id).exists():
        isFollowing = True
    # Checking if current if folowing user_profile
    elif current_user_id == user_id:
        isFollowing = ''
    else:
        isFollowing = False
        
    # Follow submit Form 
    following_posts = Post.objects.filter(user_id=user_id)
    follow_form  = FollowForm(initial={"follower_id":current_user_id, "following_id":user_id, "following_posts":following_posts})
    
    posts = Post.objects.filter(user_id = user_id).order_by('date').reverse()


    return render(request, "network/profile_page.html", {
        "posts": posts,
        "pro_followers":pro_followers,
        "pro_following":pro_following,
        "pro_user_id":pro_user_id,

        "current_user_id":current_user_id,
        
        "isFollowing":isFollowing,
        "follow_form":follow_form,
    })


@login_required   
def add_follower(request,pro_user_id):
    if request.method == "POST":
        user_id = pro_user_id
        follow_form = FollowForm(request.POST or None)
    #Save Follow info
        if follow_form.is_valid() and follow_form is not None:
            follow_form.save()

            return HttpResponseRedirect(reverse('profile_page',  args=(user_id,)))

    else:
        user_id = pro_user_id
        return  HttpResponseRedirect(reverse('profile_page',  args=(user_id,)))

@login_required
def remove_follower(request,pro_user_id):
    if request.method == "POST":
        user_id = pro_user_id
        
        follow_form = FollowForm(request.POST or None)
        follower_id = follow_form["follower_id"].value()
    #Save Follow info

        Follow.objects.filter(following_id = user_id, follower_id = follower_id).delete()

        return HttpResponseRedirect(reverse('profile_page',  args=(user_id,)))

    else:
        user_id = pro_user_id
        return  HttpResponseRedirect(reverse('profile_page',  args=(user_id,)))


@login_required
def following_page(request):
    current_user_id = request.user.id
    # user Follows:
    following_ids = Follow.objects.filter(follower_id = current_user_id).values('following_id')

    # # all user_following Posts Many To Many
    post_array = []
    for following_id in following_ids:
        posts = list(Post.objects.filter(user_id = following_id['following_id']).order_by('date').reverse())
        post_array += posts
    # sort array
    post_array.sort(key=lambda e: e.date, reverse=True)

    paginator  = Paginator(post_array ,10)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)




    return render(request, "network/following_page.html", {
        'current_user_id':current_user_id,
        'page_obj': page_obj,
    })



# form permissen || 403 forbiden
@csrf_exempt
@login_required
def like_post(request):
    user = request.user.id
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(post=post_id)

        if any(d.get('id') == user for d in post_obj.likes_list):
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)
    # Boolean True of False
    # need assin befor use
        user_id = get_object_or_404(User, pk=user)
        post =  get_object_or_404(Post,  post=post_id)

        like, created = Like.objects.get_or_create(user_id=user_id, post_id=post)
    
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        
        like.save()

        data = {
            'value': like.value,
            'likes': post_obj.liked.all().count()
        }

        return JsonResponse(data, safe=False)
    
    return HttpResponseRedirect(reverse('add_post'))