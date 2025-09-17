"""Tests for the Board class and related functionality."""

import pytest
from warchest.core.board import BoardHexes, Board, Cell, Control
from warchest.core.hex import Hex


def test_board_hexes_initialization():
    """Test that the default board hexes are initialized correctly."""
    board_hexes = BoardHexes
    assert isinstance(board_hexes, frozenset)
    assert len(board_hexes) > 0  # Ensure there are hexes in the board

    # Check if all hexes are instances of Hex
    for hex_tile in board_hexes:
        assert isinstance(hex_tile, Hex)

    # Check if the center hex is included
    assert Hex(q=0, r=0) in board_hexes

    # check out of bounds hexes
    assert Hex(q=4, r=0) not in board_hexes


def test_cell_initialization():
    """Test that the Cell dataclass initializes correctly."""
    cell = Cell(stack=["Token1", "Token2"], control="A")
    assert isinstance(cell, Cell)
    assert cell.stack == ["Token1", "Token2"]
    assert cell.control == "A"


# ------------------------------------------------------------
# test board initialization
# ------------------------------------------------------------
def test_board_initialization():
    """Test that the Board initializes correctly with default and custom layouts."""
    board = Board()
    assert isinstance(board, Board)
    assert board._layout == Board.DefaultLayout
    assert isinstance(board._map, dict)
    assert len(board._map) == 0  # Initially, the map should be empty


def test_board_initialization_with_layout():
    """Test that the Board initializes correctly with a custom layout."""
    custom_layout = frozenset({Hex(q=0, r=0), Hex(q=1, r=1)})
    board = Board(layout=custom_layout)
    assert board._layout == custom_layout
    assert isinstance(board._map, dict)
    assert len(board._map) == 0  # Initially, the map should be empty


def test_board_init_with_stack_and_control():
    """Test that the Board initializes correctly with stacks and control."""
    hx = Hex(0, 0)
    initial = {hx: ["token1", "token2"]}
    control = {hx: Control.A}

    board = Board(initial=initial, control=control)

    assert board.control_of(hx) is Control.A
    assert board._map[hx].stack == ["token1", "token2"]


def test_board_init_with_pairs_duplicate_hex():
    """Test that the Board initializes correctly with pairs, including duplicates."""
    hx = Hex(1, -1)
    pairs = [(hx, "tokenA"), (hx, "tokenB")]

    board = Board(pairs=pairs)
    assert board._map[hx].stack == ["tokenA", "tokenB"]


def test_board_init_with_outbounds_hex():
    """Test that the Board raises ValueError when initialized with out-of-bounds hexes."""
    hx = Hex(5, 5)  # Out of bounds hex
    try:
        _ = Board(initial={hx: ["token"]})
    except ValueError as e:
        assert str(e) == "off-board coordinates: [Hex(q=5, r=5)]"
    else:
        assert False, "Expected ValueError for out-of-bounds hex, but none was raised."


def test_board_init_with_outbounds_control():
    """Test that the Board raises ValueError when initialized with out-of-bounds control."""
    hx = Hex(5, 5)  # Out of bounds hex
    try:
        _ = Board(control={hx: Control.A})
    except ValueError as e:
        assert str(e) == "off-board coordinates: [Hex(q=5, r=5)]"
    else:
        assert False, "Expected ValueError for out-of-bounds hex, but none was raised."


# ------------------------------------------------------------
# test board place method
# ------------------------------------------------------------
def test_board_place_and_remove():
    """Test that the Board's place and remove methods work correctly."""
    board = Board()
    hx = Hex(0, 0)
    board.place(hx, "token1")
    assert "token1" in board._map[hx].stack
    board.place(hx, "token2")
    assert "token2" in board._map[hx].stack
    assert len(board._map[hx].stack) == 2
    board.remove_top(hx)
    assert "token1" in board._map[hx].stack
    assert len(board._map[hx].stack) == 1
    board.remove_top(hx)
    assert len(board._map[hx].stack) == 0


# ------------------------------------------------------------
# test board get_token_at method
# ------------------------------------------------------------
def test_board_get_token_at():
    """Test that the Board's get_token_at method works correctly."""
    board = Board()
    hx = Hex(0, 0)
    assert board.get_token_at(hx) is None  # Initially empty

    board.place(hx, "token1")
    assert board.get_token_at(hx) == "token1"

    board.place(hx, "token2")
    assert board.get_token_at(hx) == "token2"  # Top token should be token2

    # Test out-of-bounds hex
    bad_hex = Hex(5, 5)
    with pytest.raises(ValueError):
        board.get_token_at(bad_hex)


# ------------------------------------------------------------
# test board control methods
# ------------------------------------------------------------
def test_board_control():
    """Test that the Board's control methods work correctly."""
    board = Board()
    hx = Hex(0, 0)

    # Set control
    board.set_control(hx, Control.A)
    assert board.control_of(hx) is Control.A

    # Change control
    board.set_control(hx, Control.B)
    assert board.control_of(hx) is Control.B

    # Remove control
    board.set_control(hx, Control.NEUTRAL)
    assert board.control_of(hx) is Control.NEUTRAL

    # Attempt to set control on an out-of-bounds hex
    bad_hex = Hex(5, 5)
    with pytest.raises(ValueError):
        board.set_control(bad_hex, Control.A)


# ------------------------------------------------------------
# test bound control methods
# ------------------------------------------------------------
def test_bound_control():
    """Test that the Board raises ValueError for out-of-bounds hexes."""
    board = Board()
    bad_hex = Hex(5, 5)

    with pytest.raises(ValueError):
        board.place(bad_hex, "Oops")

    with pytest.raises(ValueError):
        board.remove_top(bad_hex)

    with pytest.raises(ValueError):
        board.set_control(bad_hex, Control.A)
