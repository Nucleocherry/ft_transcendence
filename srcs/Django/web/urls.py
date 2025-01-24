from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Route pour afficher la vue `home`
	path('login/', views.login, name='login'),  # Route pour afficher la vue `login`
	path('inscription/', views.inscription, name='inscription'), #Route pour commencer l'inscription
	path('connexion/', views.connexion, name='connexion'),


	path('search_users/', views.search_users, name='search_users'), #pour search bar

]

