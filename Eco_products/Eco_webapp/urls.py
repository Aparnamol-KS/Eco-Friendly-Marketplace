from django.contrib import admin
from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.get_home_page,name='home'),
    path('login',views.login_user,name='login'),
    path('register',views.register_user,name='register'),
    path('product_list',views.product_listing,name='product_list'),
    path('product_detail',views.product_detail,name='product_detail')
   
]