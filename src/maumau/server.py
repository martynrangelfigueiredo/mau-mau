# Mau-Mau Card Game - Web API & Asset Server
# Copyright (C) 2024 mau-mau contributors
# GPL-3.0-or-later
"""Lightweight, zero-dependency HTTP server providing Web API and serving frontend assets for Kubernetes deployment."""

from __future__ import annotations

import json
import os
import sys
from collections import Counter
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Optional, Any
from urllib.parse import parse_qs, urlparse

from maumau.ai import ai_choose_action
from maumau.cards import WILD_RANK, Card, Rank, Suit
from maumau.game import GameState, Player
from maumau.i18n import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES, TRANSLATIONS, pluralize, t
from maumau.settings import (
    get_language,
    get_profile_history,
    get_profile_stats,
    get_system_language,
    record_game_result,
    record_round_result,
    reset_profile_stats,
    set_language,
)

WEB_DIR = Path(__file__).parent / "web"

# Active web sessions in-memory store
_SESSIONS: dict[str, dict[str, Any]] = {}


def _serialize_card(card: Card) -> dict:
    return {
        "suit": card.suit.value,
        "rank": card.rank.name,
        "symbol": card.rank.symbol,
        "color": card.color,
        "points": card.points,
        "str": str(card),
    }


def _serialize_state(state: GameState, current_session_id: str, last_message: str = "") -> dict:
    current = state.current_player
    lang = get_language()

    players_data = []
    for p in state.players:
        players_data.append(
            {
                "name": p.name,
                "is_human": p.is_human,
                "score": p.score,
                "hand_count": len(p.hand),
                "hand": [_serialize_card(c) for c in p.hand] if p.is_human else [],
            }
        )

    top_c = state.top_card
    return {
        "session_id": current_session_id,
        "current_player_index": state.current_player_index,
        "current_player_name": current.name,
        "is_human_turn": current.is_human,
        "direction": state.direction,
        "draw_stack": state.draw_stack,
        "declared_suit": state.declared_suit.value if state.declared_suit else None,
        "top_card": _serialize_card(top_c),
        "deck_count": len(state.deck),
        "discard_count": len(state.discard_pile),
        "is_round_over": state.is_round_over(),
        "round_winner": state.round_winner().name if state.round_winner() else None,
        "players": players_data,
        "language": lang,
        "message": last_message,
    }


def _process_turn_advancement(state: GameState) -> str:
    """Advance game state turn, handling skips and tallying round end results."""
    if state.is_round_over():
        winner = state.round_winner()
        if winner:
            points_earned = sum(p.hand_value() for p in state.players if p is not winner)
            state.tally_round()
            human = next((p for p in state.players if p.is_human), None)
            if human:
                record_round_result(
                    human.name,
                    won=(winner is human),
                    points_earned=points_earned if winner is human else 0,
                    total_score=human.score,
                    opponents=[p.name for p in state.players if not p.is_human],
                )
                if state.is_game_over():
                    game_winner = max(state.players, key=lambda p: p.score)
                    record_game_result(human.name, won=(game_winner is human), final_score=human.score)
                    return f"🏆 {game_winner.name} won the entire match!"
            return f"🎉 {winner.name} won this round!"

    if state.skip_next:
        skipped = state.current_player
        state.skip_next = False
        state.advance_turn()
        return f"🛑 {skipped.name}'s turn was skipped!"

    return ""


class MauMauWebHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Mau-Mau Web frontend and REST endpoints."""

    def _send_json(self, data: dict, status: int = HTTPStatus.OK) -> None:
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)

    def _send_file(self, file_path: Path, content_type: str) -> None:
        if not file_path.exists() or not file_path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return
        data = file_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path

        # Kubernetes Health Check Endpoints
        if path in ("/health", "/api/health", "/healthz", "/readiness"):
            self._send_json({"status": "ok", "app": "mau-mau-web", "version": "1.0.0"})
            return

        if path == "/api/languages":
            self._send_json(
                {
                    "languages": SUPPORTED_LANGUAGES,
                    "current": get_language(),
                    "system": get_system_language(),
                }
            )
            return

        if path == "/api/translations":
            query = parse_qs(parsed.query)
            lang = query.get("lang", [get_language()])[0]
            resolved_lang = "pt_BR" if lang == "pt" else lang
            lang_dict = TRANSLATIONS.get(resolved_lang, TRANSLATIONS.get("en", {}))
            self._send_json({"lang": resolved_lang, "translations": lang_dict})
            return

        if path == "/api/stats":
            query = parse_qs(parsed.query)
            name = query.get("name", ["Player"])[0]
            stats = get_profile_stats(name)
            history = get_profile_history(name)
            self._send_json({"stats": stats, "history": history})
            return

        # Serve Web Frontend Static Files
        if path == "/" or path == "/index.html":
            self._send_file(WEB_DIR / "index.html", "text/html; charset=utf-8")
            return

        if path == "/style.css":
            self._send_file(WEB_DIR / "style.css", "text/css; charset=utf-8")
            return

        if path == "/app.js":
            self._send_file(WEB_DIR / "app.js", "application/javascript; charset=utf-8")
            return

        # Fallback to static directory
        target = WEB_DIR / path.lstrip("/")
        if target.exists() and target.is_file():
            content_type = "text/plain"
            if target.suffix == ".html":
                content_type = "text/html; charset=utf-8"
            elif target.suffix == ".css":
                content_type = "text/css; charset=utf-8"
            elif target.suffix == ".js":
                content_type = "application/javascript; charset=utf-8"
            elif target.suffix == ".svg":
                content_type = "image/svg+xml"
            elif target.suffix == ".png":
                content_type = "image/png"
            self._send_file(target, content_type)
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Resource not found")

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path

        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len) if content_len > 0 else b"{}"
        try:
            req_data = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            req_data = {}

        if path == "/api/set_language":
            code = req_data.get("language", "en")
            set_language(code)
            self._send_json({"status": "ok", "language": code})
            return

        if path == "/api/reset_stats":
            name = req_data.get("name", "Player").strip()
            success = reset_profile_stats(name)
            self._send_json({"status": "ok" if success else "error", "name": name})
            return

        if path == "/api/game/new":
            human_name = req_data.get("human_name", "Player").strip() or "Player"
            ai_count = int(req_data.get("ai_count", 2))
            ai_count = max(1, min(3, ai_count))

            players = [Player(human_name, is_human=True)]
            ai_names = ["Lukas", "Sophie", "Jan", "Emma", "Max"]
            for i in range(ai_count):
                players.append(Player(f"🤖 {ai_names[i % len(ai_names)]}", is_human=False))

            state = GameState(players)
            session_id = os.urandom(8).hex()
            _SESSIONS[session_id] = {
                "state": state,
                "players": players,
                "round_number": 1,
            }

            self._send_json(_serialize_state(state, session_id, f"🌟 Starting card: {state.top_card}"))
            return

        if path == "/api/game/play":
            session_id = req_data.get("session_id")
            if not session_id or session_id not in _SESSIONS:
                self._send_json({"error": "Invalid session"}, status=HTTPStatus.BAD_REQUEST)
                return

            session = _SESSIONS[session_id]
            state: GameState = session["state"]
            current = state.current_player

            if not current.is_human:
                self._send_json({"error": "Not human turn"}, status=HTTPStatus.BAD_REQUEST)
                return

            card_rank_name = req_data.get("rank")
            card_suit_val = req_data.get("suit")
            declared_suit_val = req_data.get("declared_suit")

            # Find matching card in player hand
            target_card = None
            for c in current.hand:
                if c.rank.name == card_rank_name and c.suit.value == card_suit_val:
                    target_card = c
                    break

            if not target_card or not state.is_valid_play(target_card):
                self._send_json({"error": "Invalid play"}, status=HTTPStatus.BAD_REQUEST)
                return

            declared_suit = Suit(declared_suit_val) if declared_suit_val else None
            state.play_card(current, target_card, declared_suit)

            msg = f"✨ You played {target_card}!"
            if not state.is_round_over():
                state.advance_turn()
                extra_msg = _process_turn_advancement(state)
                if extra_msg:
                    msg += f" {extra_msg}"
            else:
                _process_turn_advancement(state)

            self._send_json(_serialize_state(state, session_id, msg))
            return

        if path == "/api/game/draw":
            session_id = req_data.get("session_id")
            if not session_id or session_id not in _SESSIONS:
                self._send_json({"error": "Invalid session"}, status=HTTPStatus.BAD_REQUEST)
                return

            session = _SESSIONS[session_id]
            state: GameState = session["state"]
            current = state.current_player

            if not current.is_human:
                self._send_json({"error": "Not human turn"}, status=HTTPStatus.BAD_REQUEST)
                return

            if state.draw_stack > 0:
                amount = state.draw_stack
                state.apply_draw_penalty(current)
                msg = f"📥 You drew {amount} penalty cards."
            else:
                drawn = state.draw_one(current)
                msg = f"🎒 You drew {drawn}."

            if not state.is_round_over():
                state.advance_turn()
                extra_msg = _process_turn_advancement(state)
                if extra_msg:
                    msg += f" {extra_msg}"
            else:
                _process_turn_advancement(state)

            self._send_json(_serialize_state(state, session_id, msg))
            return

        if path == "/api/game/ai_turn":
            session_id = req_data.get("session_id")
            if not session_id or session_id not in _SESSIONS:
                self._send_json({"error": "Invalid session"}, status=HTTPStatus.BAD_REQUEST)
                return

            session = _SESSIONS[session_id]
            state: GameState = session["state"]
            current = state.current_player

            if current.is_human or state.is_round_over():
                self._send_json(_serialize_state(state, session_id))
                return

            msg = ""
            # AI logic execution
            if state.draw_stack > 0:
                chainable = [c for c in current.hand if state.is_valid_play(c)]
                if not chainable:
                    amount = state.draw_stack
                    state.apply_draw_penalty(current)
                    msg = f"📥 {current.name} drew {amount} penalty cards."
                    if not state.is_round_over():
                        state.advance_turn()
                        extra_msg = _process_turn_advancement(state)
                        if extra_msg:
                            msg += f" {extra_msg}"
                    else:
                        _process_turn_advancement(state)
                    self._send_json(_serialize_state(state, session_id, msg))
                    return

            card, declared = ai_choose_action(state, current)
            if card is None:
                drawn = state.draw_one(current)
                msg = f"🤖 {current.name} drew 1 card."
                if state.is_valid_play(drawn):
                    drawn_declared: Optional[Suit] = None
                    if drawn.rank == WILD_RANK:
                        suit_counts = Counter(c.suit for c in current.hand if c.rank != WILD_RANK)
                        drawn_declared = suit_counts.most_common(1)[0][0] if suit_counts else Suit.HEARTS
                    state.play_card(current, drawn, drawn_declared)
                    msg += f" and played {drawn} immediately!"
            else:
                state.play_card(current, card, declared)
                msg = f"🤖 {current.name} played {card}."
                if declared:
                    msg += f" (Declared suit: {declared.value})"

            if not state.is_round_over():
                state.advance_turn()
                extra_msg = _process_turn_advancement(state)
                if extra_msg:
                    msg += f" {extra_msg}"
            else:
                _process_turn_advancement(state)

            self._send_json(_serialize_state(state, session_id, msg))
            return

        self.send_error(HTTPStatus.NOT_FOUND, "Endpoint not found")


def main() -> None:
    port = int(os.environ.get("PORT", "8000"))
    server = HTTPServer(("0.0.0.0", port), MauMauWebHandler)
    print(f"Mau-Mau Web Server listening on http://localhost:{port} (Kubernetes ready)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.server_close()


if __name__ == "__main__":
    main()
