from __future__ import annotations

from typing import Optional

from .cards import (
    Card,
    Deck,
    Rank,
    Suit,
    DRAW_TWO_RANK,
    SKIP_RANK,
    REVERSE_RANK,
    WILD_RANK,
)

WINNING_SCORE = 150
INITIAL_HAND_SIZE = 5


class Player:
    def __init__(self, name: str, is_human: bool = True) -> None:
        self.name = name
        self.is_human = is_human
        self.hand: list[Card] = []
        self.score: int = 0

    def hand_value(self) -> int:
        return sum(card.points for card in self.hand)

    def __str__(self) -> str:
        return self.name


class GameState:
    """Holds the mutable state of a single round."""

    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self.deck = Deck()
        self.discard_pile: list[Card] = []
        self.current_player_index: int = 0
        self.direction: int = 1  # 1 = clockwise, -1 = counter-clockwise
        self.draw_stack: int = 0   # accumulated draw-two penalty
        self.skip_next: bool = False
        self.declared_suit: Optional[Suit] = None  # after a Jack is played

        # Deal initial hands
        for player in self.players:
            player.hand = self.deck.draw(INITIAL_HAND_SIZE)

        # Flip first card (re-draw if it's a power card)
        first_card = self.deck.draw(1)[0]
        while first_card.rank in (DRAW_TWO_RANK, WILD_RANK):
            self.deck.add_to_bottom(first_card)
            first_card = self.deck.draw(1)[0]
        self.discard_pile.append(first_card)

    @property
    def top_card(self) -> Card:
        return self.discard_pile[-1]

    @property
    def current_player(self) -> Player:
        return self.players[self.current_player_index]

    def advance_turn(self) -> None:
        """Advance to the next player's turn, taking skips into account."""
        steps = 2 if self.skip_next else 1
        self.skip_next = False
        self.current_player_index = (
            self.current_player_index + (self.direction * steps)
        ) % len(self.players)

    def is_valid_play(self, card: Card) -> bool:
        """Return True if *card* can be played on the current top card."""
        if self.draw_stack > 0:
            # During an active draw stack only 7s can be played to chain
            return card.rank == DRAW_TWO_RANK

        if self.declared_suit is not None:
            # After a Jack, only the declared suit (or another Jack) matches
            return card.rank == WILD_RANK or card.suit == self.declared_suit

        top = self.top_card
        return (
            card.suit == top.suit
            or card.rank == top.rank
            or card.rank == WILD_RANK
        )

    def play_card(self, player: Player, card: Card,
                  declared_suit: Optional[Suit] = None) -> None:
        """Remove *card* from player's hand and apply its effect."""
        player.hand.remove(card)
        self.discard_pile.append(card)
        self.declared_suit = None

        if card.rank == DRAW_TWO_RANK:
            self.draw_stack += 2

        elif card.rank == SKIP_RANK:
            self.skip_next = True

        elif card.rank == REVERSE_RANK:
            if len(self.players) == 2:
                # In a 2-player game, Ace acts like a skip
                self.skip_next = True
            else:
                self.direction *= -1

        elif card.rank == WILD_RANK:
            if declared_suit is None:
                raise ValueError("Must declare a suit when playing a Jack")
            self.declared_suit = declared_suit

    def apply_draw_penalty(self, player: Player) -> None:
        """Force the player to draw the accumulated draw stack."""
        amount = self.draw_stack
        self.draw_stack = 0
        self._draw_cards(player, amount)

    def draw_one(self, player: Player) -> Card:
        """Player voluntarily draws one card."""
        cards = self._draw_cards(player, 1)
        return cards[0]

    def _draw_cards(self, player: Player, n: int) -> list[Card]:
        cards: list[Card] = []
        for _ in range(n):
            if len(self.deck) == 0:
                if len(self.discard_pile) <= 1:
                    # No cards left at all — rare edge case
                    break
                self.deck.reshuffle_from_discard(self.discard_pile)
            cards.extend(self.deck.draw(1))
        player.hand.extend(cards)
        return cards

    def is_round_over(self) -> bool:
        return any(len(p.hand) == 0 for p in self.players)

    def round_winner(self) -> Optional[Player]:
        for p in self.players:
            if len(p.hand) == 0:
                return p
        return None

    def tally_round(self) -> None:
        """Add the hand values of all losers to the winner's score."""
        winner = self.round_winner()
        if winner is None:
            return
        points = sum(p.hand_value() for p in self.players if p is not winner)
        winner.score += points


def game_winner(players: list[Player]) -> Optional[Player]:
    for p in players:
        if p.score >= WINNING_SCORE:
            return p
    return None


def is_game_over(players: list[Player]) -> bool:
    return game_winner(players) is not None