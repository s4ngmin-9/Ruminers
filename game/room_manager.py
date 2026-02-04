from collections import defaultdict
from threading import Lock


class RoomManager:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self.rooms = {}
        self.room_lock = defaultdict(Lock)

    @classmethod
    def instance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls()
        return cls._instance

    def get_room(self, room_id):
        return self.rooms.get(room_id)

    def create_room(self, room_id):
        with self.room_lock[room_id]:
            if room_id not in self.rooms:
                self.rooms[room_id] = RoomState(room_id)
        return self.rooms[room_id]

    def remove_room(self, room_id):
        with self.room_lock[room_id]:
            self.rooms.pop(room_id, None)


# 아래에서 정의
from .room_state import RoomState
