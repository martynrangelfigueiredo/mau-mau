# Mau-Mau Card Game - Persisted user profiles
# Copyright (C) 2024  mau-mau contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Local, per-player profiles: each player name keeps its own separate
history (rounds/games played, wins, scores) in ~/.mau-mau/settings.json."""

from __future__ import annotations

import getpass
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


def get_default_player_name() -> str:
    """Return the logged-in OS username, falling back to 'Player' if unresolvable."""
    try:
        name = getpass.getuser().strip()
        if name:
            return name
    except Exception:
        pass
    return "Player"


def _new_stats() -> dict:
    """A fresh, empty stats dictionary."""
    return {
        "games_played": 0,
        "games_won": 0,
        "rounds_played": 0,
        "rounds_won": 0,
        "best_score": 0,
        "last_played": None,
        "history": [],
    }


_MAX_HISTORY_ENTRIES = 200


import hashlib
import hmac

_SECRET_SALT = b"mau-mau-v1-anti-tamper-secure-hash-salt-key-2024"


def _compute_profile_signature(stats: dict) -> str:
    """Compute HMAC-SHA256 checksum over profile stats and history to detect manual OS tampering."""
    payload = json.dumps(
        {
            "games_played": stats.get("games_played", 0),
            "games_won": stats.get("games_won", 0),
            "rounds_played": stats.get("rounds_played", 0),
            "rounds_won": stats.get("rounds_won", 0),
            "best_score": stats.get("best_score", 0),
            "history": stats.get("history", []),
        },
        sort_keys=True,
    )
    return hmac.new(_SECRET_SALT, payload.encode("utf-8"), hashlib.sha256).hexdigest()


def _settings_file() -> Path:
    return Path.home() / ".mau-mau" / "settings.json"


def _load() -> dict:
    path = _settings_file()
    if not path.exists():
        return {"last_profile": None, "profiles": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"last_profile": None, "profiles": {}}

    if "profiles" not in data:
        # Migrate the older single-name format: {"player_name": "..."}
        legacy_name = data.get("player_name")
        data = {"last_profile": legacy_name, "profiles": {}}
        if legacy_name:
            data["profiles"][legacy_name] = _new_stats()

    data.setdefault("last_profile", None)
    data.setdefault("profiles", {})
    for name, stats in list(data["profiles"].items()):
        # Fill in any fields missing from profiles saved by older versions.
        for key, default in _new_stats().items():
            stats.setdefault(key, [] if isinstance(default, list) else default)

        # Verify signature to detect manual OS file tampering
        saved_sig = stats.get("signature")
        if saved_sig is not None:
            expected_sig = _compute_profile_signature(stats)
            if not hmac.compare_digest(saved_sig, expected_sig):
                # Tampering detected! Reset tampered profile stats cleanly.
                data["profiles"][name] = _new_stats()

    return data


def _save(data: dict) -> None:
    path = _settings_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    # Sign all profile stats before persisting to disk
    for stats in data.get("profiles", {}).values():
        stats["signature"] = _compute_profile_signature(stats)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


import locale


def get_system_language() -> str:
    """Detect OS language and return matching supported game language code, or 'en' if unsupported."""
    from .i18n import SUPPORTED_LANGUAGES
    try:
        loc = None
        if hasattr(locale, "getdefaultlocale"):
            loc = locale.getdefaultlocale()[0]
        if not loc and hasattr(locale, "getlocale"):
            loc = locale.getlocale()[0]
        if loc:
            loc_clean = loc.replace("-", "_")
            # 1. Exact match (e.g. 'pt_BR', 'pt_PT')
            if loc_clean in SUPPORTED_LANGUAGES:
                return loc_clean
            # 2. Match two-letter prefix (e.g. 'pt' -> 'pt_BR' or 'pt_PT', 'de', 'nl', 'pl', 'cs', 'hu', 'es', 'fr', 'it', 'en')
            prefix = loc_clean.split("_")[0].lower()
            if prefix == "pt":
                return "pt_PT" if "PT" in loc_clean.upper() else "pt_BR"
            for code in SUPPORTED_LANGUAGES:
                if code == prefix:
                    return code
    except Exception:
        pass
    return "en"


def get_language() -> str:
    """Return saved language preference, or auto-detect OS language on first launch (falling back to 'en')."""
    data = _load()
    if "language" in data:
        return data["language"]
    return get_system_language()


def set_language(code: str) -> None:
    """Save the user's explicitly selected language preference."""
    data = _load()
    data["language"] = code
    _save(data)


def list_profile_names() -> list[str]:
    """Every known profile name, alphabetically."""
    return sorted(_load()["profiles"].keys(), key=str.casefold)


def load_last_profile() -> Optional[str]:
    """The most recently used profile name, if it still exists."""
    data = _load()
    name = data.get("last_profile")
    return name if name in data["profiles"] else None


def get_profile_stats(name: str) -> dict:
    """Stats for *name*, or fresh defaults if the profile doesn't exist yet."""
    stats = _load()["profiles"].get(name, _new_stats())
    stats = stats.copy()
    stats.pop("history", None)

    rounds_played = stats.get("rounds_played", 0)
    rounds_won = stats.get("rounds_won", 0)
    games_played = stats.get("games_played", 0)
    games_won = stats.get("games_won", 0)

    stats["win_rate_rounds"] = round((rounds_won / rounds_played * 100), 1) if rounds_played > 0 else 0.0
    stats["win_rate_games"] = round((games_won / games_played * 100), 1) if games_played > 0 else 0.0
    stats["total_played"] = rounds_played + games_played
    stats["total_wins"] = rounds_won + games_won
    return stats


def get_profile_history(name: str, limit: int = 20) -> list[dict]:
    """The *name* profile's most recent plays first, capped at *limit*."""
    history = _load()["profiles"].get(name, _new_stats()).get("history", [])
    return list(reversed(history))[:limit]


def ensure_profile(name: str) -> None:
    """Create a fresh, separate history for *name* if needed and mark it current."""
    data = _load()
    if name not in data["profiles"]:
        data["profiles"][name] = _new_stats()
    data["last_profile"] = name
    _save(data)


def delete_profile(name: str) -> bool:
    """Delete profile *name* and its history from settings if it exists."""
    data = _load()
    if name not in data["profiles"]:
        return False
    del data["profiles"][name]
    if data.get("last_profile") == name:
        remaining = list(data["profiles"].keys())
        data["last_profile"] = remaining[0] if remaining else None
    _save(data)
    return True


def rename_profile(old_name: str, new_name: str) -> bool:
    """Rename profile *old_name* to *new_name*, transferring stats and history."""
    clean_new = new_name.strip()
    if not clean_new:
        return False
    data = _load()
    if old_name not in data["profiles"]:
        return False
    if clean_new != old_name and clean_new in data["profiles"]:
        return False

    stats = data["profiles"].pop(old_name)
    data["profiles"][clean_new] = stats
    if data.get("last_profile") == old_name:
        data["last_profile"] = clean_new
    _save(data)
    return True


def reset_profile_stats(name: str) -> bool:
    """Reset statistics and clear game history for profile *name*."""
    data = _load()
    if name not in data["profiles"]:
        return False
    data["profiles"][name] = _new_stats()
    _save(data)
    return True


def record_round_result(
    name: str, won: bool, points_earned: int, total_score: int, opponents: list[str],
) -> None:
    """Save the outcome of a single round for *name* (called after every round)."""
    data = _load()
    stats = data["profiles"].setdefault(name, _new_stats())
    stats["rounds_played"] += 1
    if won:
        stats["rounds_won"] += 1
    stats["best_score"] = max(stats["best_score"], total_score)
    stats["last_played"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    stats["history"].append({
        "type": "round",
        "timestamp": stats["last_played"],
        "won": won,
        "points_earned": points_earned,
        "total_score": total_score,
        "opponents": opponents,
    })
    stats["history"] = stats["history"][-_MAX_HISTORY_ENTRIES:]
    data["last_profile"] = name
    _save(data)


def record_game_result(name: str, won: bool, final_score: int) -> None:
    """Save the outcome of a completed game (first to reach the winning score)."""
    data = _load()
    stats = data["profiles"].setdefault(name, _new_stats())
    stats["games_played"] += 1
    if won:
        stats["games_won"] += 1
    stats["best_score"] = max(stats["best_score"], final_score)
    stats["last_played"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    stats["history"].append({
        "type": "game",
        "timestamp": stats["last_played"],
        "won": won,
        "final_score": final_score,
    })
    stats["history"] = stats["history"][-_MAX_HISTORY_ENTRIES:]
    data["last_profile"] = name
    _save(data)
