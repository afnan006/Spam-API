from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

class UserTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            phone_number='1234567890',
            username='testuser',
            password='password'
        )
        self.login_url = reverse('user_login')  # Update to match 'user_login'
        self.register_url = reverse('user_register')  # Update to match 'user_register'
        self.mark_spam_url = reverse('mark_spam')  # Update to match 'mark_spam'
        self.search_url = reverse('search')  # Update to match 'search'

    def test_user_registration(self):
        data = {
            "username": "testuser2",
            "phone_number": "0987654321",
            "email": "testuser2@example.com",
            "password": "testpassword"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        data = {
            "phone_number": "1234567890",
            "password": "password"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_mark_spam(self):
        response = self.client.post(self.login_url, {"phone_number": "1234567890", "password": "password"}, format='json')
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        data = {
            "phone_number": "1234567890"
        }
        response = self.client.post(self.mark_spam_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_contacts(self):
        response = self.client.post(self.login_url, {"phone_number": "1234567890", "password": "password"}, format='json')
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(self.search_url, {'query': 'test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
