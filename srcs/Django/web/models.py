from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models import Q


class Utilisateur(AbstractUser):
    victory = models.IntegerField(default=0)

    def get_friends(self):
        """
        Retourne la liste des amis (demandes acceptées).
        """
        accepted_requests = FriendRequest.objects.filter(
            models.Q(from_user=self) | models.Q(to_user=self),
            status='accepted'
        )
        friends = set()
        for request in accepted_requests:
            if request.from_user == self:
                friends.add(request.to_user)  # Ajoute l'ami (to_user)
            else:
                friends.add(request.from_user)  # Ajoute l'ami (from_user)
        return friends

    def get_pending_requests(self):
        """
        Retourne les demandes en attente reçues par l'utilisateur.
        """
        pending_requests = FriendRequest.objects.filter(
            models.Q(from_user=self) | models.Q(to_user=self),
            status='pending'
        )
        friends = set()
        for request in pending_requests:
            if request.from_user == self:
                friends.add(request.to_user)  # Ajoute l'ami (to_user)
            else:
                friends.add(request.from_user)  # Ajoute l'ami (from_user)
        return friends


    def get_blocked_users(self):
        """
        Retourne la liste des utilisateurs bloqués par l'utilisateur.
        """
        blocked_requests = FriendRequest.objects.filter(
            from_user=self,
            status='blocked'
        )
        return [request.to_user for request in blocked_requests]


class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),  # En attente
        ('accepted', 'Accepted'),  # Acceptée
        ('rejected', 'Rejected'),  # Refusée
        ('blocked', 'Blocked'),  # Bloqué
    ]

    from_user = models.ForeignKey(
        'Utilisateur', 
        related_name='friend_requests_sent',  # Demandes envoyées
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        'Utilisateur', 
        related_name='friend_requests_received',  # Demandes reçues
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending'  # Par défaut, la demande est en attente
    )
    created_at = models.DateTimeField(default=timezone.now)  # Date de création

    class Meta:
        unique_together = ('from_user', 'to_user')  # Évite les doublons de demandes
        verbose_name_plural = "Friend Requests"  # Améliore l'affichage en admin

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.status})"

    @staticmethod
    def get_friendship_id(user1, user2):
        """Retourne l'ID de la relation entre deux utilisateurs ou None si inexistante"""
        return FriendRequest.objects.filter(
            Q(from_user=user1, to_user=user2) | Q(from_user=user2, to_user=user1)
        ).values_list("id", flat=True).first()
    