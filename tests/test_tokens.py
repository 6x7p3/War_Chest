from warchest.core.tokens import Token
from warchest.core.enums import TokenType, Player


def test_token_creation():
    """Test the creation of a Token instance."""
    token1 = Token.create(TokenType.BLANK, Player.B)
    assert token1.id == 0
    assert token1.token_type == TokenType.BLANK
    assert token1.owner == Player.B

    token2 = Token.create(TokenType.BLANK, Player.A)
    assert token2.id == 1
    assert token2.token_type == TokenType.BLANK
    assert token2.owner == Player.A
