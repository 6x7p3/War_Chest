from enum import Enum, auto


class Control(Enum):
    """Who controls a hex on the board."""

    NEUTRAL = auto()
    A = auto()
    B = auto()


class Player(Enum):
    """Players in the game."""

    A = auto()
    B = auto()


class TokenType(Enum):
    """Types of tokens that can be placed on the board."""

    BLANK = auto()
