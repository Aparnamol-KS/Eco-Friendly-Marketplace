from django.contrib import admin
from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.get_home_page,name='get_home_page'),
]