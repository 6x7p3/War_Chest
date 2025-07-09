from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Hex:
    """A class representing a hexagonal tile on the board. In axial coordinates."""
    q: int #west-east axis
    r: int #northwest-southeast axis