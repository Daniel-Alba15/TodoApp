from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
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

        print(form.errors)
        if form.is_valid():
            form.save()

            return redirect('dashboard:dashboard')

    return render(request, 'add.html', {'user': request.user.id})


@login_required
def delete_todo(request, id):
    todo = Todos.objects.get(id=id)

    if request.method == 'POST':
        todo.delete()

        return redirect('dashboard:dashboard')

    return render(request, 'delete.html', {'todo': todo})


@login_required
def edit_todo(request, id):
    form = TodoForm()
    todo = get_object_or_404(Todos, id=id, user_id=request.user.id)

    if request.method == 'POST':
        form = TodoForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            todo.title = data.get('title')
            todo.description = data.get('description')
            todo.is_done = data.get('is_done')
            todo.save()

            return redirect('dashboard:dashboard')

    context = {
        'todo': todo,
        'user': request.user.id,
    }

    return render(request, 'edit.html', context)

def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')

    return render(request, 'home.html')
