"""Tests for cards module."""
import pytest
from maumau.cards import Card, Deck, Rank, Suit, DRAW_TWO_RANK, SKIP_RANK, REVERSE_RANK, WILD_RANK


def test_deck_has_32_cards():
    deck = Deck()
    assert len(deck) == 32


def test_draw_one():
    deck = Deck()
    cards = deck.draw(1)
    assert len(cards) == 1
    assert len(deck) == 31


def test_draw_five():
    deck = Deck()
    cards = deck.draw(5)
    assert len(cards) == 5
    assert len(deck) == 27


def test_draw_empty_raises():
    deck = Deck()
    deck.draw(32)
    with pytest.raises(ValueError):
        deck.draw(1)


def test_card_str():
    c = Card(Suit.HEARTS, Rank.ACE)
    assert str(c) == "A♥"


def test_card_points_jack():
    c = Card(Suit.CLUBS, Rank.JACK)
    assert c.points == 20


def test_card_points_queen():
    c = Card(Suit.SPADES, Rank.QUEEN)
    assert c.points == 10


def test_card_points_seven():
    c = Card(Suit.DIAMONDS, Rank.SEVEN)
    assert c.points == 0


def test_reshuffle_from_discard():
    deck = Deck()
    discard = deck.draw(20)
    deck.reshuffle_from_discard(discard)
    # After reshuffling, discard should have 1 card (the top card)
    assert len(discard) == 1
    # Deck now contains the 19 cards that were in the discard pile
    assert len(deck) == 19


def test_power_card_ranks():
    assert DRAW_TWO_RANK == Rank.SEVEN
    assert SKIP_RANK == Rank.EIGHT
    assert REVERSE_RANK == Rank.ACE
    assert WILD_RANK == Rank.JACK
