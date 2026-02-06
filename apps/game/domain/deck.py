from enum import Enum
from dataclasses import dataclass


class Color(str, Enum):
    RED = "RED"
    BLUE = "BLUE"
    BLACK = "BLACK"
    YELLOW = "YELLOW"


@dataclass(frozen=True)
class Tile:
    tile_id: int
    number: int
    color: Color
