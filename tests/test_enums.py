from warchest.core.enums import Control, Player, TokenType


def test_control_enum():
    assert list(Control) == [Control.NEUTRAL, Control.A, Control.B]


def test_player_enum():
    assert list(Player) == [Player.A, Player.B]


def test_token_type_enum():
    assert list(TokenType) == [TokenType.BLANK]
