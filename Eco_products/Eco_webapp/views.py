from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Eco_webapp.models import Product,Cart,Wishlist,Order,orderedItems,UserProfile
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
        name = request.POST.get('name1')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        
        image = request.FILES.get('photo')  # Use .get() to avoid MultiValueDictKeyError
        print("Image:", image)
        
        try:
            # Create a new user and set the password securely
            user = User.objects.create_user(
                username=name,
                email=email,
                password=password  
            )

            # Create UserProfile associated with the user
            userprofile = UserProfile.objects.create(
                user=user,  # Use the user object here
                address=address,
                photo=image  # This can be None if no file was uploaded
            )

            # Success message and redirect to login
            messages.success(request, 'User registered successfully!')
            return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('register')

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


@login_required
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
    # Get the user's profile (if it exists)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        username = request.POST.get("name2")  
        email = request.POST.get("email2")
        address = request.POST.get("address")  
        image = request.FILES.get("photo")  

        # Update the current user's username and email
        request.user.username = username
        request.user.email = email

        # Save the user instance to the database
        request.user.save()

        # Update the user's profile information
        user_profile.address = address
        if image:  # Check if a new image is uploaded
            user_profile.photo = image
            
        # Save the user profile instance to the database
        user_profile.save()

        messages.success(request, 'Profile Updated Successfully!')
        return redirect('profile')

    else:
        context = {
            'user': request.user,  # Pass the user object to the template
            'address': user_profile.address,  # Pass the address from the user profile
            'photo': user_profile.photo,  # Pass the photo from the user profile
        }
        return render(request, 'profile.html', context)

    
@login_required
def add_to_cart(request,product_id):
    buyer = request.user
    product = get_object_or_404(Product,product_id = product_id)

    # Check if the product is already in the user's cart
    cart_item,created= Cart.objects.get_or_create(buyer=buyer, product=product)

    if created:
        messages.success(request, 'Added to Cart')
        # Check if the product is in the user's wishlist and delete it
        try:
            wishlist_item = Wishlist.objects.get(user=buyer, product=product)
            wishlist_item.delete()  # Remove the item from the wishlist
        except Wishlist.DoesNotExist:
            pass  # Item was not in the wishlist, do nothing
    else:
        messages.info(request, 'This product is already in your Cart.')

    return redirect('product_detail', product_id=product_id)

@login_required
def delete_cart_item(request,product_id):
    cart_item = get_object_or_404(Cart, product__product_id=product_id, buyer=request.user)
    cart_item.delete()
    messages.success(request, 'Removed from Cart')
    return redirect('cart')  

@login_required
def add_to_wishlist(request,product_id):
    user = request.user
    product = get_object_or_404(Product,product_id = product_id)

    wishlist_item,created= Wishlist.objects.get_or_create(user=user, product=product)
    if created:
        messages.success(request, 'Added to Wishlist')
    else:
        messages.info(request, 'This product is already in your Wishlist.')

    return redirect('product_detail', product_id=product_id)

@login_required
def delete_wishlist_item(request,product_id):
    wishlist_item = get_object_or_404(Wishlist, product__product_id=product_id, user=request.user)
    wishlist_item.delete()
    messages.success(request, 'Removed from Wishlist')
    return redirect('wishlist')  
    

@login_required
def checkout(request):
    if request.method == 'POST':
        # Get the user's cart items
        user_cart_items = Cart.objects.filter(buyer=request.user)

        if not user_cart_items.exists():
            return redirect('cart')  # Redirect back to cart if no items

        # Calculate the total amount
        total_amount = user_cart_items.aggregate(total=Sum(F('product__price')))['total'] or 0

        # Create the order
        order = Order.objects.create(
            buyer=request.user,
            total_amount=total_amount,
            status='Pending'
        )

        # Create order items (copy details from cart)
        for cart_item in user_cart_items:
            orderedItems.objects.create(
                order=order,
                product_name=cart_item.product.product_name,
                price=cart_item.product.price,
                product_id=cart_item.product.product_id,
                product_image = cart_item.product.product_image
            )

            # Reduce stock of the product
            cart_item.product.stock -= 1
            cart_item.product.save()

        # Clear the user's cart
        user_cart_items.delete()

        # Redirect to the order summary page
        return redirect('order_summary')

    return render(request,'orders.html')



@login_required
def order_summary(request):
    
    # Get all orders for the logged-in user
    orders = Order.objects.filter(buyer=request.user).prefetch_related('order_items')

     # Check if there are no orders
    if not orders.exists():
        context = {
            'order_details': None,  # No orders to display
            'message': 'No orders found.',  # Optional message for no orders
        }
        return render(request, 'orders.html', context)
    

    # Prepare data for each order
    order_details = []
    for order in orders:
        # Get the associated UserProfile to access the address
        user_profile = UserProfile.objects.get(user=order.buyer)
        
        # Calculate the total price for each order
        total_price = sum(item.price for item in order.order_items.all())
        order.total_price = total_price

    context = {
        'orders': orders,
        'shipping_address': user_profile.address
    }
    return render(request, 'orders.html', context)

@login_required
def delete_order(request, order_id):
    # Fetch the order item; ensure you're referring to the correct model
    order_item = get_object_or_404(Order, order_id=order_id, buyer=request.user)  # Changed from 'orderedItems' to 'Order'
    
    # Delete the order
    order_item.delete()
    
    # Redirect to the order summary page
    return redirect('order_summary') 


from django.contrib.auth.decorators import user_passes_test

def admin_check(user):
    return user.is_authenticated and user.is_staff  # or custom logic like user.profile.is_admin

@user_passes_test(admin_check)
def admin_dashboard(request):
    # Logic for your admin dashboard
    return render(request, 'admin_dashboard.html')
