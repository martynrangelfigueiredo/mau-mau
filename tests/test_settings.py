"""Tests for persisted user profiles and statistics recording."""
import json
import pytest
from unittest.mock import patch

from maumau.settings import (
    _new_stats,
    delete_profile,
    ensure_profile,
    get_profile_history,
    get_profile_stats,
    list_profile_names,
    load_last_profile,
    record_game_result,
    record_round_result,
)


@pytest.fixture
def tmp_settings(tmp_path):
    """Point settings file to a temporary file per test."""
    settings_file = tmp_path / "settings.json"
    with patch("maumau.settings._settings_file", return_value=settings_file):
        yield settings_file


def test_ensure_profile_creates_new(tmp_settings):
    ensure_profile("Alice")
    assert "Alice" in list_profile_names()
    assert load_last_profile() == "Alice"
    stats = get_profile_stats("Alice")
    assert stats["games_played"] == 0
    assert stats["rounds_played"] == 0


def test_delete_profile(tmp_settings):
    ensure_profile("Alice")
    ensure_profile("Bob")
    assert load_last_profile() == "Bob"
    assert "Alice" in list_profile_names()
    assert "Bob" in list_profile_names()

    # Delete Bob
    success = delete_profile("Bob")
    assert success is True
    assert "Bob" not in list_profile_names()
    assert load_last_profile() == "Alice"

    # Delete non-existent profile
    assert delete_profile("Unknown") is False


def test_record_round_result(tmp_settings):
    ensure_profile("Bob")
    # Record a win
    record_round_result("Bob", won=True, points_earned=25, total_score=25, opponents=["CPU-1"])
    stats = get_profile_stats("Bob")
    assert stats["rounds_played"] == 1
    assert stats["rounds_won"] == 1
    assert stats["games_played"] == 0
    assert stats["best_score"] == 25

    # Record a loss
    record_round_result("Bob", won=False, points_earned=0, total_score=25, opponents=["CPU-1"])
    stats = get_profile_stats("Bob")
    assert stats["rounds_played"] == 2
    assert stats["rounds_won"] == 1
    assert stats["win_rate_rounds"] == 50.0
    assert stats["total_played"] == 2
    assert stats["total_wins"] == 1

    history = get_profile_history("Bob")
    assert len(history) == 2
    assert history[0]["won"] is False
    assert history[1]["won"] is True


def test_record_game_result(tmp_settings):
    ensure_profile("Carol")
    record_game_result("Carol", won=True, final_score=160)
    stats = get_profile_stats("Carol")
    assert stats["games_played"] == 1
    assert stats["games_won"] == 1
    assert stats["win_rate_games"] == 100.0
    assert stats["best_score"] == 160

    history = get_profile_history("Carol")
    assert len(history) == 1
    assert history[0]["type"] == "game"
    assert history[0]["won"] is True
    assert history[0]["final_score"] == 160
