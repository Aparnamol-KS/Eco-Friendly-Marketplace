from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.get_home_page,name='home'),
    path('login',views.login_user,name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register',views.register_user,name='register'),
    path('product_list/<str:category>/',views.product_listing,name='product_list'),
    path('product_detail/<str:product_id>/',views.product_detail,name='product_detail'),
    path('cart', views.cart_view, name='cart'),
    path('wishlist', views.wishlist_view, name='wishlist'),
    path('checkout', views.checkout, name='checkout'),
    path('cart/order_summary/', views.order_summary, name='order_summary'),
    path('delete_order/<int:order_id>/',views.delete_order,name='delete_order'),
    path('profile', views.profile_view, name='profile'),
    path('add_to_cart/<str:product_id>/',views.add_to_cart,name='add_to_cart'),
    path('cart/delete_cart_item/<str:product_id>/',views.delete_cart_item,name='delete_cart_item'),
    path('add_to_wishlist/<str:product_id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('wishlist/delete_wishlist_item/<str:product_id>/',views.delete_wishlist_item,name='delete_wishlist_item'),
    path('admin_interface/', admin.site.urls)
    

   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)