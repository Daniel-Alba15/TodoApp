from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, render, reverse
from .forms import UserForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('users:login')
        # else:
        #     messages.error(request, message=form)
        #     return HttpResponseRedirect(reverse('users:signup'))
        #     return render(request, 'signup.html', {'form': form})

    return render(request, 'signup.html', {'form': form})


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
