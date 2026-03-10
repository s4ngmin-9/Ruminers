class PlayerState:
    def __init__(self, user_id):
        self.user_id = user_id
        self.hand = []

    def add_tile(self, tile):
        self.hand.append(tile)

    def remove_tile(self, tile_id):
        self.hand = [t for t in self.hand if t.tile_id != tile_id]

    def snapshot(self):
        return {
            "user_id": self.user_id,
            "hand": [
                {
                    "tile_id": t.tile_id,
                    "number": t.number,
                    "color": t.color.value,
                }
                for t in self.hand
            ],
        }
