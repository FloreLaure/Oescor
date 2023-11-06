from django.urls import path
from . import views
from .views import  enregistrer_client_api,UserLoginAPIView,prospection_api,list_produit_api,list_clients_api
from django.contrib.auth.views import LoginView,LogoutView



urlpatterns = [ 
    path('', views.index, name ='index'),
    path('tableau_de_bord/', views.tableau_de_bord, name ='tableau_de_bord'),
    path('bon', views.bon_score, name ='bon_score'),
    path('mauvais', views.mauvais_score, name ='mauvais_score'),
    path('register', views.register, name ='register'),
   
    # path('enregistrer_commercial/', views.enregistrer_commercial, name='enregistrer_commercial'),
    path('enregistrer_client_web/', views.enregistrer_client_web, name='enregistrer_client_web'),
    path('enregistrer_administrateur/', views.enregistrer_administrateur, name='enregistrer_administrateur'),
    path('ProfilView/', views.ProfilView, name='ProfilView'),
    path('api/enregistrer_client/', enregistrer_client_api.as_view(), name='enregistrer_client_api'),
    path('api/prospection_api/', prospection_api.as_view(), name='prospection_api'),
    path('api/list_produit_api/', list_produit_api.as_view(), name='list_produit_api'),
    
    path('api/list_clients_api/', list_clients_api.as_view(), name='list_clients_api'),
    path('api/login/', UserLoginAPIView.as_view(), name='api_login'),
    path('login/', LoginView.as_view(template_name='registration/login.html'),name='login'),
    path('products/', views.product_list, name='product_list'),
    path('profil_list/', views.profil_list, name='profil_list'),
    path('client_list/', views.client_list, name='client_list'),
    path('add_product/', views.add_product, name='add_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('product/<int:pk>/update/', views.update_product, name='update_product'),
    path('profil/<int:pk>/', views.profil_detail, name='profil_detail'),
    path('profil/<int:pk>/delete/', views.delete_profil, name='delete_profil'),
    path('profil/<int:pk>/update/', views.update_profil, name='update_profil'),
     path('total_clients/', views.total_clients, name='total_clients'),
    path('enregistrer_super_administrateur/', views.enregistrer_super_administrateur, name='enregistrer_super_administrateur'),
]
