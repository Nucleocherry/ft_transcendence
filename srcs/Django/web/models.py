from django.db import models
from django.contrib.auth.models import AbstractUser



class Utilisateur(AbstractUser):
	victory = models.IntegerField(default=0)
	friends_list = models.ManyToManyField('self', blank=True)


