from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .models import Task
from django.utils import timezone
from .serializers import TaskSerializer


class TaskManagerTestCase(TestCase):

    def setUp(self):
        self.default_user = User.objects.create(username='default_user', password="Efwefwef1223")

        self.client = APIClient()
        self.client.force_authenticate(user=self.default_user)

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

    def test_can_show_own_tasks(self):
        """Пользователь может посмотреть список своих задач"""

        first_user = User.objects.create(username='first_user', password="Efwefwef1223")
        second_user = User.objects.create(username='second_user', password="Efwefwef1223")

        Task.objects.create(
            author=first_user,
            title=f"Test title {timezone.now()}",
            description='Test description',
            completion_date="2020-10-10",
            status="NEW"
        )
        Task.objects.create(
            author=first_user,
            title=f"Test title {timezone.now()}",
            description='Test description',
            completion_date="2020-10-10",
            status="NEW"
        )
        Task.objects.create(
            author=first_user,
            title=f"Test title {timezone.now()}",
            description='Test description',
            completion_date="2020-10-10",
            status="NEW"
        )

        Task.objects.create(
            author=second_user,
            title=f"Test title {timezone.now()}",
            description='Test description',
            completion_date="2020-10-10",
            status="NEW"
        )
        Task.objects.create(
            author=second_user,
            title=f"Test title {timezone.now()}",
            description='Test description',
            completion_date="2020-10-10",
            status="NEW"
        )

        new_client = APIClient()
        new_client.force_authenticate(user=first_user)

        response = new_client.get(
            path='/tasks/',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_can_edit_tasks_and_show_history(self):
        """Пользователь может редактировать задачу и смотреть историю изменений задачи"""

        test_user = User.objects.create(username='test_user', password="Efwefwef1223")

        task = Task.objects.create(
            author=test_user,
            title=f"Test title {timezone.now()}",
            description='Test description',
            completion_date="2020-10-10",
            status="NEW"
        )

        task_data = {
            "title": f"{task.title}",
            "description": f"{task.description}",
            "completion_date": f"{task.completion_date}",
            "status": "IN_PROGRESS"
        }

        new_client = APIClient()
        new_client.force_authenticate(user=test_user)

        response = new_client.put(
            path=f'/tasks/{task.id}/', data=task_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = new_client.get(
            path=f'/tasks/{task.id}/',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'IN_PROGRESS')

        response = new_client.get(
            path=f'/history/?task_id={task.id}'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_can_filer_tasks(self):
        """Пользователь может отфильтровать задачи по статусу и времени завершения"""

        test_user = User.objects.create(username='test_user', password="Efwefwef1223")

        Task.objects.create(
            author=test_user,
            title=f"Test title {timezone.now()}",
            description='Test description',
            completion_date="2020-10-05",
            status="NEW"
        )
        Task.objects.create(
            author=test_user,
            title=f"Test title {timezone.now()}",
            description='Test description',
            completion_date="2020-10-10",
            status="IN_PROGRESS"
        )
        Task.objects.create(
            author=test_user,
            title=f"Test title {timezone.now()}",
            description='Test description',
            completion_date="2020-10-10",
            status="COMPLETED"
        )

        new_client = APIClient()
        new_client.force_authenticate(user=test_user)

        response = new_client.get(
            path='/tasks/?status=NEW',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        response = new_client.get(
            path='/tasks/?completion_date=2020-10-10',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_can_show_own_tasks(self):
        """Неавторизованный пользователь не может просмотреть список задач"""

        auth_user = User.objects.create(username='auth_user', password="Efwefwef1223")

        Task.objects.create(
            author=auth_user,
            title=f"Test title {timezone.now()}",
            description='Test description',
            completion_date="2020-10-10",
            status="NEW"
        )
        Task.objects.create(
            author=auth_user,
            title=f"Test title {timezone.now()}",
            description='Test description',
            completion_date="2020-10-10",
            status="NEW"
        )
        Task.objects.create(
            author=auth_user,
            title=f"Test title {timezone.now()}",
            description='Test description',
            completion_date="2020-10-10",
            status="NEW"
        )

        new_client = APIClient()

        response = new_client.get(
            path='/tasks/',
        )
        print(response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_esist_many_users(self):
        """ системе может существовать много пользователей"""

        first_user_data = {"username": "first_user", "password": "Wegwegewwe1242"}
        second_user_data = {"username": "second_user", "password": "Wegwegewwe1242"}

        new_client = APIClient()

        response = new_client.post(
            path='/auth/users/',
            data=first_user_data,
        )

        response = new_client.post(
            path='/auth/users/',
            data=second_user_data,
        )

        users_from_db = User.objects.all()
        print(users_from_db)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(users_from_db), 3)
