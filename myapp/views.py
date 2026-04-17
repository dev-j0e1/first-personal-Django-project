from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.views.generic.list import ListView
from .models import Task

from django.contrib.auth.decorators import login_required


@login_required(login_url="/myapp/login/")
def todo(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()

        if title:
            Task.create_task(request.user, title, description)
            return redirect("todo")

    tasks = Task.objects.filter(user=request.user)
    return render(request, "todo.html", {
        "active_page": "todo",
        "tasks": tasks,
    })

@login_required(login_url="/myapp/login/")
def update_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        messages.error(request, "Task not found.")
        return redirect("todo")

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        complete = request.POST.get("complete") == "on"

        if title:
            task.update_task(title=title, description=description, complete=complete)
            messages.success(request, "Task updated successfully.")
            return redirect("todo")
        else:
            messages.error(request, "Title cannot be empty.")

    return render(request, "edit_task.html", {
        "task": task,
        "active_page": "todo",
    })

@login_required(login_url="/myapp/login/")
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        messages.error(request, "Task not found.")
        return redirect("todo")

    if request.method == "POST":
        task.delete_task()
        messages.success(request, "Task deleted successfully.")
        return redirect("todo")

    return render(request, "confirm_delete.html", {
        "task": task,
        "active_page": "todo",
    })

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
        next = request.GET.get("next")

        UserModel = get_user_model()
        user = UserModel.objects.filter(email__iexact=email).first()

        if user and check_password(password, user.password):
            # user.password is stored as a secure hash (PBKDF2 by default in Django)
            # the plain text password never gets stored in the DB.
            login(request, user)
            messages.success(request, "login successful, welcome John Doe")
            if next:
                return redirect(next)

            return redirect("home")
        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, "login.html", {"active_page": "login"})


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


