from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class Hex:
    """A class representing a hexagonal tile on the board. In tilted axial coordinates (q, r)."""

    q: int  # southwest-northeast axis
    r: int  # northwest-southeast axis
    _DIRECTIONS = {
        "north": (1, 1),
        "northeast": (1, 0),
        "southeast": (0, -1),
        "south": (-1, -1),
        "southwest": (-1, 0),
        "northwest": (0, 1),
    }

    def neighbours(self, direction: str) -> "Hex":
        """Returns a new Hex object moved in the specified direction."""
        if direction not in self._DIRECTIONS:
            raise ValueError(f"Invalid direction: {direction}")
        dq, dr = self._DIRECTIONS[direction]
        return Hex(self.q + dq, self.r + dr)

    def distance(self, other: "Hex") -> int:
        """Calculates the distance to another Hex object using the axial coordinate system."""
        dq = self.q - other.q
        dr = self.r - other.r
        if dq * dr < 0:
            return abs(dq) + abs(dr)
        return max(abs(dq), abs(dr))

    def ring(self, radius: int = 1) -> Iterable["Hex"]:
        """Generates all hexes within a given radius from this hex."""
        if radius < 0:
            raise ValueError("radius must be non-negative")

        for dq in range(-radius, radius + 1):
            for dr in range(-radius, radius + 1):
                if self.distance(Hex(self.q + dq, self.r + dr)) == radius:
                    yield Hex(self.q + dq, self.r + dr)

    def straight_ring(self, radius: int = 1) -> Iterable["Hex"]:
        """Generates all hexes in a straight line at a given radius from this hex."""
        if radius < 0:
            raise ValueError("radius must be non-negative")

        q0, r0 = self.q, self.r
        for dq, dr in self._DIRECTIONS.values():
            yield Hex(q0 + dq * radius, r0 + dr * radius)


h = Hex(0, 1)  # Example usage
print(list(h.straight_ring(2)))  # Should print hexes at radius 1 in all directions
