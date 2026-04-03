from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib import messages


def home(request):
    return render(request, "home.html", {"active_page": "home"})


def about(request):
    """Render the about page."""
    return render(request, "about.html", {"active_page": "about"})


def contact(request):
    """Render the contact page."""
    return render(request, "contact.html", {"active_page": "contact"})


def login_view(request):
    """Handle user login with form validation and authentication by email."""
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        UserModel = get_user_model()
        user = UserModel.objects.filter(email__iexact=email).first()

        if user and user.check_password(password):
            login(request, user)
            messages.success(request, "login successful, welcome John Doe")
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, "login.html", {"active_page": "login"})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


