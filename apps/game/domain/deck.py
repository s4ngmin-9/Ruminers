import random
from .tile import Tile, Color


class TileDeck:
    def __init__(self):
        self.tiles = self._generate()
        random.shuffle(self.tiles)

    def _generate(self):
        tiles = []
        tile_id = 0

        # 1~13 × 4색 × 2세트 = 104장
        for _ in range(2):
            for color in Color:
                for number in range(1, 14):
                    tiles.append(
                        Tile(
                            tile_id=tile_id,
                            number=number,
                            color=color,
                        )
                    )
                    tile_id += 1

        return tiles

    def draw(self):
        if not self.tiles:
            return None
        return self.tiles.pop()

    def remaining_count(self):
        return len(self.tiles)
