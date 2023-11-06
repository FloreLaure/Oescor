from django.contrib import admin

# Register your models here.
from .models import Client,Profil, Score, Commercial, Resultat, Prospection,Product


admin.site.register(Client)
admin.site.register(Score)
admin.site.register(Commercial)
admin.site.register(Resultat)
admin.site.register(Prospection)
admin.site.register(Product)
admin.site.register(Profil)




