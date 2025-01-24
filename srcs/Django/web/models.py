from django.db import models


class Utilisateur(models.Model):
    pseudo = models.CharField(max_length=20, unique=True)  # Pseudo unique
    email = models.EmailField(unique=True)                 # Email unique
    password = models.CharField(max_length=255)

    online_status = models.BooleanField(default=False)     # Statut en ligne (True/False)
    victories = models.PositiveIntegerField(default=0)     # Nombre de victoires
    elo = models.PositiveIntegerField(default=1000)        # Score ELO initial à 1000

    friends_list = models.ManyToManyField('self', symmetrical=False, related_name='friends', blank=True)

    class Meta:
        db_table = 'web_user'  # Nom de la table dans la base de données

    def __str__(self):
        return self.pseudo

