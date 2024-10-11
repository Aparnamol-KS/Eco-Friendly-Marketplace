from django.contrib import admin
from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.login_user,name='login'),
    path('register',views.register_user,name='register'),
    path('home',views.get_home_page,name='home')
]