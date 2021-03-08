
from django.contrib import  admin 
from django.urls import path, include
from . import views

# Creating the urls patterns for the Blog App
urlpatterns = [
    path('', views.bloghome, name='home'),
    path('postcomment/',views.PostComment,name='PostComment'),
    path('<str:slug>', views.blogpost, name='slug'),
]
