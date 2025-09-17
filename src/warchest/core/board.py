"""Module defining the Board class and related functionality for managing the game board."""

from dataclasses import dataclass, field
from typing import Optional, Mapping, Union, Sequence, Iterable, FrozenSet, ClassVar
from collections import defaultdict
from warchest.core.enums import Control
from warchest.core.hex import Hex
from warchest.core.tokens import Token

# ----------------------------------------------------------------------
# the default board layout
# A set of all hexes on the board, representing the playable area.
# The board is a hexagonal grid with a radius of 3 hexes from the center
# 2 starting points each for both players, 6 neutral locations
# -----------------------------------------------------------------------
BoardHexes: frozenset[Hex] = frozenset(
    Hex(q, r) for q in range(-3, 4) for r in range(-3, 4) if Hex.distance(Hex(q, r), Hex(0, 0)) <= 3
)
AStartingLocations: frozenset[Hex] = frozenset([Hex(2, 4), Hex(3, 1)])
BStartingLocations: frozenset[Hex] = frozenset([Hex(-2, -4), Hex(-3, -1)])
NeutralLocations: frozenset[Hex] = frozenset(
    [
        Hex(0, -2),
        Hex(1, 0),
        Hex(2, 1),
        Hex(-2, -1),
        Hex(-1, 0),
        Hex(0, 2),
    ]
)


# --------------------------------------------------------------------------- #
# payload container
# --------------------------------------------------------------------------- #


@dataclass(slots=True)
class Cell:
    """Payload stored in Board._map: token stack + control flag."""

    stack: list["Token"] = field(default_factory=list)
    control: Control = Control.NEUTRAL

    # convenience
    def top(self) -> "Token | None":
        """Return the top token, or None if empty."""
        return self.stack[-1] if self.stack else None

    def size(self) -> int:
        """Return the number of tokens in the stack."""
        return len(self.stack)

    def copy(self) -> "Cell":
        """Return a shallow copy of the cell."""
        return Cell(stack=self.stack.copy(), control=self.control)


# --------------------------------------------------------------------------- #
# Board
# --------------------------------------------------------------------------- #
class Board:
    """Keeps board geometry **and** per-hex contents/status."""

    __slots__ = ("_layout", "_map")  # layout is the set of valid hexes; map is Hex -> Cell

    DefaultLayout: ClassVar[FrozenSet[Hex]] = BoardHexes

    def __init__(
        self,
        *,
        layout: Optional[FrozenSet[Hex]] = None,
        # two ways to initialize tokens on the board
        initial: Optional[Mapping[Hex, Union["Token", Sequence["Token"]]]] = None,
        pairs: Optional[Iterable[tuple[Hex, "Token"]]] = None,
        # control
        control: Optional[Mapping[Hex, Control]] = None,
    ) -> None:
        # 1 choose layout
        self._layout: FrozenSet[Hex] = layout or Board.DefaultLayout

        # 2 map  Hex → Cell
        self._map: dict[Hex, Cell] = defaultdict(Cell)

        # 3 load token stacks
        if initial:
            for hx, value in initial.items():
                cell = self._map[hx]
                if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
                    cell.stack.extend(value)
                else:
                    cell.stack.append(value)

        if pairs:
            for hx, token in pairs:
                self._map[hx].stack.append(token)

        # 4 load control info
        if control:
            for hx, ctrl in control.items():
                self._map[hx].control = ctrl

        # 5 validate
        bad = [hx for hx in self._map if hx not in self._layout]
        if bad:
            raise ValueError(f"off-board coordinates: {bad}")

    # ------------------------------------------------------------------ #
    # Public helpers
    # ------------------------------------------------------------------ #
    def get_token_at(self, hx: Hex) -> Optional["Token"]:
        """Return the top token at the given hex, or None if empty."""
        self._ensure_in_bounds(hx)
        cell = self._map.get(hx, Cell())
        return cell.top()

    def place(self, hx: Hex, token: "Token") -> None:
        """Place a token on top of the stack at the given hex."""
        self._ensure_in_bounds(hx)
        self._map[hx].stack.append(token)

    def remove_top(self, hx: Hex) -> "Token":
        """Remove and return the top token from the stack at the given hex."""
        self._ensure_in_bounds(hx)
        cell = self._map.get(hx, Cell())
        if not cell.stack:
            raise ValueError(f"No tokens at {hx}")
        top = cell.stack.pop()
        if not cell.stack and cell.control is Control.NEUTRAL:
            # keep map small: remove empty neutral cells
            self._map.pop(hx, None)
        return top

    def control_of(self, hx: Hex) -> Control:
        """Return the control status of the given hex."""
        self._ensure_in_bounds(hx)
        return self._map.get(hx, Cell()).control

    def set_control(self, hx: Hex, ctrl: Control) -> None:
        """Set the control status of the given hex."""
        self._ensure_in_bounds(hx)
        self._map[hx].control = ctrl

    # ------------------------------------------------------------------ #
    # Internal
    # ------------------------------------------------------------------ #
    def _ensure_in_bounds(self, hx: Hex) -> None:
        if hx not in self._layout:
            raise ValueError(f"{hx} is outside board bounds")

    # ------------------------------------------------------------------ #
    # Iteration / len / repr for testing & debugging
    # ------------------------------------------------------------------ #
    def __iter__(self):
        yield from self._map.items()

    def __len__(self) -> int:
        return len(self._map)

    def __repr__(self) -> str:  # compact, test-friendly
        return f"Board({dict(self._map)})"
