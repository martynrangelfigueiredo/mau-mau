"""Unit tests for Mau-Mau Web HTTP API server endpoints."""
import json
import urllib.request
import urllib.parse
from maumau.server import _serialize_card, _serialize_state, _process_turn_advancement
from maumau.cards import Card, Suit, Rank
from maumau.game import GameState, Player


def test_serialize_card():
    c = Card(Suit.HEARTS, Rank.JACK)
    s = _serialize_card(c)
    assert s["suit"] == "♥"
    assert s["rank"] == "JACK"
    assert s["symbol"] == "J"
    assert s["color"] == "red"
    assert s["points"] == 20


def test_serialize_state():
    p1 = Player("Alice", is_human=True)
    p2 = Player("CPU-1", is_human=False)
    state = GameState([p1, p2])
    data = _serialize_state(state, "test-session-123", "Test message")

    assert data["session_id"] == "test-session-123"
    assert data["current_player_name"] == "Alice"
    assert data["is_human_turn"] is True
    assert len(data["players"]) == 2
    assert data["message"] == "Test message"


def test_turn_advancement_skip():
    p1 = Player("Alice", is_human=True)
    p2 = Player("CPU-1", is_human=False)
    state = GameState([p1, p2])
    state.skip_next = True

    msg = _process_turn_advancement(state)
    assert "skipped" in msg.lower()
    assert state.current_player == p2
