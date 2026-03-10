from apps.game.domain.deck import build_deck
from .player_state import PlayerState


class RoomState:
    MAX_PLAYERS = 4
    START_HAND_COUNT = 14

    def __init__(self, room_id):
        self.room_id = room_id
        self.players = []
        self.turn_index = 0
        self.started = False

        self.deck = []
        self.table_tiles = []

    # 플레이어 관리
    def add_player(self, user_id):
        if any(p.user_id == user_id for p in self.players):
            return

        if len(self.players) >= self.MAX_PLAYERS:
            raise ValueError("room full")

        self.players.append(PlayerState(user_id))

    def remove_player(self, user_id):
        idx = next(
            (i for i, p in enumerate(self.players) if p.user_id == user_id), None
        )
        if idx is None:
            return

        self.players.pop(idx)

        if not self.players:
            self.turn_index = 0
            self.started = False
            self.deck = []
            self.table_tiles = []
            return

        if idx < self.turn_index:
            self.turn_index -= 1

        self.turn_index %= len(self.players)

    # 게임 시작
    def start(self):
        if self.started:
            return

        if len(self.players) < 2:
            raise ValueError("not enough players")

        self.deck = build_deck()

        # 각 플레이어 14장 분배
        for player in self.players:
            player.hand_tiles = [self.deck.pop() for _ in range(self.START_HAND_COUNT)]

        self.turn_index = 0
        self.started = True

    # 턴 관련
    def current_player(self):
        if not self.players:
            return None
        return self.players[self.turn_index]

    def end_turn(self, user_id):
        player = self.current_player()

        if not player or player.user_id != user_id:
            raise ValueError("not your turn")

        self.turn_index = (self.turn_index + 1) % len(self.players)

    # 타일 관련
    def draw_tile(self, user_id):
        if not self.started:
            raise ValueError("game not started")

        player = self.current_player()

        if not player or player.user_id != user_id:
            raise ValueError("not your turn")

        if not self.deck:
            raise ValueError("deck empty")

        tile = self.deck.pop()
        player.hand_tiles.append(tile)
        return tile

    # 스냅샷
    def snapshot(self):
        return {
            "room_id": self.room_id,
            "started": self.started,
            "turn_user": self.current_player().user_id if self.players else None,
            "players": [
                {
                    "user_id": p.user_id,
                    "hand_count": len(p.hand_tiles),
                }
                for p in self.players
            ],
            "deck_count": len(self.deck),
        }
