from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.views.generic.list import ListView
from .models import Task
import logging
logger = logging.getLogger(__name__)
from django.conf import settings

from django.contrib.auth.decorators import login_required
from .forms import TaskForm, TaskUpdateForm



@login_required(login_url=settings.LOGIN_PATH)
def todo(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f'"{task.title}" task created successfully!')
            return redirect("todo")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TaskForm()

    # Add status filtering (stretch goal)
    status_filter = request.GET.get('status')
    tasks = Task.objects.filter(user=request.user)

    if status_filter and status_filter.isdigit():
        tasks = tasks.filter(status=int(status_filter))

    # Order tasks with custom ordering for status
    from django.db.models import Case, When
    tasks = tasks.annotate(
        custom_order=Case(
            When(status=2, then=0),  # In Progress first
            When(status=1, then=1),  # To Do second
            When(status=3, then=2),  # Complete last
        )
    ).order_by('custom_order', '-create')

    return render(request, "todo.html", {
        "active_page": "todo",
        "tasks": tasks,
        "form": form,
        "status_filter": status_filter,
    })

@login_required(login_url=settings.LOGIN_PATH)
def update_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        messages.error(request, "Task not found.")
        return redirect("todo")

    if request.method == "POST":
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            updated_task = form.save()
            messages.success(request, f'"{updated_task.title}" task updated successfully!')

            # Check if this is an AJAX request
            if request.headers.get('Content-Type') == 'multipart/form-data' or request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                return redirect("todo")
            return redirect("todo")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TaskUpdateForm(instance=task)

    return render(request, "edit_task.html", {
        "task": task,
        "form": form,
        "active_page": "todo",
    })

@login_required(login_url=settings.LOGIN_PATH)
def delete_task(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        messages.error(request, "Task not found.")
        return redirect("todo")

    if request.method == "POST":
        task.delete_task()
        messages.success(request, "Task deleted successfully.")
        messages.add_message(request, messages.INFO, "Task has been deleted successfully!")
        return redirect("todo")

    return render(request, "confirm_delete.html", {
        "task": task,
        "active_page": "todo",
    })

def home(request):
    logger.info("Homepage accessed")
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


