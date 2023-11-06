from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from datetime import date
from datetime import datetime
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import DateTimeField
from django.utils import timezone
from django.utils.regex_helper import _lazy_re_compile
from django.utils.timezone import get_fixed_timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import Settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group,Permission
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.conf import settings

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    telephone = models.CharField(max_length=20)
    is_commercial='is_commercial'
    is_administrateur='is_administrateur'
    is_super='is_super'
    choix = ((is_super, 'is_super'),(is_commercial, 'is_commercial'),(is_administrateur, 'is_administrateur'))
    role = models.CharField(max_length=17,choices=choix,default=is_commercial, null=True)
    
    def __str__(self):
        return f"{self.nom} {self.prenom}"



class Product(models.Model):
    groupname = models.CharField(max_length=100,null=True)
    unlock = models.IntegerField()

    def __str__(self):
        return self.groupname
    
class Client(models.Model):
    Masculin='Masculin'
    Feminin='Feminin'
    choix1 = ((Masculin, 'Masculin'),(Feminin, 'Feminin'),)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    telephone = models.CharField(max_length=20)
    gender = models.CharField(max_length=8,choices=choix1, null=True)
    age = models.PositiveIntegerField()
    commerce='commerce'
    Informatique='Informatique'
    Armee='Armee'
    choix_profession = ((commerce, 'commerce'),(Informatique, 'Informatique'),(Armee, 'Armee'),)
    occupation = models.CharField(max_length=12,choices=choix_profession, null=True) 
     # à choisir dans une liste
    Peulh='Peulh'
    Moore='Moore'
    Dioula='Dioula'
    Anglais='Anglais'
    Francais='Francais'
    choix_langue = ((Peulh, 'Peulh'),(Moore, 'Moore'),(Dioula, 'Dioula'),(Anglais, 'Anglais'),(Francais, 'Francais'),)
    langue = models.CharField(max_length=8,choices=choix_langue, null=True) 
    CentreEST='Centre-EST'
    Centre='Centre'
    CentreOuest='Centre-Ouest'
    Nord='Nord'
    Sud='Sud'
    choix_region = ((CentreEST, 'Centre-EST'),(Centre, 'Centre'),(CentreOuest, 'Centre-Ouest'),(Nord, 'Nord'),(Sud, 'Sud'),) # à choisir dans une liste
    region = models.CharField(max_length=12,choices=choix_region, null=True)  

    def __str__(self):
        return f"{self.nom} {self.prenom}"


class Prospection(models.Model):
     # Utilisez settings.AUTH_USER_MODEL pour définir le modèle User par défaut
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)

    upfront = models.IntegerField()

     # Champ pour stocker le résultat de prédiction
    predicted_score = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Prospection {self.id} {self.client} {self.produit}"
    # def __str__(self):
    #     return f"{self.client} {self.produit}"


class Score(models.Model):
    Prospection = models.OneToOneField(Prospection, on_delete=models.CASCADE)
    score = models.BooleanField(default=False)
    

class Commercial(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clients_enregistres = models.ManyToManyField(Client)

class Resultat(models.Model):
    commercial = models.ForeignKey(Commercial, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    bon_score = models.BooleanField(default=False)

class Graphique(models.Model):
    type = models.CharField(max_length=100)
    url = models.URLField()



# Vous pouvez ajouter d'autres champs ou relations selon vos besoins






   