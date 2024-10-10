from django.shortcuts import render,redirect

# Create your views here.
def get_home_page(request):
    return render(request,'home.html',context={})