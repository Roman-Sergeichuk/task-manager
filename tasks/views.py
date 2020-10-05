from rest_framework import viewsets
from .models import Task, TaskHistory
from .serializers import TaskSerializer, TaskHistorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAuthor


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthor]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'completion_date']

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(author=user)


class TaskHistoryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = TaskHistory.objects.all()
    serializer_class = TaskHistorySerializer
    permission_classes = [IsAuthor]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['task_id', 'title']

    def get_queryset(self):
        user = self.request.user
        return TaskHistory.objects.filter(author=user)
