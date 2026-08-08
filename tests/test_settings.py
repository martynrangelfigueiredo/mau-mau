"""Tests for persisted user profiles and statistics recording."""
import json
import pytest
from unittest.mock import patch

from maumau.settings import (
    _new_stats,
    delete_profile,
    ensure_profile,
    get_default_player_name,
    get_profile_history,
    get_profile_stats,
    list_profile_names,
    load_last_profile,
    record_game_result,
    record_round_result,
    rename_profile,
)


@pytest.fixture
def tmp_settings(tmp_path):
    """Point settings file to a temporary file per test."""
    settings_file = tmp_path / "settings.json"
    with patch("maumau.settings._settings_file", return_value=settings_file):
        yield settings_file


def test_get_default_player_name():
    name = get_default_player_name()
    assert isinstance(name, str)
    assert len(name) > 0


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


def test_rename_profile(tmp_settings):
    ensure_profile("Bob")
    record_round_result("Bob", won=True, points_earned=50, total_score=50, opponents=["CPU-1"])
    ensure_profile("Carol")

    # Rename Bob to Robert
    success = rename_profile("Bob", "Robert")
    assert success is True
    assert "Bob" not in list_profile_names()
    assert "Robert" in list_profile_names()

    # Verify Robert inherited Bob's stats and history
    stats = get_profile_stats("Robert")
    assert stats["rounds_played"] == 1
    assert stats["rounds_won"] == 1
    assert stats["best_score"] == 50

    history = get_profile_history("Robert")
    assert len(history) == 1
    assert history[0]["won"] is True

    # Collision test: renaming Robert to Carol (which exists) should fail
    assert rename_profile("Robert", "Carol") is False


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


def test_reset_profile_stats(tmp_settings):
    from maumau.settings import reset_profile_stats
    ensure_profile("Dave")
    record_round_result("Dave", won=True, points_earned=40, total_score=40, opponents=["CPU-1"])
    record_game_result("Dave", won=True, final_score=150)

    stats_before = get_profile_stats("Dave")
    assert stats_before["rounds_played"] == 1
    assert stats_before["games_played"] == 1
    assert len(get_profile_history("Dave")) == 2

    # Reset Dave's stats and history
    success = reset_profile_stats("Dave")
    assert success is True

    stats_after = get_profile_stats("Dave")
    assert stats_after["rounds_played"] == 0
    assert stats_after["games_played"] == 0
    assert stats_after["best_score"] == 0
    assert len(get_profile_history("Dave")) == 0

    # Reset non-existent profile
    assert reset_profile_stats("NonExistent") is False


def test_tamper_protection(tmp_settings):
    ensure_profile("Eve")
    record_round_result("Eve", won=True, points_earned=50, total_score=50, opponents=["CPU-1"])
    stats_before = get_profile_stats("Eve")
    assert stats_before["rounds_played"] == 1

    # Simulate manual file tampering via OS text editor
    raw_data = json.loads(tmp_settings.read_text(encoding="utf-8"))
    raw_data["profiles"]["Eve"]["rounds_played"] = 999  # Falsified value!
    tmp_settings.write_text(json.dumps(raw_data), encoding="utf-8")

    # Load stats — tamper protection should detect signature mismatch and auto-reset profile
    stats_after = get_profile_stats("Eve")
    assert stats_after["rounds_played"] == 0
    assert stats_after["rounds_won"] == 0
    assert len(get_profile_history("Eve")) == 0


def test_os_language_detection_and_persistence(tmp_settings):
    from maumau.settings import get_language, get_system_language, set_language

    # Test system language fallback for unsupported locale
    with patch("locale.getdefaultlocale", return_value=("ja_JP", "UTF-8")):
        assert get_system_language() == "en"

    # Test system language detection for German
    with patch("locale.getdefaultlocale", return_value=("de_DE", "UTF-8")):
        assert get_system_language() == "de"

    # Test first launch auto-detection when no saved preference exists
    with patch("locale.getdefaultlocale", return_value=("pt_BR", "UTF-8")):
        assert get_language() == "pt_BR"

    # Test manual selection persists across runs regardless of OS locale
    set_language("es")
    with patch("locale.getdefaultlocale", return_value=("de_DE", "UTF-8")):
        assert get_language() == "es"
