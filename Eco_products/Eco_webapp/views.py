from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserDetails


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
        
        if UserDetails.objects.filter(email=email).exists():
            messages.error(request, 'This email is already registered.')
            return redirect('register')
        
        # Assign a default role, for example, 'Buyer'
        default_role = 'Buyer'
        
        # Create a new CustomUser entry
        custom_user = UserDetails.objects.create(
            name=name,
            email=email,
            password=password,
            role=default_role
        )
        custom_user.save()
        messages.success(request, 'User registered successfully!')
        return redirect('login')
    
    return render(request, 'register.html')


    
def product_listing(request):
    return render(request,'product_listing.html',context={})

def product_detail(request):
    return render(request,'single_product_view.html',context={})


