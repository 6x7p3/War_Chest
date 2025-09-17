"""Tests for the action module which implements game actions and their validation."""

from warchest.core.action import Action, MoveAction
from warchest.core.enums import LocationType, Player, TokenType
from warchest.core.tokens import Token
from warchest.core.hex import Hex
from warchest.core.board import Board


class DummyGameState:
    """Simplified game state implementation for testing."""

    def __init__(self, player, board):
        self._player = player
        self.board = board

    def get_current_player(self):
        """Return the current player."""
        return self._player


def test_action_turn_validation():
    """Test that basic action validation checks if it's the player's turn."""
    player = Player.A
    action = Action(player)
    board = Board()
    gs = DummyGameState(Player.B, board)
    assert not action.is_valid(gs)

    gs = DummyGameState(Player.A, board)
    assert action.is_valid(gs)


def test_moveaction_valid_move():
    """Test that a valid move passes validation and moves the token correctly."""
    player = Player.A
    token = Token.create(TokenType.BLANK, player)
    token = Token(token.id, token.token_type, player, LocationType.HAND)
    from_hex = Hex(0, 0)
    to_hex = Hex(0, 1)
    board = Board()
    board.place(from_hex, token)
    gs = DummyGameState(player, board)

    move = MoveAction(player, token, from_hex, to_hex)
    assert move.is_valid(gs)

    move.apply(gs)
    assert board.get_token_at(to_hex) == token
    assert board.get_token_at(from_hex) is None


def test_moveaction_invalid_not_player_turn():
    """Test that move validation fails when it's not the player's turn."""
    player = Player.A
    token = Token.create(TokenType.BLANK, player)
    token = Token(token.id, token.token_type, player, LocationType.HAND)
    from_hex = Hex(0, 0)
    to_hex = Hex(0, 1)
    board = Board()
    board.place(from_hex, token)
    gs = DummyGameState(Player.B, board)

    move = MoveAction(player, token, from_hex, to_hex)
    assert not move.is_valid(gs)


def test_moveaction_invalid_token_not_in_hand():
    """Test that move validation fails when token is not in player's hand."""
    player = Player.A
    token = Token.create(TokenType.BLANK, player)
    token = Token(token.id, token.token_type, player, LocationType.BOARD)  # Not in hand
    from_hex = Hex(0, 0)
    to_hex = Hex(0, 1)
    board = Board()
    board.place(from_hex, token)
    gs = DummyGameState(player, board)

    move = MoveAction(player, token, from_hex, to_hex)
    assert not move.is_valid(gs)


def test_moveaction_invalid_token_wrong_owner():
    """Test that move validation fails when token belongs to another player."""
    player = Player.A
    wrong_owner = Player.B
    token = Token.create(TokenType.BLANK, wrong_owner)
    token = Token(token.id, token.token_type, wrong_owner, LocationType.HAND)
    from_hex = Hex(0, 0)
    to_hex = Hex(0, 1)
    board = Board()
    board.place(from_hex, token)
    gs = DummyGameState(player, board)

    move = MoveAction(player, token, from_hex, to_hex)
    assert not move.is_valid(gs)


def test_moveaction_invalid_destination_occupied():
    """Test that move validation fails when destination hex is occupied."""
    player = Player.A
    token = Token.create(TokenType.BLANK, player)
    token = Token(token.id, token.token_type, player, LocationType.HAND)
    from_hex = Hex(0, 0)
    to_hex = Hex(0, 1)
    board = Board()
    board.place(from_hex, token)
    other_token = Token.create(TokenType.BLANK, player)
    board.place(to_hex, other_token)
    gs = DummyGameState(player, board)

    move = MoveAction(player, token, from_hex, to_hex)
    assert not move.is_valid(gs)


def test_moveaction_invalid_distance():
    """Test that move validation fails when distance is greater than 1 hex."""
    player = Player.A
    token = Token.create(TokenType.BLANK, player)
    token = Token(token.id, token.token_type, player, LocationType.HAND)
    from_hex = Hex(0, 0)
    to_hex = Hex(0, 2)  # Distance is 2
    board = Board()
    board.place(from_hex, token)
    gs = DummyGameState(player, board)

    move = MoveAction(player, token, from_hex, to_hex)
    assert not move.is_valid(gs)
