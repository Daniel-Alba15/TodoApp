from django import forms
from django.core.exceptions import ValidationError
from .models import MyUser


class UserForm(forms.Form):
    email = forms.EmailField(max_length=200)
    name = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = super().clean().get('email')
        print(email)
        print('aca')
        query = MyUser.objects.filter(email=email)

        if query:
            self.add_error('email', ValidationError(
                ('Email already exists, please login'), code='eror'))

        return email

    def clean(self):
        data = super().clean()
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password != password_confirm:
            self.add_error('password', ValidationError(
                ('Passwords does not match!'), code='invalid'))

    def save(self):
        data = self.cleaned_data
        data.pop('password_confirm')
        user = MyUser.objects.create_user(**data)
        user.save()
