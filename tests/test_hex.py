from warchest.core.hex import Hex


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


def test_hex_neighbours():
    hex_tile = Hex(q=1, r=2)
    new_hex = hex_tile.neighbours("south")
    assert new_hex.q == 0
    assert new_hex.r == 1


def test_hex_distance():
    hex1 = Hex(q=0, r=0)
    hex2 = Hex(q=3, r=3)
    assert hex1.distance(hex2) == 3  # Distance should be 3 in axial coordinates

    hex3 = Hex(q=1, r=1)
    assert hex2.distance(hex3) == 2  # Distance should be 1 in axial coordinates


def test_hex_ring():
    hex_tile = Hex(q=0, r=0)
    moves = list(hex_tile.ring(radius=1))
    expected_moves = [
        Hex(q=1, r=0),
        Hex(q=0, r=-1),
        Hex(q=-1, r=-1),
        Hex(q=-1, r=0),
        Hex(q=0, r=1),
        Hex(q=1, r=1),
    ]
    assert set(moves) == set(expected_moves)  # Check if all expected moves are generated


def test_hex_straight_ring():
    hex_tile = Hex(q=0, r=1)
    moves = list(hex_tile.straight_ring(radius=2))
    expected_moves = [
        Hex(q=0, r=-1),
        Hex(q=2, r=1),
        Hex(q=2, r=3),
        Hex(q=0, r=3),
        Hex(q=-2, r=1),
        Hex(q=-2, r=-1),
    ]
    assert set(moves) == set(expected_moves)  # Check if all expected moves are generated
