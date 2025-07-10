from warchest.core.board import Hex, BoardHexes, Board, Cell, Control
import pytest


def test_hex_initialization():
    hex_tile = Hex(q=1, r=2)
    assert hex_tile.q == 1
    assert hex_tile.r == 2
    assert isinstance(hex_tile, Hex)


def test_hex_immutability():
    hex_tile = Hex(q=1, r=2)
    try:
        hex_tile.q = 3  # Attempt to modify q
    except AttributeError:
        pass  # Expected behavior, as Hex is frozen
    else:
        assert False, "Hex should be immutable, but was modified."

    try:
        hex_tile.r = 4  # Attempt to modify r
    except AttributeError:
        pass  # Expected behavior, as Hex is frozen
    else:
        assert False, "Hex should be immutable, but was modified."


def test_hex_move():
    hex_tile = Hex(q=1, r=2)
    new_hex = hex_tile.move("south")
    assert new_hex.q == 0
    assert new_hex.r == 1


def test_hex_distance():
    hex1 = Hex(q=0, r=0)
    hex2 = Hex(q=3, r=3)
    assert hex1.distance(hex2) == 3  # Distance should be 3 in axial coordinates

    hex3 = Hex(q=1, r=1)
    assert hex2.distance(hex3) == 2  # Distance should be 1 in axial coordinates


def test_board_hexes_initialization():
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
    cell = Cell(stack=["Token1", "Token2"], control="A")
    assert isinstance(cell, Cell)
    assert cell.stack == ["Token1", "Token2"]
    assert cell.control == "A"


# ------------------------------------------------------------
# test board initialization
# ------------------------------------------------------------
def test_board_initialization():
    board = Board()
    assert isinstance(board, Board)
    assert board._layout == Board.DefaultLayout
    assert isinstance(board._map, dict)
    assert len(board._map) == 0  # Initially, the map should be empty


def test_board_initialization_with_layout():
    custom_layout = frozenset({Hex(q=0, r=0), Hex(q=1, r=1)})
    board = Board(layout=custom_layout)
    assert board._layout == custom_layout
    assert isinstance(board._map, dict)
    assert len(board._map) == 0  # Initially, the map should be empty


def test_board_init_with_stack_and_control():
    hx = Hex(0, 0)
    initial = {hx: ["token1", "token2"]}
    control = {hx: Control.A}

    board = Board(initial=initial, control=control)

    assert board.control_of(hx) is Control.A
    assert board._map[hx].stack == ["token1", "token2"]


def test_board_init_with_pairs_duplicate_hex():
    hx = Hex(1, -1)
    pairs = [(hx, "tokenA"), (hx, "tokenB")]

    board = Board(pairs=pairs)
    assert board._map[hx].stack == ["tokenA", "tokenB"]


def test_board_init_with_outbounds_hex():
    hx = Hex(5, 5)  # Out of bounds hex
    try:
        board = Board(initial={hx: ["token"]})
    except ValueError as e:
        assert str(e) == "off-board coordinates: [Hex(q=5, r=5)]"
    else:
        assert False, "Expected ValueError for out-of-bounds hex, but none was raised."


def test_board_init_with_outbounds_control():
    hx = Hex(5, 5)  # Out of bounds hex
    try:
        board = Board(control={hx: Control.A})
    except ValueError as e:
        assert str(e) == "off-board coordinates: [Hex(q=5, r=5)]"
    else:
        assert False, "Expected ValueError for out-of-bounds hex, but none was raised."


# ------------------------------------------------------------
# test board place method
# ------------------------------------------------------------
def test_board_place_and_remove():
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
# test board control methods
# ------------------------------------------------------------
def test_board_control():
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
    board = Board()
    bad_hex = Hex(5, 5)

    with pytest.raises(ValueError):
        board.place(bad_hex, "Oops")

    with pytest.raises(ValueError):
        board.remove_top(bad_hex)

    with pytest.raises(ValueError):
        board.set_control(bad_hex, Control.A)
