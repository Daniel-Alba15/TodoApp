from django.db import router
from django.urls import path
from . import views


urlpatterns = [
    path(route='', view=views.home_view, name='home'),
    path(route='dashboard/', view=views.dashboard, name='dashboard'),
    path(route='add/', view=views.add_todo, name='add'),
    path(route='delete/<int:id>/', view=views.delete_todo, name='delete'),
    path(route='edit/<int:id>/', view=views.edit_todo, name='edit'),
]
