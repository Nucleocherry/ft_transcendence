from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),  # Route pour afficher la vue `home`
    path('login/', views.login, name='login'),  # Route pour afficher la vue `login`
    path('inscription/', views.inscription, name='inscription'), #Route pour commencer l'inscription
    path('connexion/', views.connexion, name='connexion'),


    path('search_users/', views.search_users, name='search_users'), #pour search bar

    path("send-friend-request/", views.send_friend_request, name="send_friend_request"), #pour la demande d'ami

    path("get-user-id/", views.get_user_id, name="get_user_id"), #pour recup l'id de la personne a ajouter selon son pseudo

	path("showFriendList/", views.showFriendList, name="showFriendList"), #pour recup la liste d'amis
	path("showFriendRequestList/", views.showFriendRequestList, name="showFriendRequestList"), #pour recup la liste de requete d'amis


]
