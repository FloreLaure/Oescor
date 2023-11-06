from django.test import TestCase
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse

class LoginViewTestCase(TestCase):
    def setUp(self):
        # Créez un utilisateur de test pour le test d'authentification
        self.user = User.objects.create_user(
            username='lari',
            password='inside@5'
        )

    def test_login_view_with_valid_credentials(self):
        # Effectuez une requête POST vers la vue de connexion avec des identifiants valides
        response = self.client.post('/login/', {'username': 'lari', 'password': 'inside@5'})

        # Vérifiez que la réponse renvoie une redirection vers 'tableau_de_bord'
        self.assertRedirects(response, '/tableau_de_bord/', status_code=302, target_status_code=200)

        # Vérifiez que l'utilisateur est connecté
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    # def test_login_view_with_invalid_credentials(self):
    #     # Effectuez une requête POST vers la vue de connexion avec des identifiants invalides
    #     response = self.client.post('/login/', {'username': 'lari', 'password': 'insi5'})

    #     # Vérifiez que la réponse renvoie une redirection vers 'login' (car les identifiants sont incorrects)
    #     self.assertRedirects(response, '/tableau_de_bord/', status_code=302, target_status_code=200)

    #     # Vérifiez que l'utilisateur n'est pas connecté
    #     self.assertFalse(response.wsgi_request.user.is_authenticated)


class UserLoginAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('api_login')  # Assurez-vous d'utiliser le nom correct de l'URL

        # Créez un utilisateur de test pour les tests d'authentification
        self.user = User.objects.create_user(
            username='lari',
            password='inside@5'
        )

    def test_user_login_with_valid_credentials(self):
        # Données valides pour l'authentification
        data = {
            'username': 'lari',
            'password': 'inside@5'
        }

        response = self.client.post(self.login_url, data, format='json')

        # Assurez-vous que la réponse renvoie un code HTTP 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assurez-vous que la réponse contient un jeton (token)
        self.assertIn('token', response.data)

    def test_user_login_with_invalid_credentials(self):
        # Données invalides pour l'authentification
        data = {
            'username': 'lari',
            'password': 'wrongpassword'
        }

        response = self.client.post(self.login_url, data, format='json')

        # Assurez-vous que la réponse renvoie un code HTTP 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Assurez-vous que la réponse contient une erreur
        self.assertIn('error', response.data)

    def test_user_login_with_missing_credentials(self):
        # Données manquantes pour l'authentification
        data = {}  # Ne contient ni 'username' ni 'password'

        response = self.client.post(self.login_url, data, format='json')

        # Assurez-vous que la réponse renvoie un code HTTP 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assurez-vous que la réponse contient des erreurs de validation
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)