from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.shortcuts import redirect, render, reverse
from django.urls.base import reverse_lazy
from .forms import UserForm, Password
import requests
from decouple import config


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():

            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': config('GOOGLE_RECAPTCHA_SECRET_KEY'),
                'response': recaptcha_response
            }
            r = requests.post(
                'https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''

            if result['success']:
                form.save()
                return redirect('users:login')
            else:
                messages.error(request, 'Invalid reCAPTCHA. Please try again.')
                return HttpResponseRedirect(reverse('users:signup'))
        else:
            return render(request, 'signup.html', {'form': form})

    context = {
        'form': form,
    }

    return render(request, 'signup.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)

            return redirect('dashboard:dashboard')
        else:
            messages.error(request=request,
                           message='Invalid user or password!')
            return HttpResponseRedirect(reverse('users:login'))

    return render(request, 'login.html', {})


def logout_view(request):
    logout(request)

    return redirect('dashboard:home')


def error_404(request, exception):

    return render(request, '404.html')


@login_required
def detail_view(request):
    user = request.user
    form = Password(user=user)

    context = {
        'form': form,
        'user': user
    }

    if request.method == 'POST':
        form = Password(data=request.POST, user=user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed succesfully!')
        else:
            for field in form:
                for error in field.errors:
                    messages.add_message(request=request, level=messages.ERROR, message=error)
        
        return HttpResponseRedirect(reverse('users:detail'))

    return render(request, 'detail.html', context)
