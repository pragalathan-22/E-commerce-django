from .models import Product
from django.shortcuts import render, get_object_or_404
from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from . models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm


# views.py


from django.shortcuts import get_object_or_404, render
from .models import Category, Product


def category(request, category_name):
    # Look up the category or return a 404 error if not found
    category = get_object_or_404(Category, name=category_name) 
   
    # Retrieve products related to the category
    products = Product.objects.filter(category=category)

    # Render the template with the products and category
    return render(request, 'category.html', {'products': products, 'category': category})


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product.html', {'product': product})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(
        request, ("you have been logged out...thanks for shoping bye"))
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # login user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("you have registered succussfully..."))
            return redirect('home')
        else:
            messages.success(request, ("your registration failed..."))
            return redirect('home')

    return render(request, 'register.html', {'form': form})
