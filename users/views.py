from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import UserForm


def signup_view(request):
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('users:login')

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)

            return redirect('dashboard:dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid user or password'})

    return render(request, 'login.html', {})


def logout_view(request):
    logout(request)
    
    return redirect('users:login')