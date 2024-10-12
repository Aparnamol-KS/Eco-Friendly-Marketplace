from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User


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
        username = request.POST["name1"]
        password = request.POST["pwd1"]
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return redirect('register')
        
        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        
        # Authenticate and log the user in
        if user is not None:
            login(request, user)
            messages.success(request, 'You have registered successfully! Welcome!')
            return redirect('home')
        else:
            messages.error(request, 'There was a problem registering. Please try again.')
            return redirect('register')
    else:
        return render(request, 'register.html')

    

