import json
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .room_manager import RoomManager


class GameConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.user_id = str(uuid.uuid4())  # 임시 user id

        self.group_name = f"room_{self.room_id}"
        self.manager = RoomManager.instance()

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        event = data.get("type")

        try:
            if event == "join":
                snapshot = await self.join_room()
                await self.broadcast(snapshot)

            elif event == "end_turn":
                snapshot = await self.end_turn()
                await self.broadcast(snapshot)

            elif event == "snapshot":
                snapshot = await self.get_snapshot()
                await self.send(
                    json.dumps({"type": "room_update", "payload": snapshot})
                )

            else:
                return

        except Exception as e:
            await self.send(json.dumps({"error": str(e)}))

    @sync_to_async
    def join_room(self):
        room = self.manager.create_room(self.room_id)
        room.add_player(self.user_id)
        return room.snapshot()

    @sync_to_async
    def end_turn(self):
        room = self.manager.get_room(self.room_id)
        if not room:
            raise ValueError("room not found")

        room.end_turn(self.user_id)
        return room.snapshot()

    @sync_to_async
    def get_snapshot(self):
        room = self.manager.get_room(self.room_id)
        if not room:
            raise ValueError("room not found")

        return room.snapshot()

    async def broadcast(self, snapshot):
        await self.channel_layer.group_send(
            self.group_name, {"type": "room_update", "snapshot": snapshot}
        )

    async def room_update(self, event):
        await self.send(
            json.dumps({"type": "room_update", "payload": event["snapshot"]})
        )
