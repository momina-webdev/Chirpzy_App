
from django.db import models
from django.contrib.auth.models import User

# ---- User Profile ----
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', default='default.png')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def followers_count(self):
        return Follow.objects.filter(following=self.user).count()

    def following_count(self):
        return Follow.objects.filter(follower=self.user).count()

# ---- Follow Relationship ----
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following_set', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers_set', on_delete=models.CASCADE)
   
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

# ---- Post ----
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    caption = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)

    def total_likes(self):
        return self.likes.count()
    def total_views(self):
        return self.likes.count()

# ---- Like ----
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

# ---- View ----
class View(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='view_records', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}"
