import random
from .tile import Tile, Color


class TileDeck:
    def __init__(self):
        self.tiles = self._generate()
        random.shuffle(self.tiles)

    def _generate(self):
        tiles = []
        tile_id = 0

        for color in Color:
            for number in range(1, 14):
                for _ in range(2):  # 루미큐브는 같은 타일 2개씩
                    tiles.append(Tile(tile_id, number, color))
                    tile_id += 1

        return tiles

    def draw(self):
        if not self.tiles:
            return None
        return self.tiles.pop()
