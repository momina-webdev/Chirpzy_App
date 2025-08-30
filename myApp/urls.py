from django.contrib import admin
from django.urls import path
from myApp import views
from .views import profile_view

urlpatterns = [
    path('', views.index , name='index'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
   path('profile/', views.profile_view, name='profile'),
   path('follow/<str:username>/', views.follow_view, name='follow'),
   path('toggle-follow/<str:username>/', views.toggle_follow, name='toggle_follow'),  
   path('edit-profile/', views.edit_profile, name='edit_profile'),  # ✅ THIS must exist
   path('create-post/', views.create_post, name='create_post'),  # ✅
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
  # urls.py
  path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),

  

]