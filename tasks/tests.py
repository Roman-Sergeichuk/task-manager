from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .models import Task
from django.utils import timezone
from .serializers import TaskSerializer


class TaskManagerTestCase(TestCase):

    def setUp(self):
        self.first_user = User.objects.create(username='first_user', password="Efwefwef1223")

        self.client = APIClient()
        self.client.force_authenticate(user=self.first_user)

    def test_can_create_task(self):
        """Пользователь может успешно создать задачу"""

        task_data = {
            "title": f"Test title {timezone.now()}",
            "description": "Test description",
            "completion_date": "2020-10-10",
            "status": "NEW"
        }

        response = self.client.post(
            path='/tasks/',
            data=task_data,
        )

        task_in_db = Task.objects.get(title=task_data['title'])
        serializer = TaskSerializer(task_in_db)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_can_register_in_system(self):
        """Пользователь может зарегистрироваться в сервисе, задав пару логин-пароль"""

        user_data = {"username": "test_can_register_in_system", "password": "Wegwegewwe1242"}

        new_client = APIClient()

        response = new_client.post(
            path='/auth/users/',
            data=user_data,
        )
        users_from_db = User.objects.filter(username=user_data['username'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(users_from_db), 1)

    def test_can_authorize_if_exists(self):
        """Пользователь может авторизоваться в сервисе предоставив пару логин-пароль и получив в ответе токен"""

        user_data = {"username": "test_can_authorize", "password": "Wegwegewwe1242"}
        new_client = APIClient()
        new_client.post(
            path='/auth/users/',
            data=user_data,
        )

        response = new_client.post(
            path='/auth/token/login/',
            data=user_data,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'auth_token')

# Пользователь может посмотреть список своих задач

# Пользователь может редактировать задачу
# Пользователь может посмотреть историю изменения каждой задачи

# Пользователь может отфильтровать задачи по статусу и времени завершения

# В системе может существовать много пользователей






