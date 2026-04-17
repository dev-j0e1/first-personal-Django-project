from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title 
    
    class Meta:
        ordering = ['-create']


    def update_task(self, title=None, description=None, complete=None):
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if complete is not None:
            self.complete = complete
        self.save()
        return self

    def delete_task(self):
        self.delete()


    @classmethod
    def create_task(cls, user, title, description=None):
        return cls.objects.create(
            user = user,
            title = title,
            description = description or "",
            complete = False,
        )