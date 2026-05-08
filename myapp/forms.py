from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task


class TaskForm(forms.ModelForm):
    """Form for creating and editing tasks."""

    class Meta:
        model = Task
        fields = ['title', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'What do I need to do?...',
                'maxlength': '200',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Add some details about this task...',
                'rows': '3'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }, choices=[
                (1, 'To Do'),
                (2, 'In Progress...'),
                (3, 'Complete ✅')
            ])
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make title required
        self.fields['title'].required = True


class TaskUpdateForm(forms.ModelForm):
    """Form for updating existing tasks."""

    class Meta:
        model = Task
        fields = ['title', 'description', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'id': 'editTitle',
                'maxlength': '200',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'id': 'editDescription',
                'rows': '3'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'id': 'statusSelector',
                'required': True
            }, choices=[
                (1, 'To Do'),
                (2, 'In Progress...'),
                (3, 'Complete ✅')
            ])
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make title required
        self.fields['title'].required = True