import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

class WebConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['user'].id
        self.group_name = f"user_{self.user_id}"
        
        print(f"✅ Connexion WebSocket : Utilisateur {self.user_id} ajouté au groupe {self.group_name}")

        # On ajoute l'utilisateur à son groupe spécifique AVANT d'accepter la connexion
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # On accepte la connexion WebSocket
        await self.accept()

    async def receive(self, text_data):
        # Juste pour debugger
        data = json.loads(text_data)
        print(f"📩 Message reçu du client: {data}")

    async def disconnect(self, close_code):
        # Quand l'utilisateur se déconnecte, on le retire du groupe
        await self.channel_layer.group_discard(self.group_name, self.channel_name)


    async def update_lists(self, event):
        """Envoie une mise à jour de la liste d'amis au client."""
        await self.send(text_data=json.dumps({
            "type": "update_lists",
            "message": event.get("message", "Votre liste d'amis a été mise à jour.")
        }))