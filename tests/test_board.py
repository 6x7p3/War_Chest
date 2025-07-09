from warchest.core.board import Hex 

def test_hex_initialization():
    hex_tile = Hex(q=1, r=2)
    assert hex_tile.q == 1
    assert hex_tile.r == 2
    assert isinstance(hex_tile, Hex)