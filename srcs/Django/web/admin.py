from django.contrib import admin
from .models import Utilisateur

# Enregistrer le modèle User dans l'administration
@admin.register(Utilisateur)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pseudo', 'email', 'online_status', 'victories', 'elo')  # Afficher ces champs dans la liste
    search_fields = ('pseudo', 'email')  # Champs par lesquels on peut rechercher dans l'admin
    list_filter = ('online_status',)  # Ajouter un filtre pour le statut en ligne
    ordering = ('elo',)  # Trier par le score ELO par défaut
