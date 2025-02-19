from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib import messages  # Importer messages
from .models import Utilisateur
from django.shortcuts import get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from .models import FriendRequest
from django.db.models import Q
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@login_required
def home(request):
    utilisateur = request.user  # L'utilisateur connecté
    friends = utilisateur.get_friends()  # Utilise la méthode get_friends() pour récupérer les amis

    return render(request, 'web/index.html', {
        'nickname': utilisateur.username,  # Passe le pseudo de l'utilisateur
        'friends': friends,  # Passe la liste des amis au template
        'user_id': utilisateur.id  # Passe l'ID de l'utilisateur au template
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
        utilisateur = Utilisateur(email=email_given, username=nickname_given, password=hashed_password, victory=0, is_online=True)
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
        utilisateur.is_online = True
        utilisateur.save()
        return redirect('home')




def search_users(request):
    query = request.GET.get('q', '')  # Récupère le paramètre 'q' de la requête
    if query:
        users = Utilisateur.objects.filter(username__icontains=query)
    else:
        users = Utilisateur.objects.all()

    # Ajoute l'ID des utilisateurs dans la réponse
    user_data = [{"id": user.id, "username": user.username, "is_online": user.is_online} for user in users]
    
    return JsonResponse({"users": user_data})



#Gestion des demandes d'ami et autre fonctions social

@login_required
def get_user_id(request):
    username = request.GET.get("username")
    user = Utilisateur.objects.filter(username=username).first()

    if user:
        return JsonResponse({"success": True, "user_id": user.id})
    else:
        return JsonResponse({"success": False, "message": "Utilisateur introuvable"}, status=404)


@login_required
def send_friend_request(request):
    if request.method == "POST":
        to_user_id = request.POST.get("to_user_id")
        if not to_user_id:
            return JsonResponse(
                {"success": False, "message": "ID utilisateur manquant."}, status=400
            )

        from_user = request.user

        try:
            to_user = Utilisateur.objects.get(id=to_user_id)
            if from_user == to_user:
                return JsonResponse(
                    {"success": False, "message": "Vous ne pouvez pas vous ajouter vous-même."},
                    status=400,
                )

            existing_request = FriendRequest.objects.filter(
                Q(from_user=from_user, to_user=to_user)
                | Q(from_user=to_user, to_user=from_user)
            ).first()

            channel_layer = get_channel_layer()

            if existing_request:
                if existing_request.status == "pending":
                    if existing_request.from_user == from_user:
                        return JsonResponse(
                            {"success": False, "message": "Demande déjà envoyée."},
                            status=400,
                        )
                    else:
                        # L'autre utilisateur avait déjà envoyé une demande ; on l'accepte
                        existing_request.status = "accepted"
                        existing_request.save()

                        # Notifier les deux utilisateurs via WebSocket (consumer unique update_lists)
                        async_to_sync(channel_layer.group_send)(
                            f"user_{from_user.id}",
                            {
                                "type": "update_lists",
                                "message": "Votre liste d'amis a été mise à jour.",
                            },
                        )
                        async_to_sync(channel_layer.group_send)(
                            f"user_{to_user.id}",
                            {
                                "type": "update_lists",
                                "message": "Votre liste d'amis a été mise à jour.",
                            },
                        )

                        return JsonResponse(
                            {"success": True, "message": "Demande d'amis acceptée !"}
                        )

                return JsonResponse(
                    {"success": False, "message": "Demande déjà traitée."}, status=400
                )

            # Créer une nouvelle demande d'ami (statut "pending")
            FriendRequest.objects.create(from_user=from_user, to_user=to_user, status="pending")
            print(f"📢 WebSocket envoyé à {to_user.id} pour une demande d'ami")

            # Notifier les deux utilisateurs via WebSocket (consumer unique update_lists)
            async_to_sync(channel_layer.group_send)(
                f"user_{from_user.id}",
                {
                    "type": "update_lists",
                    "message": "Votre liste d'amis a été mise à jour.",
                },
            )
            async_to_sync(channel_layer.group_send)(
                f"user_{to_user.id}",
                {
                    "type": "update_lists",
                    "message": "Votre liste d'amis a été mise à jour.",
                },
            )

            return JsonResponse(
                {"success": True, "message": "Demande envoyée avec succès !"}
            )

        except Utilisateur.DoesNotExist:
            return JsonResponse(
                {"success": False, "message": "Utilisateur introuvable."}, status=404
            )

    return JsonResponse(
        {"success": False, "message": "Méthode non autorisée."}, status=405
    )


@login_required
def showFriendList(request):
    user = request.user  # Utilisateur actuellement connecté
    friends = user.get_friends()  # Appel de la méthode sur l'instance de l'utilisateur

    # Formater la liste des amis pour la réponse JSON
    friends_data = [{"id": friend.id, "username": friend.username} for friend in friends]

    return JsonResponse({"success": True, "friends": friends_data})

@login_required
def showFriendRequestList(request):
    user = request.user  # Utilisateur actuellement connecté
    friends = user.get_pending_requests()  # Appel de la méthode sur l'instance de l'utilisateur

    # Formater la liste des amis pour la réponse JSON
    friends_data = [{"id": friend.id, "username": friend.username} for friend in friends]

    return JsonResponse({"success": True, "friends": friends_data})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/login/') 