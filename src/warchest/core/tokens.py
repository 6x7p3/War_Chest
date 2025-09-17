"""Module defining the Token class and its factory methods."""

from dataclasses import dataclass
from typing import ClassVar
from warchest.core.enums import TokenType, Player, LocationType


@dataclass(frozen=True, slots=True)
class Token:
    """representation of one token"""

    id: int
    token_type: TokenType
    owner: Player
    location: LocationType

    _NEXT_ID: ClassVar[int] = 0

    # --------------------------------------------
    # create using factory methods
    # --------------------------------------------
    @classmethod
    def create(cls, token_type: TokenType, owner: Player) -> "Token":
        """create a new token with the given type and owner"""
        token = cls(cls._NEXT_ID, token_type, owner, LocationType.RESERVE)
        cls._NEXT_ID = cls._NEXT_ID + 1
        return token
