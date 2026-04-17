from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("todo/", views.todo, name="todo"),
    path("todo/<int:task_id>/update/", views.update_task, name="update_task"),
    path("todo/<int:task_id>/delete/", views.delete_task, name="delete_task"),
    ]

