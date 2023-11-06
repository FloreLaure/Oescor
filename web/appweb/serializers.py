from rest_framework import serializers
from django.contrib.auth import get_user_model
import joblib
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from .models import  Client,Product,Prospection,Profil 
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'



class ProspectionSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(slug_field='nom', queryset=Client.objects.all())
    produit = serializers.SlugRelatedField(slug_field='groupname', queryset=Product.objects.all())
    

    class Meta:
        model = Prospection
        fields = '__all__'
     # Vous pouvez ajouter un champ 'predicted_score' si nécessaire
    predicted_score = serializers.IntegerField(read_only=True)
    
   


class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profil
        fields = '__all__'


class ScorePredictionSerializer(serializers.Serializer):
    client_id = serializers.IntegerField()
    predicted_score = serializers.FloatField()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ChangerMotDePasseSerializer(serializers.Serializer):
    ancien_mot_de_passe = serializers.CharField()
    nouveau_mot_de_passe = serializers.CharField()    

# class ProduitSerializer(serializers.ModelSerializer):
#     prospection = ProspectionSerializer(many=True, read_only=True)  # Spécifiez le sérialiseur pour les livres





