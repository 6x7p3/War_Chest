"""Enumerations for the game, including player identifiers, token types, and location types."""

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


class LocationType(Enum):
    """Types of locations where tokens can be placed."""

    BOARD = auto()
    HAND = auto()
    RESERVE = auto()
    DEAD = auto()
    BAG = auto()
    DISCARD = auto()
