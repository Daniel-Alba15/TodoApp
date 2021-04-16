from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Todos
from .forms import TodoForm


@login_required
def dashboard(request):
    data = Todos.objects.filter(user_id=request.user.id)

    context = {'todos': data}

    return render(request, 'dashboard.html', context)

@login_required
def add_todo(request):
    form = TodoForm()

    if request.method == 'POST':
        form = TodoForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('dashboard:dashboard')

    return render(request, 'add.html', {'user': request.user.id})
