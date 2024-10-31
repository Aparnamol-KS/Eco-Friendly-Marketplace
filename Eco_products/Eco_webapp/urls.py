from django.contrib import admin
from django.urls import path,include
from .import views
urlpatterns = [
    path('',views.get_home_page,name='home'),
    path('login',views.login_user,name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register',views.register_user,name='register'),
    path('product_list',views.product_listing,name='product_list'),
    path('product_detail',views.product_detail,name='product_detail'),
    path('cart', views.cart_view, name='cart'),
    path('wishlist', views.wishlist_view, name='wishlist'),
    path('profile', views.profile_view, name='profile')
   
]