from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib import messages  # Importer messages
from .models import Utilisateur
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'web/index.html', {'pseudo': request.user.username})

def login(request):
    return render(request, 'web/login.html')

def inscription(request):
    if request.method == 'POST':
        email_given = request.POST.get('email')
        nickname_given = request.POST.get('nickname')
        password_given = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Vérifier si les mots de passe correspondent
        if password_given != confirm_password:
            return HttpResponse('Mot de passes differents')

        # Créer un nouvel utilisateur et l'enregistrer dans la base de données
        utilisateur = Utilisateur(email=email_given, pseudo=nickname_given, password=password_given)
        utilisateur.save()

        # Ajouter un message de succès après l'inscription
        messages.success(request, 'Inscription réussie ! Vous pouvez vous connecter.')
        
        return render(request, 'web/index.html')

def connexion(request):
    if request.method == 'POST':
        email_given = request.POST.get('email')
        password_given = request.POST.get('password')

        utilisateur = Utilisateur.objects.filter(email=email_given).first()

        if not utilisateur:
            return HttpResponse('Utilisateur non trouvé.')
        if password_given != utilisateur.password:
            return HttpResponse('Mot de passe incorrect')

        return render(request, 'web/index.html')



def search_users(request):
    print("sffefef", flush=True)
    query = request.GET.get('q', '')
    if query:
        users = Utilisateur.objects.filter(pseudo__icontains=query)
        results = [{"pseudo": user.pseudo} for user in users]
    else:
        results = []
    return JsonResponse({"results": results})


