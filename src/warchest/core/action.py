"""Action classes to represent player actions in the game, such as moving tokens, attacking, and recruiting."""

from warchest.core.enums import LocationType
from warchest.core.tokens import Token
from warchest.core.hex import Hex


class Action:
    """Base class for all actions."""

    def __init__(self, player, **kwargs):
        self.player = player
        self.params = kwargs

    def is_valid(self, game_state):
        """
        base validation
        - is it the player's turn?
        - does the player have sufficient resources?
        """

        # check player's turn
        if game_state.get_current_player() != self.player:
            return False

        # Other generic checks can be added here

        # Specific action types will implement their own validation

        return True

    def apply(self, game_state):
        """dummy apply method to be overridden by subclasses"""


class MoveAction(Action):
    """Class to represent a move action."""

    def __init__(self, player, resource: Token, from_hex: Hex, to_hex: Hex):
        super().__init__(player, resource=resource, from_hex=from_hex, to_hex=to_hex)
        self.resource = resource
        self.from_hex = from_hex
        self.to_hex = to_hex

    def is_valid(self, game_state):
        """
        Validate the move action
        """

        # Parent validation
        if not super().is_valid(game_state):
            return False

        # check if token is at the place the token is the same as the resource
        if game_state.board.get_token_at(self.from_hex) != self.resource:
            return False

        # check if resource is in player's hand
        if self.resource.location != LocationType.HAND or self.resource.owner != self.player:
            return False

        # Check if valid distance
        if self.from_hex.distance(self.to_hex) != 1:  # move distance is 1
            return False

        return True

    def apply(self, game_state):
        # Move the token on the board
        game_state.board.move_token(self.from_hex, self.to_hex)
