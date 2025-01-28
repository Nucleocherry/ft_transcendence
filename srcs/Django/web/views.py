from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib import messages  # Importer messages
from .models import Utilisateur
from django.shortcuts import get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


@login_required
def home(request):
    utilisateur = request.user  # L'utilisateur connecté
    amis = utilisateur.friends_list.all()  # Récupère tous les amis de l'utilisateur connecté

    return render(request, 'web/index.html', {
        'nickname': utilisateur.username,  # Passe le pseudo de l'utilisateur
        'amis': amis  # Passe la liste des amis au template
    })



def login(request):
    return render(request, 'web/login.html')

def inscription(request):
    if request.method == 'POST':
        email_given = request.POST.get('email')
        nickname_given = request.POST.get('nickname')  # Ici, nickname_given correspond à 'username'
        password_given = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Vérifier si les mots de passes correspondent
        if password_given != confirm_password:
            return HttpResponse('Les mots de passe sont différents.')

        # Crypter le mot de passe
        hashed_password = make_password(password_given)

        # Créer un nouvel utilisateur et l'enregistrer dans la base de données
        utilisateur = Utilisateur(email=email_given, username=nickname_given, password=hashed_password, victory=0)
        utilisateur.save()

        # Ajouter un message de succès après l'inscription
        messages.success(request, 'Inscription réussie ! Vous pouvez vous connecter.')
        auth_login(request, utilisateur)

        return redirect('home')




def connexion(request):
    if request.method == 'POST':
        email_given = request.POST.get('email')
        password_given = request.POST.get('password')

        # Trouver l'utilisateur par email
        utilisateur = Utilisateur.objects.filter(email=email_given).first()

        if not utilisateur:
            return HttpResponse('Utilisateur non trouvé.')

        if not check_password(password_given, utilisateur.password):
            return HttpResponse('Mot de passe incorrect.')

        # Connexion de l'utilisateur
        auth_login(request, utilisateur)

        return redirect('home')




def search_users(request):
    query = request.GET.get('q', '')  # Récupère le paramètre 'q' de la requête
    if query:
        users = Utilisateur.objects.filter(username__icontains=query)  # Filtrer les utilisateurs
    else:
        users = Utilisateur.objects.all()  # Si aucune recherche, récupère tous les utilisateurs

    user_data = [{"username": user.username} for user in users]
    return JsonResponse({"users": user_data})


