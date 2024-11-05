from django.contrib.auth.models import User  
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Product(models.Model):
    product_id = models.CharField(max_length=10, unique=True, primary_key=True)
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    eco_friendly_certifications = models.CharField(max_length=255)  
    material = models.CharField(null=True,max_length=255)  
    product_image = models.ImageField(upload_to='images/',null=True) 

    def __str__(self):
        return self.product_name

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)  
    buyer = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='cart_buyer')  
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE, related_name='cart_products')  
    quantity = models.PositiveIntegerField(default=1) 

    def __str__(self):
        return f"Cart {self.cart_id} - {self.buyer.username}"  


class Wishlist(models.Model):
    wishlist_id = models.AutoField(primary_key=True)  
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='wishlists')  
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE, related_name='wishlist_products')  

    def __str__(self):
        return f"Wishlist {self.wishlist_id} - {self.user.username}" 


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    order_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    status = models.CharField(max_length=10, choices=ORDER_STATUS_CHOICES, default='Pending')
    cart_items = models.ManyToManyField(Cart) 

    def __str__(self):
        return f"Order {self.order_id} by {self.buyer.username}" 
    
class orderedItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product_name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    product_id = models.CharField(max_length=10)
    product_image = models.ImageField(upload_to='images/',null=True)


class Eco_certifications(models.Model):
    certification_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE, related_name='certifications')  
    certification_name = models.CharField(max_length=255)

    def __str__(self):
        return self.certification_name




from django.db import models

class UserDetails(models.Model):
    user_id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(
        max_length=10, 
        choices=(('Buyer', 'Buyer'), ('Admin', 'Admin'))
    )

    def __str__(self):
        return f"{self.name} ({self.email})"

from django.db import models

class Product(models.Model):
    product_id = models.CharField(max_length=10, unique=True, primary_key=True)
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()
    category = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    eco_friendly_certifications = models.CharField(max_length=255)  
    product_image_url = models.URLField(max_length=500)  

    def __str__(self):
        return self.product_name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    buyer_id = models.ForeignKey(UserDetails,null=False,on_delete=models.CASCADE,related_name='order_buyer')
    product_id = models.ForeignKey(Product,null=False,on_delete=models.CASCADE,related_name='order_products')
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.product_id.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id} by {self.buyer_id.name}"
    
class Eco_certifications(models.Model):
    certification_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, null=False, on_delete=models.CASCADE, related_name='certifications')  
    certification_name = models.CharField(max_length=255)

    def __str__(self):
        return self.certification_name

class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)  
    buyer_id = models.ForeignKey(UserDetails, null=False, on_delete=models.CASCADE, related_name='cart_buyer')
    product_id = models.ForeignKey(Product, null=False, on_delete=models.CASCADE, related_name='cart_products')  
    quantity = models.PositiveIntegerField() 

    def __str__(self):
        return f"Cart {self.cart_id} - {self.buyer.name}"

class Wishlist(models.Model):
    wishlist_id = models.AutoField(primary_key=True)  
    user_id = models.ForeignKey(UserDetails, null=False, on_delete=models.CASCADE, related_name='wishlists')  
    product_id = models.ForeignKey(Product, null=False, on_delete=models.CASCADE, related_name='wishlist_products')  

    def __str__(self):
        return f"Wishlist {self.wishlist_id} - {self.user.name}"