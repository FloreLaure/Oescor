from django.test import TestCase
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse

class UserLoginAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('api_login')  
        self.user = User.objects.create_user(
            username='lari',
            password='inside@5'
        )
    def test_user_login_with_valid_credentials(self):
        data = {
            'username': 'lari',
            'password': 'inside@5'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    def test_user_login_with_invalid_credentials(self):
        data = {
            'username': 'lari',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)
    def test_user_login_with_missing_credentials(self):
        data = {}  # Ne contient ni 'username' ni 'password'
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)