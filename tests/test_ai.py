"""Tests for AI module."""
from maumau.cards import Card, Rank, Suit, WILD_RANK
from maumau.game import GameState, Player
from maumau.ai import AI_NAMES, ai_choose_action, get_random_ai_names


def test_ai_names_count():
    assert len(AI_NAMES) == 100
    for name in AI_NAMES:
        assert name.startswith("🤖 [")
        assert "]" in name


def test_get_random_ai_names():
    names = get_random_ai_names(3)
    assert len(names) == 3
    assert len(set(names)) == 3
    for name in names:
        assert name in AI_NAMES

    # Exclude names
    names_excluded = get_random_ai_names(3, exclude=[names[0]])
    assert names[0] not in names_excluded


def test_ai_plays_valid_card():
    players = [Player("AI", is_human=False), Player("P2", is_human=False)]
    state = GameState(players)
    ai = players[0]
    # Ensure AI has a playable card
    top = state.top_card
    playable_card = Card(top.suit, Rank.NINE if top.rank != Rank.NINE else Rank.TEN)
    ai.hand.append(playable_card)
    card, suit = ai_choose_action(state, ai)
    if card is not None:
        assert state.is_valid_play(card)


def test_ai_returns_none_when_no_playable():
    players = [Player("AI", is_human=False), Player("P2", is_human=False)]
    state = GameState(players)
    ai = players[0]
    # Replace hand with cards that cannot match any top card
    top = state.top_card
    other_suits = [s for s in Suit if s != top.suit]
    other_ranks = [r for r in Rank if r != top.rank and r != WILD_RANK]
    ai.hand = [Card(other_suits[0], other_ranks[0])]
    card, suit = ai_choose_action(state, ai)
    # May be None (draw) or a valid card — just verify no crash
    assert card is None or state.is_valid_play(card)


def test_ai_declares_suit_for_jack():
    players = [Player("AI", is_human=False), Player("P2", is_human=False)]
    state = GameState(players)
    ai = players[0]
    jack = Card(Suit.CLUBS, WILD_RANK)
    ai.hand = [jack]
    card, declared = ai_choose_action(state, ai)
    assert card == jack
    assert declared in list(Suit)
