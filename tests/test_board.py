"""Tests for the Board class and related functionality."""

import pytest
from warchest.core.board import BoardHexes, Board, Cell, Control
from warchest.core.hex import Hex
from warchest.core.tokens import Token
from warchest.core.enums import TokenType, Player

# Shared variables used across multiple tests
CENTER_HEX = Hex(0, 0)
ADJACENT_HEX = Hex(0, 1)
OUT_OF_BOUNDS_HEX = Hex(5, 5)
CUSTOM_LAYOUT = frozenset({CENTER_HEX, Hex(1, 1)})


def test_board_hexes_initialization():
    """Verify the default board hexes are properly initialized."""
    board_hexes = BoardHexes
    assert isinstance(board_hexes, frozenset)
    assert len(board_hexes) > 0

    # Check if all hexes are instances of Hex
    for hex_tile in board_hexes:
        assert isinstance(hex_tile, Hex)

    # Check center hex inclusion and out of bounds exclusion
    assert CENTER_HEX in board_hexes
    assert OUT_OF_BOUNDS_HEX not in board_hexes


def test_cell_initialization():
    """Verify Cell dataclass initializes with correct values."""
    token1 = Token.create(TokenType.BLANK, Player.A)
    token2 = Token.create(TokenType.BLANK, Player.A)
    cell = Cell(stack=[token1, token2], control=Control.A)
    assert isinstance(cell, Cell)
    assert cell.stack == [token1, token2]
    assert cell.control == Control.A


def test_board_initialization():
    """Verify Board initializes with default layout."""
    board = Board()
    assert isinstance(board, Board)
    assert board._layout == Board.DefaultLayout
    assert isinstance(board._map, dict)
    assert len(board._map) == 0


def test_board_initialization_with_layout():
    """Verify Board initializes with custom layout."""
    board = Board(layout=CUSTOM_LAYOUT)
    assert board._layout == CUSTOM_LAYOUT
    assert isinstance(board._map, dict)
    assert len(board._map) == 0


def test_board_init_with_stack_and_control():
    """Verify Board initializes with stacks and control."""
    token1 = Token.create(TokenType.BLANK, Player.A)
    token2 = Token.create(TokenType.BLANK, Player.A)
    initial = {CENTER_HEX: [token1, token2]}
    control = {CENTER_HEX: Control.A}

    board = Board(initial=initial, control=control)

    assert board.control_of(CENTER_HEX) is Control.A
    assert board._map[CENTER_HEX].stack == [token1, token2]


def test_board_init_with_pairs_duplicate_hex():
    """Verify Board initializes with duplicate hex pairs."""
    hx = Hex(1, -1)
    tokenA = Token.create(TokenType.BLANK, Player.A)
    tokenB = Token.create(TokenType.BLANK, Player.B)
    pairs = [(hx, tokenA), (hx, tokenB)]

    board = Board(pairs=pairs)
    assert board._map[hx].stack == [tokenA, tokenB]


def test_board_init_with_outbounds_hex():
    """Verify ValueError is raised with out-of-bounds hexes."""
    token = Token.create(TokenType.BLANK, Player.A)
    try:
        _ = Board(initial={OUT_OF_BOUNDS_HEX: [token]})
    except ValueError as e:
        assert str(e) == "off-board coordinates: [Hex(q=5, r=5)]"
    else:
        assert False, "Expected ValueError for out-of-bounds hex, but none was raised."


def test_board_init_with_outbounds_control():
    """Verify ValueError is raised with out-of-bounds control."""
    try:
        _ = Board(control={OUT_OF_BOUNDS_HEX: Control.A})
    except ValueError as e:
        assert str(e) == "off-board coordinates: [Hex(q=5, r=5)]"
    else:
        assert False, "Expected ValueError for out-of-bounds hex, but none was raised."


def test_board_place_and_remove():
    """Verify place and remove methods work correctly."""
    board = Board()
    token1 = Token.create(TokenType.BLANK, Player.A)
    token2 = Token.create(TokenType.BLANK, Player.A)

    board.place(CENTER_HEX, token1)
    assert token1 in board._map[CENTER_HEX].stack

    board.place(CENTER_HEX, token2)
    assert token2 in board._map[CENTER_HEX].stack
    assert len(board._map[CENTER_HEX].stack) == 2

    board.remove_top(CENTER_HEX)
    assert token1 in board._map[CENTER_HEX].stack
    assert len(board._map[CENTER_HEX].stack) == 1

    board.remove_top(CENTER_HEX)
    assert len(board._map[CENTER_HEX].stack) == 0


def test_board_get_token_at():
    """Verify get_token_at method returns correct tokens."""
    board = Board()
    assert board.get_token_at(CENTER_HEX) is None  # Initially empty

    token1 = Token.create(TokenType.BLANK, Player.A)
    token2 = Token.create(TokenType.BLANK, Player.A)

    board.place(CENTER_HEX, token1)
    assert board.get_token_at(CENTER_HEX) == token1

    board.place(CENTER_HEX, token2)
    assert board.get_token_at(CENTER_HEX) == token2  # Top token should be token2

    # Test out-of-bounds hex
    with pytest.raises(ValueError):
        board.get_token_at(OUT_OF_BOUNDS_HEX)


def test_board_move_token():
    """Verify move_token method correctly relocates tokens."""
    board = Board()
    token = Token.create(TokenType.BLANK, Player.A)

    board.place(CENTER_HEX, token)
    board.move_token(CENTER_HEX, ADJACENT_HEX)
    assert board.get_token_at(ADJACENT_HEX) == token
    assert board.get_token_at(CENTER_HEX) is None


def test_board_move_token_stack():
    """Verify move_token method correctly relocates entire stacks."""
    board = Board()
    token1 = Token.create(TokenType.BLANK, Player.A)
    token2 = Token.create(TokenType.BLANK, Player.A)

    board.place(CENTER_HEX, token1)
    board.place(CENTER_HEX, token2)
    board.move_token(CENTER_HEX, ADJACENT_HEX)

    assert board.get_token_at(ADJACENT_HEX) == token2  # Top token should be token2
    assert board._map[ADJACENT_HEX].stack == [token1, token2]
    assert board.get_token_at(CENTER_HEX) is None

    # Test moving from an empty hex
    with pytest.raises(ValueError):
        board.move_token(CENTER_HEX, Hex(0, 2))

    # Test moving to a non-empty hex
    with pytest.raises(ValueError):
        board.move_token(ADJACENT_HEX, ADJACENT_HEX)


def test_board_control():
    """Verify control methods set and get control status correctly."""
    board = Board()

    # Set control
    board.set_control(CENTER_HEX, Control.A)
    assert board.control_of(CENTER_HEX) is Control.A

    # Change control
    board.set_control(CENTER_HEX, Control.B)
    assert board.control_of(CENTER_HEX) is Control.B

    # Remove control
    board.set_control(CENTER_HEX, Control.NEUTRAL)
    assert board.control_of(CENTER_HEX) is Control.NEUTRAL

    # Attempt to set control on an out-of-bounds hex
    with pytest.raises(ValueError):
        board.set_control(OUT_OF_BOUNDS_HEX, Control.A)


def test_bound_control():
    """Verify ValueError is raised for operations on out-of-bounds hexes."""
    board = Board()
    token = Token.create(TokenType.BLANK, Player.A)

    with pytest.raises(ValueError):
        board.place(OUT_OF_BOUNDS_HEX, token)

    with pytest.raises(ValueError):
        board.remove_top(OUT_OF_BOUNDS_HEX)

    with pytest.raises(ValueError):
        board.set_control(OUT_OF_BOUNDS_HEX, Control.A)
