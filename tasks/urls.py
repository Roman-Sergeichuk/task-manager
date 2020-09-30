
from django.urls import path
from . import views
from django.contrib.auth.decorators import permission_required
from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = [
    path('', views.index),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tasks/', views.readings_list, name='readings_list'),
    path('dashboard/tasks/new/', views.tasks_new, name='tasks_new'),
]
