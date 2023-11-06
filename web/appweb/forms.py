
from django import forms
from django.forms import Form
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput
from .models import Client,Product,User,Profil

class CompteForm(UserCreationForm):
    username = forms.CharField(
        label="",
        max_length=20,
        error_messages={
            'invalid': ("This value may contain only letters, numbers and "
                    "@/./+/-/_ characters.")},
        widget=forms.TextInput(attrs={'class': 'form-control',
                        'placeholder': 'Nom d\'utilisateur',

                                    'required': 'true',                         
        })
)  
    password1 = forms.CharField(
        label=(""),
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                        'placeholder': 'Mot de passe',

                                          'required': 'true',

        })

    )

    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe',
                                          'required': 'true',

        })
    )

    is_active = forms.BooleanField(
        label="Activer le compte",
        required=False,  # Pour permettre de laisser vide (désactivé)
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()

class ProfilForm(forms.ModelForm): 
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(profil__isnull=True),
        # User.objects.all(),
        label='Utilisateur',
        widget=forms.Select(attrs={'class': 'form-control'}),  # Ajoutez une classe CSS
    )
    class Meta:
        model = Profil
        fields='__all__'
   

# class UserForm(UserCreationForm):
#     class Meta:
#         model = Profil
#         fields = ['nom','prenom','telephone','role','user']
            

    
class CommercialUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajoutez une classe CSS personnalisée pour le champ d'erreur
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'custom-error-class' 

class AdministrateurUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajoutez une classe CSS personnalisée pour le champ d'erreur
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'custom-error-class' 

class superadminUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajoutez une classe CSS personnalisée pour le champ d'erreur
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'custom-error-class' 


class ClientForm(forms.ModelForm):
    produit = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        # User.objects.all(),
        label='Nom produit',
        widget=forms.Select(attrs={'class': 'form-control'}),  # Ajoutez une classe CSS
    )
    class Meta:
        model = Client
        fields='__all__'  

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

