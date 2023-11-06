
from django.urls import reverse, resolve
from django.test import SimpleTestCase
from rest_framework import status
from . views import register, ProfilView, login,UserLoginAPIView, tableau_de_bord, LoginView,prospection_api, enregistrer_client_api
from django.contrib.auth.views import LoginView

class TestUrls(SimpleTestCase):
    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func,register)

    def test_ProfilView_url_resolves(self):
            url = reverse('ProfilView')
            self.assertEqual(resolve(url).func,ProfilView)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_tableau_de_bord_url_resolves(self):
        url = reverse('tableau_de_bord')
        self.assertEqual(resolve(url).func,tableau_de_bord)  