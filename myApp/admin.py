
from django.contrib import admin
from .models import UserProfile, Post, Like, Follow, View
from .models import  Comment

# --- Comment Admin ---


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__caption', 'content')

# --- UserProfile Admin ---
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_image', 'followers_count', 'following_count')
    search_fields = ('user__username',)

# --- Post Admin ---
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'created_at', 'views')
    list_filter = ('created_at',)
    search_fields = ('caption', 'user__username')

# --- Like Admin ---
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user')
    search_fields = ('user__username', 'post__caption')



# --- Follow Admin ---
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'following__username')

# --- View Admin ---
@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('post', 'user')
    search_fields = ('user__username', 'post__caption')
