import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from to_do.models import Todo


class TodoTests(APITestCase):
    def setUp(self):
        self.user_test_instance = {'username': 'test_user', 'password': 'pass123'}
        registration_url = reverse("registration-list")
        user_response = self.client.post(registration_url, self.user_test_instance, format='json')
        self.token = f'Token {user_response.data["token"]}'

        self.todo_test_instance = {'title': 'Test todo',
                                   'text': 'Test todo',
                                   'completion_date': datetime.date(2021, 1, 1)
                                   }
        todo_url = reverse('todo-list')
        self.client.post(todo_url, self.todo_test_instance, format='json', HTTP_AUTHORIZATION=self.token)

    def test_list_action_with_token(self):
        """
        Пользователь может просматривать только свой список задач.
        """
        todo_url = reverse('todo-list')
        todo_response = self.client.get(todo_url, format='json', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(todo_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(todo_response.data), 1)

    def test_list_action_without_token(self):
        """
        Без токена промастривать список задач нельзя.
        """
        todo_url = reverse('todo-list')
        todo_response = self.client.get(todo_url, format='json')
        self.assertEqual(todo_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_action_with_token(self):
        """
        Просмотреть конкретную задачу можно только с токеном.
        """
        todo = Todo.objects.first()
        todo_url = reverse('todo-detail', args=[todo.id])
        todo_response = self.client.get(todo_url, format='json', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(todo_response.status_code, status.HTTP_200_OK)
        self.assertEqual(todo_response.data['title'], todo.title)
        self.assertEqual(todo_response.data['completion_date'], f'{todo.completion_date:%Y-%d-%m}')
        self.assertEqual(todo_response.data['complete'], todo.complete)
        self.assertEqual(todo_response.data['user'], todo.user.id)

    def test_retrieve_action_without_token(self):
        """
        Просмотреть конкретную задачу без токена нельзя.
        """
        todo = Todo.objects.first()
        todo_url = reverse('todo-detail', args=[todo.id])
        todo_response = self.client.get(todo_url, format='json')
        self.assertEqual(todo_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_action_with_token(self):
        """
        Задачу может создать только пользователь с токеном.
        """
        todo_url = reverse('todo-list')
        todo_response = self.client.post(todo_url, self.todo_test_instance, format='json',
                                         HTTP_AUTHORIZATION=self.token)
        self.assertEqual(todo_response.status_code, status.HTTP_201_CREATED)

    def test_create_action_without_token(self):
        """
        Задачу без токена создать нельзя.
        """
        self.todo_new_test_instance = {'title': 'New Test todo',
                                       'text': 'Test todo',
                                       'completion_date': datetime.date(2021, 1, 1)
                                       }
        todo_url = reverse('todo-list')
        todo_response = self.client.post(todo_url, self.todo_new_test_instance, format='json')
        self.assertEqual(todo_response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_action_with_token(self):
        """
        Отметить задачу как выполненную может только владелец.
        """
        todo_new_test_instance = {
                                  'complete': True
                                  }
        todo = Todo.objects.first()
        todo_url = reverse('todo-detail', args=[todo.id])
        todo_response = self.client.patch(todo_url, todo_new_test_instance, HTTP_AUTHORIZATION=self.token)
        todo = Todo.objects.first()
        self.assertEqual(todo_response.status_code, status.HTTP_200_OK)
        self.assertEqual(todo_response.data['complete'], todo.complete)

    def test_update_action_without_token(self):
        """
        Без токена отметить выполнение задачи нельзя.
        """
        todo_new_test_instance = {
                                  'complete': True
                                  }
        todo = Todo.objects.first()
        todo_url = reverse('todo-detail', args=[todo.id])
        todo_response = self.client.patch(todo_url, todo_new_test_instance)
        todo = Todo.objects.first()
        self.assertEqual(todo_response.status_code, status.HTTP_401_UNAUTHORIZED)
