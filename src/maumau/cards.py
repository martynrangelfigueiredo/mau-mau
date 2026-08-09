from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum


class Suit(Enum):
    CLUBS = "♣"
    SPADES = "♠"
    HEARTS = "♥"
    DIAMONDS = "♦"


class Rank(Enum):
    SEVEN = ("7", 0)
    EIGHT = ("8", 0)
    NINE = ("9", 0)
    TEN = ("10", 0)
    JACK = ("J", 20)
    QUEEN = ("Q", 10)
    KING = ("K", 10)
    ACE = ("A", 11)

    def __init__(self, symbol: str, points: int) -> None:
        self.symbol = symbol
        self.points = points


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank

    def __str__(self) -> str:
        return f"{self.rank.symbol}{self.suit.value}"

    @property
    def points(self) -> int:
        return self.rank.points


# Power card ranks
DRAW_TWO_RANK = Rank.SEVEN
SKIP_RANK = Rank.EIGHT
REVERSE_RANK = Rank.ACE
WILD_RANK = Rank.JACK


class Deck:
    """A 32-card German/French deck (7 through Ace, 4 suits)."""

    def __init__(self) -> None:
        self._cards: list[Card] = [
            Card(suit, rank) for suit in Suit for rank in Rank
        ]
        random.shuffle(self._cards)

    def draw(self, n: int = 1) -> list[Card]:
        """Draw *n* cards from the top of the deck."""
        drawn: list[Card] = []
        for _ in range(n):
            if not self._cards:
                raise ValueError("Deck is empty")
            drawn.append(self._cards.pop())
        return drawn

    def add_to_bottom(self, card: Card) -> None:
        """Place a card back at the bottom of the deck."""
        self._cards.insert(0, card)

    def reshuffle_from_discard(self, discard_pile: list[Card]) -> None:
        """Refill the deck from the discard pile, keeping the top card."""
        if len(discard_pile) <= 1:
            raise ValueError("Not enough cards in discard pile to reshuffle")
        top_card = discard_pile.pop()
        self._cards = discard_pile[:]
        discard_pile.clear()
        discard_pile.append(top_card)
        random.shuffle(self._cards)

    def __len__(self) -> int:
        return len(self._cards)