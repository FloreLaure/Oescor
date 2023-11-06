from rest_framework import generics
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect 
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages 
from django.core.paginator import Paginator 
# from .serializers import ReserveSerializer, VoyagesSerializer, VilleSerializer, ClientSerializer, CourierSerializer 
# from rest_framework import  generics 
from django.contrib.auth.models import User
from rest_framework.response import Response 
from rest_framework.decorators import api_view 
import json 
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetConfirmView
from .forms import ClientForm,CompteForm,ProfilForm, CommercialUserCreationForm,AdministrateurUserCreationForm,ProductForm,superadminUserCreationForm
import joblib
from .models import Client, Score,Prospection, Commercial,Profil, Resultat, Graphique,Product
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserLoginSerializer,ChangerMotDePasseSerializer,ClientSerializer,ProductSerializer,ProspectionSerializer,ProfilSerializer, UserSerializer
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.generics import ListAPIView

import pandas as pd


# Votre code Django ici






@login_required
def tableau_de_bord(request):
    user = request.user
    # profil = Profil.objects.get(user=user)
    # if Profil.user.is_super:
    #     # Logique spécifique pour le superutilisateur
    #     resultats = Resultat.objects.all()
    #     clients = Client.objects.all()
    #     total_clients = Client.objects.count()
    #     scores = Score.objects.all()
    #     scores_bon = Resultat.objects.filter(bon_score=True).count()
    #     scores_mauvais = Resultat.objects.filter(bon_score=False).count()
    #     graphiques = Graphique.objects.all()
    return render(request, 'tableau_de_bord_superuser.html')

    # elif Profil.user.is_commercial:
    #     commercial = Commercial.objects.get(user=user)
    #     clients_enregistres = commercial.clients_enregistres.all()
    #     total_enregistres = commercial.clients_enregistres.count()
    #     return render(request, 'tableau_de_bord_commercial.html', {'clients_enregistres': clients_enregistres, 'total_enregistres':total_enregistres})

    # elif Profil.user.is_administrateur:
    #     clients = Client.objects.all()
    #     total_clients = Client.objects.count()
    #     scores = Score.objects.all()
    #     scores_bon = Resultat.objects.filter(bon_score=True).count()
    #     scores_mauvais = Resultat.objects.filter(bon_score=False).count()
    #     graphiques = Graphique.objects.all()
    #     return render(request, 'tableau_de_bord_administrateur.html', {'clients': clients, 'scores': scores, 'graphiques': graphiques, 'total_clients': total_clients, 'scores_bon':scores_bon, 'scores_mauvais':scores_mauvais})
    # elif user.is_bloque:
    #     return Response({'message': 'Vous avez été bloqué'})

        
@login_required
def enregistrer_client_web(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            produit_id = form.cleaned_data['produit'].id
            produit = Product.objects.get(id=produit_id)
            prix_produit = produit.price
            form.save()
            return redirect('prospection')
        else:
            form = ClientForm()
    else:
        form = ClientForm()        
    return render(request, 'enregistrer_client.html', {'form': form})

logger = logging.getLogger(__name__)
class prospection_api(APIView):
     # Utilisez le décorateur pour spécifier l'authentification par session
    @permission_classes([IsAuthenticated])
    
    def post(self, request, *args, **kwargs):
        try:
            

            serializer = ProspectionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
               
                prospection = serializer.save()
                prospection_id = serializer.instance.id  # Récupérez l'ID de la prospection nouvellement créée

                # Créez un DataFrame Pandas à partir des données de la prospection
                prospection_data = {
                    
                    'Group Name':[serializer.instance.produit.groupname],
                    'Upfront Price':[serializer.instance.upfront],
                    'Unlock Price':[serializer.instance.produit.unlock],
                    'Customer Gender':[serializer.instance.client.gender],
                    'Customer Age':[serializer.instance.client.age],
                    'Customer Occupation': [serializer.instance.client.occupation],
                    'Langue': [serializer.instance.client.langue],
                    'Region':[serializer.instance.client.region]
                 
                }
                df = pd.DataFrame(prospection_data)

                # Chargez votre modèle et effectuez la prédiction ici
                model = joblib.load('C:/Users/HKWX2191/Music/project_django/web/appweb/model_dev.joblib')
                predicted_score = model.predict(df)
                

                # Mettez à jour le champ 'predicted_score' dans la prospection
                prospection = Prospection.objects.get(id=prospection_id)
                prospection.predicted_score = predicted_score[0]  # Assurez-vous que votre modèle renvoie une valeur unique
                prospection.save()

                # Sérialisez la prospection avec le champ 'predicted_score' mis à jour
                serializer_with_prediction = ProspectionSerializer(prospection)
                return Response(serializer_with_prediction.data, status=status.HTTP_201_CREATED)
            else:
                # En cas de validation de données incorrecte, journalisez les erreurs
                logger.error("Erreur de validation de données : %s", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # En cas d'autres erreurs, journalisez l'exception
            logger.error("Erreur lors du traitement de la requête : %s", e)
            return Response("Erreur lors du traitement de la requête", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class UserAPI(APIView):
#     def get(self, request):
#         if request.user.is_authenticated:
#             user = request.user
#             serializer = UserSerializer(user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response('Utilisateur non connecté', status=status.HTTP_401_UNAUTHORIZED)

# class prospection_api(APIView):
    
#     def post(self, request, *args, **kwargs):
#         try:
#             serializer = ProspectionSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 prospection = serializer.instance
#                 model = joblib.load('C:/Users/HKWX2191/Music/project_django/web/appweb/model_dev.joblib')
#                 features = [prospection.Product.groupname, prospection.upfront, prospection.Product.unlock, prospection.Client.gendes, prospection.Client.age, prospection.Client.occupation, prospection.Client.langue, prospection.Client.region]
#                 predicted_score = model.predict([features])[0]
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)

#             else:
#                 # En cas de validation de données incorrecte, journalisez les erreurs
#                 logger.error("Erreur de validation de données : %s", serializer.errors)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             # En cas d'autres erreurs, journalisez l'exception
#             logger.error("Erreur lors du traitement de la requête : %s", e)
#             return Response("Erreur lors du traitement de la requête", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def voir_scores_api(request, prospection_id):
    try:
        prospections = Prospection.objects.get(id=prospection_id)
        # Charger le modèle de machine learning préalablement enregistré
        model = joblib.load('C:/Users/HKWX2191/Music/project_django/web/appweb/model_dev.joblib')
        # Prédire le score en utilisant les caractéristiques du client
        for prospection in prospections:
            features = [prospection.Product.groupname, prospection.upfront, prospection.Product.unlock, prospection.Client.gendes, prospection.Client.age, prospection.Client.occupation, prospection.Client.langue, prospection.Client.region]
            predicted_score = model.predict([features])[0]
            predicted_score.save()
        return Response({'prospection_id': prospection_id, 'predicted_score': predicted_score}, status=status.HTTP_200_OK)
    except Client.DoesNotExist:
        return Response({'message': 'Client non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class enregistrer_client_api(APIView):
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            serializer = ClientSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class list_produit_api(ListAPIView):
    def get(self, request):
        products = Product.objects.all()
        serialized_products = [{'groupname': product.groupname, 'unlock': product.unlock} for product in products]
        return Response(serialized_products)
 

class list_clients_api(ListAPIView):
    def get(self, request):
        clients = Client.objects.all()
        serialized_clients = [{'nom': client.nom, 'prenom': client.prenom, 'telephone':client.telephone, 'gender':client.gender, 'age':client.age, 'occupation':client.occupation, 'langue':client.langue, 'region':client.region} for client in clients]
        return Response(serialized_clients)
        
    
class list_Prospection_api(ListAPIView):
    def get(self, request):
        prospections = Prospection.objects.filter(client__user=request.user)

        ProspectionSerializer = [{'nom': prospection.nom, 'prenom': prospection.prenom, 'telephone':prospection.telephone, 'gender':prospection.gender, 'age':prospection.age, 'occupation':prospection.client.occupation, 'langue':client.langue, 'region':client.region} for prospection in prospections]
        return Response(ProspectionSerializer)    

@login_required
def voir_scores_web(request, prospection_id):
    prospections = Prospection.objects.get(id=prospection_id)
    # Charger le modèle de machine learning préalablement enregistré
    model = joblib.load('C:/Users/HKWX2191/Music/project_django/web/appweb/model_dev.joblib')
    # Prédire le score en utilisant les caractéristiques du client
    for prospection in prospections:
        features = [prospection.Product.name, prospection.upfont_price, prospection.Product.price, prospection.Client.genre, prospection.Client.age, prospection.Client.profession, prospection.Client.Langue, prospection.Client.region]
        predicted_score = model.predict([features])[0]
        predicted_score.save()
        return render(request, 'voir_scores.html', {'prospection': prospection, 'predicted_score': predicted_score})



class UserLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # serializer = ConnexionSerializer(data=request.data)
    # if serializer.is_valid():
    #     username = serializer.validated_data['username']
    #     password = serializer.validated_data['password']
    #     user = authenticate(request, username=username, password=password)    
    #     if user is not None:
    #         if user.is_active:
    #             return Response({'message': 'Connexion réussie'})
    #         else:
    #             return Response({'message':'Utilisateur non actif' })
    #     else:
    #         return Response({'message': 'Identifiants invalides'}, status=400)
    # else:
    #     return Response(serializer.errors, status=400)




def enregistrer_commercial(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        try:
            user = User.objects.create_commercial_user(
                username=username,
                nom=nom,
                prenom=prenom,
                password=password,  # Vous n'avez pas besoin de créer un hash du mot de passe ici, Django le fera automatiquement.
                telephone=telephone,
            )
            user.save()

            return redirect('index')
        except IntegrityError:
            error_message = "Nom d'utilisateur déjà utilisé"
            form = CommercialUserCreationForm()
            return render(request, 'register.html', {'form': form, 'error_message': error_message})

    else:
        form = CommercialUserCreationForm()
        return render(request, 'register.html', {'form': form})


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Assurez-vous que le commercial est authentifié
def api_changer_mot_de_passe_commercial(request):
    if request.method == 'POST':
        serializer = ChangerMotDePasseSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            ancien_mot_de_passe = serializer.validated_data['ancien_mot_de_passe']
            nouveau_mot_de_passe = serializer.validated_data['nouveau_mot_de_passe']
            if user.check_password(ancien_mot_de_passe):
                user.set_password(nouveau_mot_de_passe)
                user.save()
                return Response({'message': 'Mot de passe mis à jour avec succès'})
            else:
                return Response({'message': 'Ancien mot de passe incorrect'}, status=400)
        else:
            return Response(serializer.errors, status=400)
        



def enregistrer_administrateur(request):
    form = AdministrateurUserCreationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        # Autres champs à récupérer    
        # if not User.objects.filter(username=username).exists():
        try:
            user = User.objects.create_user(
                username=username,
                nom=nom,
                prenom=prenom,
                password=make_password(password),
                telephone=telephone,
                is_administrateur=True
            )
        # Enregistrez cette instance dans la base de données
            user.save()
        # Créez une instance de Commercial liée à cet utilisateur
            administrateur = administrateur(user=user)
        # Enregistrez l'instance Commercial dans la base de données
            administrateur.save()
            return redirect('index')  # Rediriger vers une page appropriée
        except IntegrityError:
            error_message = "Nom d\'utilisateur déjà utilisé"
            form = AdministrateurUserCreationForm()
            return render(request, 'registerAdmin.html', {'form': form, 'error_message': error_message})

    else:
        form = AdministrateurUserCreationForm()
        return render(request, 'registerAdmin.html', {'form': form})
    

def enregistrer_super_administrateur(request):
    form = superadminUserCreationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        # Autres champs à récupérer    
        # if not User.objects.filter(username=username).exists():
        try:
            user = User.objects.create_superuser(
                username=username,
                nom=nom,
                prenom=prenom,
                password=make_password(password),
                telephone=telephone,
            )
        # Enregistrez cette instance dans la base de données
            user.save()
        # Créez une instance de Commercial liée à cet utilisateur
            superadministrateur = superadministrateur(user=user)
        # Enregistrez l'instance Commercial dans la base de données
            superadministrateur.save()
            return redirect('index')  # Rediriger vers une page appropriée
        except IntegrityError:
            error_message = "Nom d\'utilisateur déjà utilisé"
            form = superadminUserCreationForm()
            return render(request, 'registerAdmin.html', {'form': form, 'error_message': error_message})

    else:
        form = superadminUserCreationForm()
        return render(request, 'registerAdmin.html', {'form': form})  
    
      
def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Utilisez des parenthèses ()
        password = request.POST.get('password')  # Utilisez des parenthèses ()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return redirect('login')
    else:
        return redirect('login')
  
def add_product(request):
    form = ProductForm(request.POST)
    if request.method == 'POST':
        groupname = request.POST.get('groupname')
        unlock = request.POST.get('unlock')
        donnee = Product.objects.create(groupname=groupname, unlock=unlock)
        donnee.save()
        return redirect('product_list')  # Redirigez vers la liste des produits après l'ajout
    else:
        form = ProductForm()
    return render(request, 'enregistreProduit.html', {'form': form})



def client_list(request):
    clients =Client.objects.all()  # Récupérez tous les produits
    return render(request, 'client_list.html', {'clients': clients})


def profil_list(request):
    profils = Profil.objects.all()  # Récupérez tous les produits
    return render(request, 'profil_list.html', {'profils': profils})

def profil_detail(request, pk):
    profil = get_object_or_404(Profil, pk=pk)
    return render(request, 'profil_detail.html', {'profil': profil})

def delete_profil(request, pk):
    profil = get_object_or_404(Profil, pk=pk)
    if request.method == 'POST':
        profil.delete()
        return redirect('profil_list')
    return render(request, 'confirm_delete_profil.html', {'profil': profil})

def update_profil(request, pk):
    profil = get_object_or_404(Profil, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=profil) 
        if form.is_valid():
            form.save()
            return redirect('profil_list')
        else:
            return redirect('index')
    else:
        form = ProductForm(instance=profil)
    return render(request, 'profil_form.html', {'form': form, 'profil': profil})




def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'confirm_delete_product.html', {'product': product})

def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product) 
        if form.is_valid():
            form.save()
            return redirect('product_list')
        else:
            return redirect('index')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form, 'product': product})

def total_clients(request):
    total = Client.objects.count()
    return render(request, 'index.html', {'total_clients': total})

def index(request):
    return render(request, 'index.html', {'index' : index})


def bon_score(request):
    return render(request, 'bon_score.html', {'bon_score' : bon_score})  


def mauvais_score(request):
    return render(request, 'mauvais_score.html', {'mauvais_score' : mauvais_score}) 



def register(request):
    if request.method == 'POST':
        form = CompteForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            is_active = form.cleaned_data.get('is_active')
            user.is_active = is_active
            user.save()
            return redirect ('ProfilView')
    else:
        form = CompteForm()
    return render(request,'register.html', {"form":form})

def ProfilView(request):
    if request.method == "POST":
        form = ProfilForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProfilForm()

    return render(request, 'registerProfil.html', {'form': form})

    # form = ProfilForm()
    # if request.method == "POST":
    #     nom = request.POST.get('nom')
    #     prenom = request.POST.get('prenom')
    #     telephone = request.POST.get('telephone')
    #     role = request.POST.get('role')
    #     is_active = request.POST.get('is_active')
    #     users = User.objects.all()
    #     donnee = Profil.objects.create(nom=nom, prenom=prenom, telephone=telephone,
    #     role = role, is_active=is_active, users=users)

    #     donnee.save()

    #     return redirect ('tableau_de_bord')

    # else:
    #    return render(request, 'registerProfil.html', {'form':form})



User = get_user_model()

@csrf_exempt
def request_password_reset(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data['email']
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f'https://votre-app.com/reset-password/{uid}/{token}/'

            # Envoyez un e-mail à l'utilisateur avec le lien de réinitialisation
            send_mail(
                'Réinitialisation de mot de passe',
                f'Pour réinitialiser votre mot de passe, veuillez cliquer sur le lien suivant : {reset_url}',
                'votre-email@example.com',
                [email],
                fail_silently=False,
            )

            return JsonResponse({'message': 'Un e-mail de réinitialisation a été envoyé.'})

        except User.DoesNotExist:
            return JsonResponse({'error': 'Aucun utilisateur avec cette adresse e-mail.'})

    return JsonResponse({'error': 'Méthode non autorisée.'})




# ide = 0 
# @api_view(['POST']) 
# def verifeLogin(request): 
#         data = json.loads(request.body) 
#         userName = data.get('nomUtisateur') 
#         mdp = data.get('motDePass') 
#         a = Client.objects.get(nomUtisateur=userName) 
#         global ide 
#         ide = a.id 
#         try: 
  
#             if a.motDePass == mdp: 
#                 response_data = {'success': True, 'message': 'Modèle enregistré avec succès.'} 
#                 return JsonResponse(response_data, status=201) 
#          except: 
#              print(userName) 
#              print(mdp) 
#              print(a.nom) 
#              response_data = {'success': True, 'message': 'Modèle enregistré avec succès.'} 
#              return JsonResponse(response_data, status = 400) 
  
  
#  @api_view(['POST']) 
#  def createClient(request): 
#      serializer = ClientSerializer(data=request.data) 
#      if serializer.is_valid(): 
#          serializer.save() 
#          print('YES') 
#          return Response(serializer.data, status=201) 
#      print('NON') 
#      print(serializer.errors) 
#      return Response(serializer.errors, status=400) 
  
#  @api_view(['POST']) 
#  def createCourier(request): 
#      serializer = CourierSerializer(data=request.data) 
#      if serializer.is_valid(): 
#          serializer.save() 
#          print('YES') 
#          return Response(serializer.data, status=201) 
#      print('NON') 
#      print(serializer.errors) 
#      return Response(serializer.errors, status=400) 
#  class VoyageList(generics.ListAPIView): 
#      queryset = Voyages.objects.all() 
#      serializer_class = VoyagesSerializer 
  
#  @api_view(['POST']) 
#  def createReserve(request): 
#      serializer = ReserveSerializer(data=request.data) 
#      if serializer.is_valid(): 
#          donnees = request.data 
  
#          serializer.save() 
#          print('YES') 
  
#          villeDepar = donnees.get('villeDepart') 
#          villeArriv = donnees.get('villeArrive') 
#          print(villeDepar + ' '+villeArriv) 
#          dateReservation=donnees.get('dateReservation') 
#          voyage = Voyages.objects.get(ville_depart=villeDepar, ville_arrive=villeArriv) 
#          print(ide) 
#          client = Client.objects.get(id=ide) 
#          reservat = Reservation.objects.create(client=client, voyage=voyage, date=dateReservation) 
#          reservat.save() 
#          return Response(serializer.data, status=201) 
#      print('NON') 
#      print(serializer.errors) 
#      return Response(serializer.errors, status=400) 
  
#  @api_view(['POST']) 
#  def createReservePourUnePersonne(request): 
#      serializer = ReserveSerializer(data=request.data) 
#      if serializer.is_valid(): 
#          serializer.save() 
#          print('YES') 
#          donnees = request.data 
#          villeDepar = donnees.get('villeDepart') 
#          villeArriv = donnees.get('villeArrive') 
#          nomEtPrenom = donnees.get('NomEtPrenom') 
#          print(villeDepar + ' '+villeArriv) 
#          dateReservation=donnees.get('dateReservation') 
#          voyage = Voyages.objects.get(ville_depart=villeArriv, ville_arrive=villeDepar) 
#          print(ide) 
#          client = Client.objects.get(id=ide) 
#          reservat = Reservation.objects.create(client=client, voyage=voyage,  
#                                                date=dateReservation,  
#                                                NomEtPrenom=nomEtPrenom) 
#          reservat.save() 
#          return Response(serializer.data, status=201) 
#      print('NON') 
#      print(serializer.errors) 
#      return Response(serializer.errors, status=400) 
  
#  class ClientEnregistre(generics.RetrieveAPIView): 
#      queryset = Client.objects.all() 
#      serializer_class = ClientSerializer 
#      lookup_field ='id' 
  
#  class VilleList(generics.ListAPIView): 
#      queryset = Ville.objects.all() 
#      serializer_class = VilleSerializer 
  
#  def profile(request): 
#      return redirect('profile', ide) 
  
#  @login_required 
#  def home(request): 
#      clientcount = Client.objects.count() 
#      couriercount = Courier.objects.filter(Q(validerArrive=False)| Q(validerPris=False)).count() 
#      couriertotal = Courier.objects.all().count() 
#      courierArriver = Courier.objects.filter(validerArrive = True).count() 
#      courierPris = Courier.objects.filter(validerPris=True).count() 
#      Voyagescount = Voyages.objects.count() 
#      reservationcount = Reservation.objects.filter(valider_reservation=False).count() 
#      reservationtotal = Reservation.objects.all().count() 
  
  
#      return render(request, 'admin_t/homeAdmin.html',{ 
#                      'nombreClient': clientcount, 'nombreCourier': couriercount, 
#                      'nombreVoyages': Voyagescount, 'nombreReservation': reservationcount, 
#                      'couriertotal':couriertotal, 'courierArriver':courierArriver, 
#                      'courierPris':courierPris, 'reservationtotal':reservationtotal, 
  
#                      } 
#                    ) 
  
  
#  @login_required 
#  def client(request, id=0): 
  
#      if 'editClient' in request.path and id != 0 : 
  
#          model = get_object_or_404(Client, pk=id) 
#          if request.method == 'POST': 
#              form = ClientForm(request.POST, instance=model) 
#              if form.is_valid(): 
#                  form.save() 
#                  return redirect('client') 
#              else: 
#                  form = ClientForm(instance=model) 
#                  return render(request, 'admin_t/client.html', {"form": form}) 
#          form = ClientForm(instance=model) 
#          return render(request, 'admin_t/client.html', {"form": form, 'id':id}) 
  
#      elif 'deleteClient' in request.path and id != 0: 
#          ob = get_object_or_404(Client, id=id) 
#          ob.delete() 
#          return redirect('client') 
  
#      else: 
  
  
#          if request.method == "POST" and 'addClient' in request.path: 
#              form = ClientForm(request.POST) 
#              visit = Client.objects.all() 
#              page = Paginator(visit, 5) 
#              pge = request.GET.get('page') 
#              client = page.get_page(pge) 
#              if form.is_valid(): 
#                  form.save() 
#                  messages.success(request, "Client added !") 
#                  return redirect('client') 
#              else: 
#                  return render(request, 'admin_t/client.html', {"form": form, "models":client}) 
#          else: 
#              form = ClientForm() 
#              visit = Client.objects.all() 
#              page = Paginator(visit, 5) 
#              pge = request.GET.get('page') 
#              client = page.get_page(pge) 
#              return render(request, 'admin_t/client.html', {"form": form, "models":client}) 
  
  
#  @login_required 
#  def courier(request, id=0): 
  
#      if 'editCourier' in request.path and id != 0 : 
  
#          model = get_object_or_404(Courier, pk=id) 
#          if request.method == 'POST': 
#              form = CourierForm(request.POST, instance=model) 
#              if form.is_valid(): 
#                  form.save() 
#                  return redirect('courier') 
#              else: 
#                  form = CourierForm(instance=model) 
#                  return render(request, 'admin_t/courier.html', {"form": form}) 
#          form = CourierForm(instance=model) 
#          return render(request, 'admin_t/courier.html', {"form": form, 'id':id}) 
  
#      elif 'deleteCourier' in request.path and id != 0: 
#          ob = get_object_or_404(Courier, id=id) 
#          ob.delete() 
#          return redirect('courier') 
  
#      else: 
  
  
#          if request.method == "POST" and 'addCourier' in request.path: 
#              form = CourierForm(request.POST) 
#              visit = Courier.objects.all() 
#              page = Paginator(visit, 5) 
#              pge = request.GET.get('page') 
#              courier = page.get_page(pge) 
#              if form.is_valid(): 
#                  form.save() 
#                  messages.success(request, "Courier added !") 
#                  return redirect('courier') 
#              else: 
#                  return render(request, 'admin_t/courier.html', {"form": form, "models":courier}) 
#          else: 
#              form = CourierForm() 
#              visit = Courier.objects.all() 
#              page = Paginator(visit, 5) 
#              pge = request.GET.get('page') 
#              courier = page.get_page(pge) 
#              return render(request, 'admin_t/courier.html', {"form": form, "models":courier}) 
  
  
  
#  @login_required 
#  def car(request, id=0): 
  
#      if 'editCar' in request.path and id != 0 : 
  
#          model = get_object_or_404(Car, pk=id) 
#          if request.method == 'POST': 
#              form = CarForm(request.POST, instance=model) 
#              if form.is_valid(): 
#                  form.save() 
#                  return redirect('car') 
#              else: 
#                  form = CarForm(instance=model) 
#                  return render(request, 'admin_t/car.html', {"form": form}) 
#          form = CarForm(instance=model) 
#          return render(request, 'admin_t/car.html', {"form": form, 'id':id}) 
  
#      elif 'deleteCar' in request.path and id != 0: 
#          ob = get_object_or_404(Car, id=id) 
#          ob.delete() 
#          return redirect('car') 
  
#      else: 
  
  
#          if request.method == "POST" and 'addCar' in request.path: 
#              form = CarForm(request.POST) 
#              visit = Car.objects.all() 
#              page = Paginator(visit, 5) 
#              pge = request.GET.get('page') 
#              car = page.get_page(pge) 
#              if form.is_valid(): 
#                  form.save() 
#                  messages.success(request, "car added !") 
#                  return redirect('car') 
#              else: 
#                  return render(request, 'admin_t/car.html', {"form": form, "models":car}) 
#          else: 
#              form = CarForm() 
#              visit = Car.objects.all() 
#              page = Paginator(visit, 5) 
#              pge = request.GET.get('page') 
#              car = page.get_page(pge) 
#              return render(request, 'admin_t/car.html', {"form": form, "models":car}) 
  
#  def validerReservation(request, id): 
#      valider = get_object_or_404(Reservation, id=id) 
#      valider.valider_reservation = True 
#      valider.save() 
#      return redirect('reservation') 
  
  
#  def validerCourier(request, id): 
#      courier = get_object_or_404(Courier, id=id) 
#      if 'Arrive' in request.path: 
#          courier.validerArrive = True 
#      elif 'Pris' in request.path: 
#          courier.validerPris = True 
#      courier.save() 
#      return redirect('courier') 
  
#  @login_required 
#  def voyage(request, id=0): 
  
#      if 'editVoyage' in request.path and id != 0 : 
  
#          model = get_object_or_404(Voyages, pk=id) 
#          if request.method == 'POST': 
#              form = VoyagesForm(request.POST, instance=model) 
#              if form.is_valid(): 
#                  form.save() 
#                  return redirect('voyage') 
#              else: 
#                  form = VoyagesForm(instance=model) 
#                  return render(request, 'admin_t/voyage.html', {"form": form}) 
#          form = VoyagesForm(instance=model) 
#          return render(request, 'admin_t/voyage.html', {"form": form, 'id':id}) 
  
#      elif 'deleteVoyage' in request.path and id != 0: 
#          ob = get_object_or_404(Voyages, id=id) 
#          ob.delete() 
#          return redirect('voyage') 
  
#      else: 
  
  
#          if request.method == "POST" and 'addVoyage' in request.path: 
#              form = VoyagesForm(request.POST) 
#              visit = Voyages.objects.all() 
#              page = Paginator(visit, 5) 
#              pge = request.GET.get('page') 
#              voyage = page.get_page(pge) 
#              if form.is_valid(): 
#                  form.save() 
#                  messages.success(request, "voyage added !") 
#                  return redirect('voyage') 
#              else: 
#                  return render(request, 'admin_t/voyage.html', {"form": form, "models":voyage}) 
#          else: 
#              form = VoyagesForm() 
#              visit = Voyages.objects.all() 
#              page = Paginator(visit, 5) 
#              pge = request.GET.get('page') 
#              voyage = page.get_page(pge) 
#              return render(request, 'admin_t/voyage.html', {"form": form, "models":voyage}) 
  
#  @login_required 
#  def reservation(request, id=0): 
  
#      if 'editReservation' in request.path and id != 0 : 
  
#          model = get_object_or_404(Reservation, pk=id) 
#          if request.method == 'POST': 
#              form = ReservationForm(request.POST, instance=model) 
#              if form.is_valid(): 
#                  form.save() 
#                  return redirect('reservation') 
#              else: 
#                  form = ReservationForm(instance=model) 
#                  return render(request, 'admin_t/reservation.html', {"form": form}) 
#          form = ReservationForm(instance=model) 
#          return render(request, 'admin_t/reservation.html', {"form": form, 'id':id}) 
  
#      elif 'deleteReservation' in request.path and id != 0: 
#          ob = get_object_or_404(Reservation, pk=id) 
#          ob.delete() 
#          return redirect('reservation') 
  
#      else: 
  
  
#          if request.method == "POST" and 'addReservation' in request.path: 
  
#              form = ReservationForm(request.POST) 
#              visit = Reservation.objects.all() 
#              page = Paginator(visit, 5) 
#              pge = request.GET.get('page') 
#              reservation = page.get_page(pge) 
#              if form.is_valid(): 
  
#                  try: 
#                      b = form.cleaned_data['date'] 
#                      a = Place.objects.get(date=b) 
#                      if a.disponibilite: 
#                          form.save() 
#                          messages.success(request, "Reservation added !") 
#                          return redirect('reservation') 
#                      else: 
#                          return HttpResponse("Vous ne pouvez plus reserver car il n'y a plus de place disponibles a cette date") 
#                  except: 
#                      form.save() 
#                      messages.success(request, "Reservation added !") 
#                      return redirect('reservation') 
#              else: 
#                  return render(request, 'admin_t/reservation.html', {"form": form, "models":reservation}) 
#          else: 
#              form = ReservationForm() 
#              visit = Reservation.objects.all() 
#              page = Paginator(visit, 5) 
#              pge = request.GET.get('page') 
#              reservation = page.get_page(pge) 
#              return render(request, 'admin_t/reservation.html', {"form": form, "models":reservation})





# import 'package:flutter/material.dart';

# class ResetPasswordScreen extends StatelessWidget {
#   final TextEditingController newPasswordController = TextEditingController();

#   void resetPassword(String newPassword) async {
#     // Appelez votre API Django pour mettre à jour le mot de passe
#     // en utilisant le nouveau mot de passe fourni par l'utilisateur.
#     // Assurez-vous de gérer correctement les erreurs et la réponse de l'API.
#   }

#   @override
#   Widget build(BuildContext context) {
#     return Scaffold(
#       appBar: AppBar(
#         title: Text('Réinitialisation de mot de passe'),
#       ),
#       body: Column(
#         children: [
#           TextField(
#             controller: newPasswordController,
#             obscureText: true,
#             decoration: InputDecoration(labelText: 'Nouveau mot de passe'),
#           ),
#           ElevatedButton(
#             onPressed: () => resetPassword(newPasswordController.text),
#             child: Text('Réinitialiser le mot de passe'),
#           ),
#         ],
#       ),
#     );
#   }
# }
