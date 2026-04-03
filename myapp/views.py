from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def home(request):
    return render(request, "home.html")


def login_view(request):
    """Handle user login with form validation and authentication."""
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Authentication successful
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("home")
        else:
            # Authentication failed
            messages.error(request, "Invalid username or password. Please try again.")
    
    return render(request, "login.html")


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


