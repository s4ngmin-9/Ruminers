class PlayerState:
    def __init__(self, user_id):
        self.user_id = user_id


class RoomState:
    MAX_PLAYERS = 4

    def __init__(self, room_id):
        self.room_id = room_id
        self.players = []
        self.turn_index = 0
        self.started = False

    # 참여
    def add_player(self, user_id):
        if any(p.user_id == user_id for p in self.players):
            return

        if len(self.players) >= self.MAX_PLAYERS:
            raise ValueError("room full")

        self.players.append(PlayerState(user_id))

    # 퇴장
    def remove_player(self, user_id):
        idx = next((i for i, p in enumerate(self.players) if p.user_id == user_id), None)
        if idx is None:
            return

        self.players.pop(idx)

        if not self.players:
            self.turn_index = 0
            self.started = False
            return

        # 턴 보정
        if idx < self.turn_index:
            self.turn_index -= 1

        self.turn_index %= len(self.players)

    # 게임 시작
    def start(self):
        if len(self.players) < 2:
            raise ValueError("not enough players")

        self.started = True
        self.turn_index = 0

    # 턴
    def current_player(self):
        if not self.players:
            return None
        return self.players[self.turn_index]

    def end_turn(self, user_id):
        player = self.current_player()

        if not player or player.user_id != user_id:
            raise ValueError("not your turn")

        self.turn_index = (self.turn_index + 1) % len(self.players)

    # 스냅샷
    def snapshot(self):
        return {
            "room_id": self.room_id,
            "started": self.started,
            "turn_user": self.current_player().user_id if self.players else None,
            "players": [p.user_id for p in self.players],
        }
