from rest_framework import serializers
from .models import Task, TaskHistory


class TaskSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskHistory
        fields = '__all__'
