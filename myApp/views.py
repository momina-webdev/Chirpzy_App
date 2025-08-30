from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from django.contrib.auth.models import User
from .models import UserProfile, Post, Follow, Like, View, Comment


# -----------------------------
# AUTHENTICATION VIEWS
# -----------------------------

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    auth_logout(request)
    return redirect('login')


# -----------------------------
# PROFILE VIEWS
# -----------------------------

@login_required
def profile_view(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    posts = Post.objects.filter(user=user)

    follower_ids = Follow.objects.filter(following=user).values_list('follower_id', flat=True)
    follower_users = User.objects.filter(id__in=follower_ids)

    context = {
        'profile': profile,
        'posts': posts,
        'post_count': posts.count(),
        'followers': follower_users.count(),
        'following': Follow.objects.filter(follower=user).count(),
        'profile_user': user,
        'follower_users': follower_users,
    }
    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        bio = request.POST.get('bio')
        image = request.FILES.get('profile_image')

        if bio:
            profile.bio = bio
        if image:
            profile.profile_image = image
        profile.save()

    return redirect('profile')


# -----------------------------
# POST VIEWS
# -----------------------------

@login_required
def create_post(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        caption = request.POST.get("caption")

        if image:
            Post.objects.create(user=request.user, image=image, caption=caption)
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "error", "message": "No image"})

    return JsonResponse({"status": "error", "message": "Invalid request"})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user == request.user:  # ✅ only owner can delete
        post.delete()
        return redirect('index')
    return redirect('profile')


# -----------------------------
# HOME / DASHBOARD VIEW
# -----------------------------

@login_required
def index(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        action = request.POST.get('action')
        post = get_object_or_404(Post, id=post_id)

        if action == 'like':
            Like.objects.get_or_create(user=request.user, post=post)
        elif action == 'view':
            View.objects.get_or_create(user=request.user, post=post)

    posts = Post.objects.select_related('user', 'user__userprofile').all().order_by('-created_at')

    followed_user_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)

    active_users = User.objects.filter(
        userprofile__isnull=False
    ).exclude(
        id__in=followed_user_ids
    ).exclude(
        id=request.user.id
    )

    return render(request, 'index.html', {
        'posts': posts,
        'active_users': active_users,
    })


# -----------------------------
# COMMENT VIEW
# -----------------------------

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)

    return redirect('index')


# -----------------------------
# FOLLOW / UNFOLLOW VIEWS
# -----------------------------

@login_required
def toggle_follow(request, username):
    target_user = get_object_or_404(User, username=username)

    if request.user == target_user:
        return redirect('profile')  # ✅ self-follow not allowed

    existing_relation = Follow.objects.filter(follower=request.user, following=target_user)

    if existing_relation.exists():
        existing_relation.delete()  # unfollow
    else:
        Follow.objects.create(follower=request.user, following=target_user)  # follow

    return redirect('follow', username=username)


@login_required
def follow_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=profile_user)
    posts = Post.objects.filter(user=profile_user)

    is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    followed_users_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    suggested_users = User.objects.exclude(id__in=followed_users_ids).exclude(id=request.user.id)

    context = {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'post_count': posts.count(),
        'followers': profile.followers_count(),
        'following': profile.following_count(),
        'is_following': is_following,
        'suggested_users': suggested_users,
    }
    return render(request, 'follow.html', context)
