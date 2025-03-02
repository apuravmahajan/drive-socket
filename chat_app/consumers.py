import json
from channels.generic.websocket import AsyncWebsocketConsumer

PRECONFIGURED_USERS = ["User1", "User2"]  # two preconfigured users User1 and User2

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "chatroom"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        # json data format: {"sender": "User1", "message": "Hello"}
        data = json.loads(text_data)
        sender = data.get("sender")

        if sender not in PRECONFIGURED_USERS:
            await self.send(text_data=json.dumps({"error": "Unauthorized user"}))
            return

        message = data.get("message")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender,
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"]
        }))
