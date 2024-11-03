from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Eco_webapp.models import Product,Cart,Wishlist,Order
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, F

# Create your views here.
def get_home_page(request):
    return render(request,'home.html',context={})

def login_user(request):
    # Check if the request method is POST (indicating that the form has been submitted)
    if(request.method == 'POST'):
        # Extract the username and password from the POST request
        username = request.POST["name"]
        password = request.POST["pwd"]
        
        # Authenticate the user with the provided username and password
        user = authenticate(request, username=username, password=password)
        
        # If authentication is successful (user exists and credentials are correct)
        if user is not None:
            # Log the user in and create a session
            login(request, user)
            # Redirect the user to the home page after a successful login
            return redirect('home')
        else:
            # If authentication fails, display an error message to the user
            messages.success(request,('Sorry Account not found'))
            # Redirect the user back to the login page for another attempt
            return redirect('login')
    else:
        # If the request method is GET, render the login page
        return render(request,'login.html',context={})



def register_user(request):
    if request.method == 'POST':
        name = request.POST['name1']
        email = request.POST['email']
        password = request.POST['password']
        
        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
            return redirect('register')
        
        # Create a new user and set the password securely
        user = User.objects.create_user(
            username=name,
            email=email,
            password=password  
        )
        
        # Save the user
        user.save()
        
        # Success message and redirect to login
        messages.success(request, 'User registered successfully!')
        return redirect('login')
    
    return render(request, 'register.html')


    
def product_listing(request,category):
    products = Product.objects.filter(product_id__startswith = category)
    if category == "SF":
        category_heading = "Sustainable Fashion"
    elif category == "ZW":
        category_heading = "Zero Waste Products"
    elif category == "SH":
        category_heading = "Sustainable Home Essentials"
    elif category == 'PC':
        category_heading = 'Personal Care'
    else:
        category_heading = "Product Details"
    return render(request, 'product_listing.html', {'products': products, 'heading': category_heading})

def product_detail(request,product_id):
    product = get_object_or_404(Product, product_id=product_id)

    if product.product_id.startswith("SF"):
        category_heading = "Sustainable Fashion"
    elif product.product_id.startswith("ZW"):
        category_heading = "Zero Waste Products"
    elif product.product_id.startswith("SH"):
        category_heading = "Sustainable Home Essentials"
    elif product.product_id.startswith('PC'):
        category_heading = 'Personal Care'
    else:
        category_heading = "Product Details"
    return render(request,'single_product_view.html',{'product':product, 'heading':category_heading})



def logout_user(request):
    logout(request)  
    return redirect('login')  

def cart_view(request):
    cart_items = Cart.objects.filter(buyer=request.user)
    count = len(cart_items)
    sub_total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request,'cart.html', {'cart_items': cart_items, 'sub_total': sub_total,'total':sub_total+3,'Count':count})

def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request,'wishlist.html',context={'wishlist_items':wishlist_items})

@login_required  
def profile_view(request):
    if request.method == 'POST':
        username = request.POST.get("name2")  
        email = request.POST.get("email2")
        
        # Update the current user's username and email
        request.user.username = username
        request.user.email = email
        
        # Save the user instance to the database
        request.user.save()
        
        messages.success(request, 'Profile Updated Successfully!')
        return redirect('profile')
    else:
        context = {'user': request.user}  # Pass the user object to the template
        return render(request, 'profile.html', context)
    
@login_required
def add_to_cart(request,product_id):
    buyer = request.user
    product = get_object_or_404(Product,product_id = product_id)

    # Check if the product is already in the user's cart
    cart_item,created= Cart.objects.get_or_create(buyer=buyer, product=product)

    if not created:
        cart_item.save()
    return redirect('cart')

@login_required
def delete_cart_item(request,product_id):
    cart_item = get_object_or_404(Cart, product__product_id=product_id, buyer=request.user)
    cart_item.delete()
    return redirect('cart')  

def add_to_wishlist(request,product_id):
    user = request.user
    product = get_object_or_404(Product,product_id = product_id)

    wishlist_item,created= Wishlist.objects.get_or_create(user=user, product=product)
    if not created:
        wishlist_item.save()
    return redirect('wishlist')

def delete_wishlist_item(request,product_id):
    wishlist_item = get_object_or_404(Wishlist, product__product_id=product_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist')  

def checkout(request):
    if request.method == 'POST':
        # Get the user's cart items
        user_cart_items = Cart.objects.filter(buyer=request.user)

        if not user_cart_items.exists():
            # If no items in the cart, return or show an error message
            return redirect('cart')  # Redirect back to cart if no items

        # Calculate the total amount from the cart
        total_amount = user_cart_items.aggregate(total=Sum(F('product__price')))['total'] or 0

        # Create the order
        order = Order.objects.create(
            buyer=request.user,
            total_amount=total_amount,
            status='Pending'
        )

        # Link the cart items to the order and update stock
        for cart_item in user_cart_items:
            order.cart_items.add(cart_item)  # Add cart items to the order
            cart_item.product.stock -= 1  # Update stock based on quantity
            cart_item.product.save()  # Save the product with updated stock

        order.save()

        # After creating the order, you may want to clear the cart
        #user_cart_items.delete()

        # Redirect to the order summary or orders page
        return redirect('order_summary', order_id=order.order_id)  # Redirect to order summary page

    return render(request, 'orders.html')


    

def order_summary(request,order_id):
    order = get_object_or_404(Order, order_id=order_id, buyer=request.user)

    context = {
        'order': order,
        'cart_items': order.cart_items.all(),  # Cart items associated with the order
        'total_amount': order.total_amount,
        'status': order.status,
        'order_date': order.order_date,
    }
    return render(request, 'orders.html', context)


def sample(request):
    students = Product.objects.all()
    context = {
        'all_students':students
    }
    return render(request,'sample.html',context = context)