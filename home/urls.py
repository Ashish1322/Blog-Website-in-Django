# Importing some libraries
from django.contrib import  admin
from django.urls import path, include
from . import views

# Creating and handling all the urls in the home app
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search_result, name='search'),
    path('signup/', views.handleSignUp, name='search'),
    path('login/', views.handleLogin, name='search'),
    path('logout/', views.handleLogout, name='search'),
]
