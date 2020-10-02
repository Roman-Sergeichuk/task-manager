from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from .models import Task, TaskHistory
from .serializers import TaskSerializer, TaskHistorySerializer
from django_filters.rest_framework import DjangoFilterBackend


class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'completion_date']


# class TaskList(generics.ListAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['status', 'completion_date']


class TaskHistoryViewSet(viewsets.ModelViewSet):

    queryset = TaskHistory.objects.all()
    serializer_class = TaskHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task_id', 'title']
