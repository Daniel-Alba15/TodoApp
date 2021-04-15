from django import forms
from django.core.exceptions import ValidationError
from .models import MyUser

class UserForm(forms.Form):
    email = forms.EmailField(max_length=200)
    name = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)


    def clean(self): 
        data = super().clean()
        password = data['password']
        password_confirm = data['password_confirm']

        if password != password_confirm:
            raise ValidationError(('Passwords does not match!'), code='invalid')

    def save(self):
        data = self.cleaned_data
        data.pop('password_confirm')
        user = MyUser.objects.create_user(**data)
        user.save()