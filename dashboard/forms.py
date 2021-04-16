from django import forms
from django.core.exceptions import ValidationError
from django.db.models.expressions import F
from .models import Todos


class TodoForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=500, required=False)
    user_id = forms.CharField(max_length=100)

    def save(self):
        data = self.cleaned_data

        todo = Todos(**data)
        todo.save()
