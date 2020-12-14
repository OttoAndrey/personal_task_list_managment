from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class NumPairAPITests(APITestCase):
    def setUp(self):
        User.objects.create(username='first_user', password='pass1234')
        User.objects.create(username='second_user', password='pass1234')

        self.count_before = User.objects.count()
        self.user_instance = {'username': 'third_user', 'password': 'pass1234'}

    def test_create_action_correct_instance(self):
        """
        Регистрация нового пользователя.
        """
        registration_url = reverse('registration-list')
        registration_response = self.client.post(registration_url, self.user_instance, format='json')

        self.assertEqual(registration_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), self.count_before + 1)
        self.assertEqual(self.user_instance['username'], registration_response.data['username'])
        self.assertEqual(Token.objects.last().key, registration_response.data['token'])

    def test_login_action_correct(self):
        """
        Логин пользователя с существующими данными.
        """
        user_url = reverse('registration-list')
        self.client.post(user_url, self.user_instance, format='json')

        login_url = reverse('api-login')
        login_response = self.client.post(login_url, self.user_instance, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertEqual(login_response.data['username'], self.user_instance['username'])
        self.assertEqual(login_response.data['token'], Token.objects.last().key)

    def test_login_action_incorrect_data(self):
        """
        Логин пользователя с несуществующими данными.
        """
        new_user_instance = {'username': 'fourth_user', 'password': 'pass1234'}
        login_url = reverse('api-login')
        login_response = self.client.post(login_url, new_user_instance, format='json')
        self.assertEqual(login_response.status_code, status.HTTP_400_BAD_REQUEST)
