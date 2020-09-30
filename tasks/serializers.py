from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'


