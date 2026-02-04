from threading import Lock

_rooms = {}
_lock = Lock()


def get_room(room_id: str):
    with _lock:
        return _rooms.get(room_id)


def create_room(room_id: str):
    with _lock:
        if room_id not in _rooms:
            _rooms[room_id] = {
                "players": [],
                "turn": 0,
                "status": "WAITING",
            }
        return _rooms[room_id]


def join_room(room_id: str, user_id: str):
    with _lock:
        room = _rooms.setdefault(room_id, {
            "players": [],
            "turn": 0,
            "status": "WAITING",
        })

        if user_id not in room["players"]:
            room["players"].append(user_id)

        return room


def next_turn(room_id: str):
    with _lock:
        room = _rooms.get(room_id)
        if not room or not room["players"]:
            return None

        room["turn"] = (room["turn"] + 1) % len(room["players"])
        return room
