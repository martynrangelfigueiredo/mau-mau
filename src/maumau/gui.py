# Mau-Mau Card Game - Desktop GUI (PySide6 / Qt)
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
"""Windowed desktop UI built with PySide6 (Qt for Python).

Qt is a free/open-source, cross-platform toolkit (LGPLv3 here, born on and
still heavily used on Linux/KDE) available at https://www.qt.io/qt-for-python.
All card artwork below is drawn procedurally with QPainter — plain geometric
shapes, standard pip layouts and Unicode suit glyphs — so there are no
third-party image assets, trademarks, or specific card-deck designs involved.
"""

from __future__ import annotations

import sys
from collections import Counter
from functools import partial
from typing import Callable, Optional

from PySide6.QtCore import QRectF, QSize, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QIcon, QPainter, QPainterPath, QPen, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from .ai import ai_choose_action
from .cards import Card, Rank, Suit, DRAW_TWO_RANK, WILD_RANK
from .game import (
    GameState,
    Player,
    WINNING_SCORE,
    is_game_over,
    game_winner,
)
from .settings import (
    ensure_profile,
    get_profile_history,
    get_profile_stats,
    list_profile_names,
    load_last_profile,
    record_game_result,
    record_round_result,
)

TABLE_COLOR = "#0b6623"
PANEL_COLOR = "#0d4f1c"
ACCENT_COLOR = "#f5c518"
SUIT_HEX = {
    Suit.HEARTS: "#c81e2c",
    Suit.DIAMONDS: "#c81e2c",
    Suit.CLUBS: "#1a1a1a",
    Suit.SPADES: "#1a1a1a",
}
CARD_W, CARD_H = 96, 134
SMALL_CARD_W, SMALL_CARD_H = 46, 64
AI_DELAY_MS = 900

# Standard pip layouts (fractions of card width/height) used on every
# generic playing-card deck; this is a functional, centuries-old convention
# and not tied to any particular artist's design.
PIP_LAYOUTS: dict[int, list[tuple[float, float]]] = {
    7: [(0.32, 0.18), (0.68, 0.18), (0.5, 0.32), (0.32, 0.5), (0.68, 0.5),
        (0.32, 0.82), (0.68, 0.82)],
    8: [(0.32, 0.16), (0.68, 0.16), (0.32, 0.38), (0.68, 0.38),
        (0.32, 0.62), (0.68, 0.62), (0.32, 0.84), (0.68, 0.84)],
    9: [(0.32, 0.14), (0.68, 0.14), (0.32, 0.35), (0.68, 0.35), (0.5, 0.5),
        (0.32, 0.65), (0.68, 0.65), (0.32, 0.86), (0.68, 0.86)],
    10: [(0.32, 0.12), (0.68, 0.12), (0.5, 0.25), (0.32, 0.38), (0.68, 0.38),
         (0.32, 0.62), (0.68, 0.62), (0.5, 0.75), (0.32, 0.88), (0.68, 0.88)],
}


def _card_pip_count(rank: Rank) -> Optional[int]:
    return {"7": 7, "8": 8, "9": 9, "10": 10}.get(rank.symbol)


def _draw_card_back(width: int, height: int) -> QPixmap:
    pix = QPixmap(width, height)
    pix.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    path = QPainterPath()
    path.addRoundedRect(QRectF(1, 1, width - 2, height - 2), 10, 10)
    painter.setBrush(QColor("#1b3a6b"))
    painter.setPen(QPen(QColor("#0d1f3d"), 2))
    painter.drawPath(path)

    painter.setClipPath(path)
    painter.setPen(QPen(QColor("#3a63ab"), 3))
    step = 14
    for x in range(-height, width + height, step):
        painter.drawLine(x, height, x + height, 0)
    painter.setClipping(False)
    painter.end()
    return pix


def _draw_card_face(card: Card, width: int, height: int) -> QPixmap:
    pix = QPixmap(width, height)
    pix.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    path = QPainterPath()
    path.addRoundedRect(QRectF(1, 1, width - 2, height - 2), 10, 10)
    painter.setBrush(QColor("white"))
    painter.setPen(QPen(QColor("#333333"), 2))
    painter.drawPath(path)
    painter.setClipPath(path)

    color = QColor(SUIT_HEX[card.suit])
    painter.setPen(color)
    suit_char = card.suit.value
    rank_symbol = card.rank.symbol

    corner_font = QFont("Arial", max(10, width // 7), QFont.Weight.Bold)
    painter.setFont(corner_font)
    painter.drawText(QRectF(4, 2, width * 0.4, height * 0.16),
                      Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, rank_symbol)
    suit_font = QFont("Arial", max(9, width // 8))
    painter.setFont(suit_font)
    painter.drawText(QRectF(4, height * 0.15, width * 0.4, height * 0.16),
                      Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, suit_char)

    painter.save()
    painter.translate(width, height)
    painter.rotate(180)
    painter.setFont(corner_font)
    painter.drawText(QRectF(4, 2, width * 0.4, height * 0.16),
                      Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, rank_symbol)
    painter.setFont(suit_font)
    painter.drawText(QRectF(4, height * 0.15, width * 0.4, height * 0.16),
                      Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, suit_char)
    painter.restore()

    _draw_center_motif(painter, card, width, height, color)

    painter.end()
    return pix


def _draw_center_motif(painter: QPainter, card: Card, width: int, height: int, color: QColor) -> None:
    suit_char = card.suit.value
    rank = card.rank

    if rank == Rank.ACE:
        painter.setPen(color)
        painter.setFont(QFont("Arial", int(height * 0.34)))
        painter.drawText(QRectF(0, 0, width, height),
                          Qt.AlignmentFlag.AlignCenter, suit_char)
        return

    if rank in (Rank.JACK, Rank.QUEEN, Rank.KING):
        inset = QRectF(width * 0.22, height * 0.24, width * 0.56, height * 0.52)
        painter.setPen(QPen(color, 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(inset, 8, 8)
        painter.setFont(QFont("Georgia", int(height * 0.22), QFont.Weight.Bold))
        painter.drawText(inset, Qt.AlignmentFlag.AlignCenter, rank.symbol)
        painter.setFont(QFont("Arial", int(height * 0.1)))
        painter.drawText(
            QRectF(inset.x(), inset.y() - height * 0.12, inset.width(), height * 0.12),
            Qt.AlignmentFlag.AlignCenter, suit_char,
        )
        return

    n = _card_pip_count(rank)
    if n is None:
        return
    painter.setFont(QFont("Arial", int(height * 0.13)))
    for fx, fy in PIP_LAYOUTS[n]:
        x, y = fx * width, fy * height
        size = height * 0.16
        painter.drawText(
            QRectF(x - size / 2, y - size / 2, size, size),
            Qt.AlignmentFlag.AlignCenter, suit_char,
        )


class _PixmapCache:
    """Renders card face/back pixmaps once and reuses them."""

    def __init__(self) -> None:
        self._faces: dict[tuple[Card, int, int], QPixmap] = {}
        self._backs: dict[tuple[int, int], QPixmap] = {}

    def face(self, card: Card, width: int = CARD_W, height: int = CARD_H) -> QPixmap:
        key = (card, width, height)
        if key not in self._faces:
            self._faces[key] = _draw_card_face(card, width, height)
        return self._faces[key]

    def back(self, width: int = CARD_W, height: int = CARD_H) -> QPixmap:
        key = (width, height)
        if key not in self._backs:
            self._backs[key] = _draw_card_back(width, height)
        return self._backs[key]


PIXMAPS = _PixmapCache()


class CardButton(QPushButton):
    """A hand card rendered as a real playing card, clickable to play it."""

    def __init__(self, card: Card, on_click: Callable[[Card], None]) -> None:
        super().__init__()
        self.card = card
        self.setIcon(QIcon(PIXMAPS.face(card)))
        self.setIconSize(QSize(CARD_W, CARD_H))
        self.setFixedSize(CARD_W + 10, CARD_H + 10)
        self.setFlat(True)
        self.setStyleSheet("QPushButton { border: none; background: transparent; }")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(partial(on_click, card))


class HandFanWidget(QWidget):
    """Small overlapping card-back fan used to represent an opponent's hand."""

    def __init__(self) -> None:
        super().__init__()
        self.count = 0
        self.setFixedHeight(SMALL_CARD_H + 10)

    def set_count(self, count: int) -> None:
        self.count = count
        shown = min(count, 6)
        self.setFixedWidth(SMALL_CARD_W + shown * 16 + 10)
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802 (Qt override)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        back = PIXMAPS.back(SMALL_CARD_W, SMALL_CARD_H)
        shown = min(self.count, 6)
        for i in range(shown):
            painter.drawPixmap(5 + i * 16, 5, back)


class SuitDialog(QDialog):
    """Popup used to declare a suit after playing a Jack."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle("Choose a suit")
        self.setModal(True)
        self.chosen: Optional[Suit] = None

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Declare a suit:", alignment=Qt.AlignmentFlag.AlignCenter))

        row = QHBoxLayout()
        layout.addLayout(row)
        for suit in Suit:
            btn = QPushButton(suit.value)
            btn.setFixedSize(56, 56)
            btn.setStyleSheet(
                f"QPushButton {{ font-size: 22px; font-weight: bold; color: {SUIT_HEX[suit]}; }}"
            )
            btn.clicked.connect(partial(self._choose, suit))
            row.addWidget(btn)

    def _choose(self, suit: Suit) -> None:
        self.chosen = suit
        self.accept()

    @staticmethod
    def ask(parent: QWidget) -> Optional[Suit]:
        dialog = SuitDialog(parent)
        dialog.exec()
        return dialog.chosen


class HistoryDialog(QDialog):
    """Read-only list of a profile's past rounds and games."""

    def __init__(self, parent: QWidget, profile_name: str) -> None:
        super().__init__(parent)
        self.setWindowTitle(f"History — {profile_name}")
        self.resize(440, 420)

        layout = QVBoxLayout(self)
        entries = get_profile_history(profile_name, limit=50)

        if not entries:
            layout.addWidget(QLabel("No plays recorded yet for this profile."))
        else:
            list_widget = QListWidget()
            for entry in entries:
                list_widget.addItem(self._format_entry(entry))
            layout.addWidget(list_widget)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    @staticmethod
    def _format_entry(entry: dict) -> str:
        when = entry.get("timestamp", "")[:19].replace("T", " ")
        if entry.get("type") == "game":
            result = "WON the game" if entry["won"] else "lost the game"
            return f"{when}  —  {result}  (final score: {entry['final_score']})"
        result = "won" if entry["won"] else "lost"
        opponents = ", ".join(entry.get("opponents", [])) or "?"
        return (
            f"{when}  —  Round {result}, +{entry['points_earned']} pts "
            f"(total {entry['total_score']}) vs {opponents}"
        )


class SetupScreen(QWidget):
    NEW_PROFILE = "+ New Player…"

    def __init__(self, on_start: Callable[[str, int], None]) -> None:
        super().__init__()
        self._on_start = on_start
        self.setStyleSheet(f"background-color: {TABLE_COLOR};")

        outer = QVBoxLayout(self)
        outer.addStretch()

        title = QLabel("MAU-MAU")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white; font-size: 40px; font-weight: bold;")
        outer.addWidget(title)

        form = QGridLayout()
        form_widget = QWidget()
        form_widget.setLayout(form)
        form_widget.setStyleSheet("color: white; font-size: 14px;")
        outer.addWidget(form_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        form.addWidget(QLabel("Profile:"), 0, 0)
        self.profile_combo = QComboBox()
        self.profile_combo.setMinimumWidth(160)
        self.profile_combo.currentTextChanged.connect(self._on_profile_changed)
        form.addWidget(self.profile_combo, 0, 1)

        self.history_btn = QPushButton("View History")
        self.history_btn.setStyleSheet("color: white; text-decoration: underline; border: none;")
        self.history_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.history_btn.clicked.connect(self._show_history)
        form.addWidget(self.history_btn, 0, 2)

        self.new_name_label = QLabel("New player name:")
        form.addWidget(self.new_name_label, 1, 0)
        self.new_name_edit = QLineEdit()
        self.new_name_edit.setPlaceholderText("Type a name…")
        form.addWidget(self.new_name_edit, 1, 1)

        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("color: #ffe066; font-size: 12px;")
        form.addWidget(self.stats_label, 2, 0, 1, 2)

        form.addWidget(QLabel("AI opponents (1-3):"), 3, 0)
        self.ai_spin = QSpinBox()
        self.ai_spin.setRange(1, 3)
        form.addWidget(self.ai_spin, 3, 1)

        start_btn = QPushButton("Start Game")
        start_btn.setStyleSheet(
            f"QPushButton {{ background-color: {ACCENT_COLOR}; font-weight: bold; "
            "font-size: 15px; padding: 8px 20px; }"
        )
        start_btn.clicked.connect(self._start)
        outer.addWidget(start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        outer.addStretch()

        self.refresh()

    def refresh(self) -> None:
        """Reload known profiles; called whenever the setup screen is shown."""
        last_profile = load_last_profile()

        self.profile_combo.blockSignals(True)
        self.profile_combo.clear()
        self.profile_combo.addItems(list_profile_names())
        self.profile_combo.addItem(self.NEW_PROFILE)
        self.profile_combo.blockSignals(False)

        if last_profile:
            self.profile_combo.setCurrentText(last_profile)
        else:
            self.profile_combo.setCurrentText(self.NEW_PROFILE)
        self._on_profile_changed(self.profile_combo.currentText())

    def _on_profile_changed(self, selected: str) -> None:
        is_new = selected == self.NEW_PROFILE or not selected
        self.new_name_label.setVisible(is_new)
        self.new_name_edit.setVisible(is_new)
        if is_new:
            self.new_name_edit.clear()
            self.new_name_edit.setFocus()
            self.stats_label.setText("A separate history will be created for this player.")
        else:
            stats = get_profile_stats(selected)
            self.stats_label.setText(
                f"Games played: {stats['games_played']}  |  "
                f"Wins: {stats['games_won']}  |  Best score: {stats['best_score']}"
            )

    def _start(self) -> None:
        selected = self.profile_combo.currentText()
        if selected == self.NEW_PROFILE or not selected:
            name = self.new_name_edit.text().strip() or "Player"
        else:
            name = selected
        ensure_profile(name)
        self._on_start(name, self.ai_spin.value())

    def _show_history(self) -> None:
        name = self.profile_combo.currentText()
        if not name or name == self.NEW_PROFILE:
            QMessageBox.warning(self, "Profile Name", "Please select a profile to view its history.")
            return

        dialog = HistoryDialog(self, name)
        dialog.exec()


class GameScreen(QWidget):
    def __init__(self, app: "MauMauApp") -> None:
        super().__init__()
        self.app = app
        self.setStyleSheet(f"background-color: {TABLE_COLOR};")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        top_bar = QFrame()
        top_bar.setStyleSheet(f"background-color: {PANEL_COLOR};")
        top_layout = QHBoxLayout(top_bar)
        self.round_label = QLabel()
        self.round_label.setStyleSheet("color: white; font-weight: bold; font-size: 13px;")
        top_layout.addWidget(self.round_label)
        top_layout.addStretch()
        self.score_label = QLabel()
        self.score_label.setStyleSheet("color: white; font-size: 13px;")
        top_layout.addWidget(self.score_label)
        root.addWidget(top_bar)

        self.opponents_layout = QHBoxLayout()
        opponents_widget = QWidget()
        opponents_widget.setLayout(self.opponents_layout)
        root.addWidget(opponents_widget)

        middle = QHBoxLayout()
        root.addLayout(middle, stretch=1)

        self.deck_label = QLabel()
        self.deck_label.setStyleSheet("color: white; font-size: 13px;")
        middle.addWidget(self.deck_label)
        middle.addStretch()

        self.top_card_label = QLabel()
        self.top_card_label.setFixedSize(CARD_W, CARD_H)
        middle.addWidget(self.top_card_label)
        middle.addStretch()

        self.info_label = QLabel()
        self.info_label.setStyleSheet("color: #ffe066; font-size: 12px;")
        middle.addWidget(self.info_label)

        self.status_label = QLabel()
        self.status_label.setStyleSheet("color: white; font-size: 13px; font-style: italic;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        root.addWidget(self.status_label)

        bottom = QFrame()
        bottom.setStyleSheet(f"background-color: {PANEL_COLOR};")
        bottom_layout = QVBoxLayout(bottom)

        self.hand_scroll = QScrollArea()
        self.hand_scroll.setWidgetResizable(True)
        self.hand_scroll.setFixedHeight(CARD_H + 30)
        self.hand_scroll.setStyleSheet("border: none; background: transparent;")
        self.hand_container = QWidget()
        self.hand_container.setStyleSheet("background: transparent;")
        self.hand_layout = QHBoxLayout(self.hand_container)
        self.hand_layout.addStretch()
        self.hand_scroll.setWidget(self.hand_container)
        bottom_layout.addWidget(self.hand_scroll)

        self.draw_button = QPushButton("Draw Card")
        self.draw_button.setStyleSheet(
            f"QPushButton {{ background-color: {ACCENT_COLOR}; font-weight: bold; "
            "font-size: 13px; padding: 6px 16px; }"
        )
        self.draw_button.clicked.connect(self.app.on_draw)
        bottom_layout.addWidget(self.draw_button, alignment=Qt.AlignmentFlag.AlignCenter)

        root.addWidget(bottom)

    def set_status(self, message: str) -> None:
        self.status_label.setText(message)

    def set_controls_enabled(self, enabled: bool) -> None:
        self.draw_button.setEnabled(enabled)
        for i in range(self.hand_layout.count()):
            item = self.hand_layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, CardButton) and getattr(widget, "_playable", False):
                widget.setEnabled(enabled)

    def render(self, state: GameState, players: list[Player], round_number: int) -> None:
        self.round_label.setText(f"Round {round_number}")
        self.score_label.setText(
            "  |  ".join(f"{p.name}: {p.score} pts" for p in players)
            + f"   (First to {WINNING_SCORE} wins)"
        )

        while self.opponents_layout.count():
            item = self.opponents_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for p in players:
            if p.is_human:
                continue
            is_turn = p is state.current_player
            box = QVBoxLayout()
            col = QWidget()
            col.setLayout(box)
            fan = HandFanWidget()
            fan.set_count(len(p.hand))
            box.addWidget(fan, alignment=Qt.AlignmentFlag.AlignCenter)
            name_label = QLabel(f"{p.name} ({len(p.hand)} cards)")
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name_label.setStyleSheet(
                "color: #000; background-color: #ffe066; font-weight: bold; "
                "border-radius: 4px; padding: 2px 6px;"
                if is_turn else
                "color: white; font-size: 12px;"
            )
            box.addWidget(name_label)
            self.opponents_layout.addWidget(col)

        top = state.top_card
        self.top_card_label.setPixmap(PIXMAPS.face(top))
        self.deck_label.setText(f"Deck: {len(state.deck)} cards")

        info_lines = []
        if state.declared_suit is not None:
            info_lines.append(f"Declared suit: {state.declared_suit.value}")
        if state.draw_stack > 0:
            info_lines.append(f"\u26A0 Draw stack: {state.draw_stack} cards pending!")
        self.info_label.setText("\n".join(info_lines))

        human = next(p for p in players if p.is_human)
        while self.hand_layout.count():
            item = self.hand_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        is_human_turn = state.current_player.is_human
        for card in human.hand:
            playable = is_human_turn and state.is_valid_play(card)
            btn = CardButton(card, self.app.on_play_card)
            btn.setEnabled(playable)
            btn._playable = playable
            self.hand_layout.addWidget(btn)
        self.hand_layout.addStretch()

        self.draw_button.setEnabled(is_human_turn)


class MauMauApp:
    """Drives the game state through the Qt widgets."""

    def __init__(self, window: QMainWindow) -> None:
        self.window = window
        self.stack = QStackedWidget()
        window.setCentralWidget(self.stack)

        self.players: list[Player] = []
        self.state: Optional[GameState] = None
        self.round_number = 0

        self.setup_screen = SetupScreen(self.start_game)
        self.game_screen = GameScreen(self)
        self.stack.addWidget(self.setup_screen)
        self.stack.addWidget(self.game_screen)
        self.stack.setCurrentWidget(self.setup_screen)

    def show_setup_screen(self) -> None:
        self.players = []
        self.state = None
        self.round_number = 0
        self.setup_screen.refresh()
        self.stack.setCurrentWidget(self.setup_screen)

    def start_game(self, name: str, num_ai: int) -> None:
        self.players = [Player(name, is_human=True)]
        for i in range(1, num_ai + 1):
            self.players.append(Player(f"CPU-{i}", is_human=False))
        self.round_number = 0
        self.stack.setCurrentWidget(self.game_screen)
        self.start_round()

    # ------------------------------------------------------------------ #
    # Round / turn flow
    # ------------------------------------------------------------------ #
    def start_round(self) -> None:
        self.round_number += 1
        self.state = GameState(self.players)
        self.game_screen.set_status(f"Starting card: {self.state.top_card}")
        self.process_turn()

    def process_turn(self) -> None:
        assert self.state is not None
        if self.state.is_round_over():
            self.end_round()
            return

        if self.state.skip_next:
            skipped = self.state.current_player
            self.state.skip_next = False
            self.state.advance_turn()
            self.game_screen.render(self.state, self.players, self.round_number)
            self.game_screen.set_status(f"{skipped.name} is skipped!")
            QTimer.singleShot(AI_DELAY_MS, self.process_turn)
            return

        self.game_screen.render(self.state, self.players, self.round_number)
        current = self.state.current_player
        if current.is_human:
            self.game_screen.set_controls_enabled(True)
        else:
            self.game_screen.set_controls_enabled(False)
            QTimer.singleShot(AI_DELAY_MS, self.ai_turn)

    def after_action(self) -> None:
        assert self.state is not None
        self.game_screen.render(self.state, self.players, self.round_number)
        if self.state.is_round_over():
            QTimer.singleShot(AI_DELAY_MS, self.end_round)
            return
        self.state.advance_turn()
        QTimer.singleShot(AI_DELAY_MS, self.process_turn)

    # ------------------------------------------------------------------ #
    # Human actions
    # ------------------------------------------------------------------ #
    def on_play_card(self, card: Card) -> None:
        assert self.state is not None
        state = self.state
        player = state.current_player
        if not player.is_human:
            return

        if state.draw_stack > 0:
            if card.rank != DRAW_TWO_RANK or not state.is_valid_play(card):
                return
            state.play_card(player, card)
            self.game_screen.set_status(f"You played {card} to chain the draw penalty.")
            self.game_screen.set_controls_enabled(False)
            self.after_action()
            return

        if not state.is_valid_play(card):
            return

        if card.rank == WILD_RANK:
            suit = SuitDialog.ask(self.window)
            if suit is None:
                return
            self._finish_human_play(card, suit)
        else:
            self._finish_human_play(card, None)

    def _finish_human_play(self, card: Card, suit: Optional[Suit]) -> None:
        assert self.state is not None
        state = self.state
        player = state.current_player
        state.play_card(player, card, suit)

        msg = f"You played {card}."
        if suit:
            msg += f" Declared suit: {suit.value}"
        if len(player.hand) == 1:
            msg += "  *** MAU! ***"
        elif len(player.hand) == 0:
            msg += "  *** MAU-MAU! ***"
        self.game_screen.set_status(msg)
        self.game_screen.set_controls_enabled(False)
        self.after_action()

    def on_draw(self) -> None:
        assert self.state is not None
        state = self.state
        player = state.current_player
        if not player.is_human:
            return

        if state.draw_stack > 0:
            amount = state.draw_stack
            state.apply_draw_penalty(player)
            self.game_screen.set_status(f"You drew {amount} cards.")
            self.game_screen.set_controls_enabled(False)
            self.after_action()
            return

        drawn = state.draw_one(player)
        if state.is_valid_play(drawn):
            self.game_screen.set_controls_enabled(False)
            self._offer_play_drawn(drawn)
        else:
            self.game_screen.set_status(f"You drew {drawn}.")
            self.game_screen.set_controls_enabled(False)
            self.after_action()

    def _offer_play_drawn(self, drawn: Card) -> None:
        assert self.state is not None
        self.game_screen.render(self.state, self.players, self.round_number)
        answer = QMessageBox.question(
            self.window, "Card drawn",
            f"You drew {drawn}, which is playable. Play it now?",
        )
        if answer != QMessageBox.StandardButton.Yes:
            self.game_screen.set_status(f"You drew {drawn} and kept it.")
            self.after_action()
            return

        if drawn.rank == WILD_RANK:
            suit = SuitDialog.ask(self.window)
            if suit is None:
                self.game_screen.set_status(f"You drew {drawn} and kept it.")
                self.after_action()
                return
            self._finish_human_play(drawn, suit)
        else:
            self._finish_human_play(drawn, None)

    # ------------------------------------------------------------------ #
    # AI actions
    # ------------------------------------------------------------------ #
    def ai_turn(self) -> None:
        assert self.state is not None
        state = self.state
        player = state.current_player

        if state.draw_stack > 0:
            chainable = [c for c in player.hand if state.is_valid_play(c)]
            if not chainable:
                amount = state.draw_stack
                state.apply_draw_penalty(player)
                self.game_screen.set_status(f"{player.name} draws {amount} cards.")
                self.after_action()
                return

        card, declared = ai_choose_action(state, player)
        if card is None:
            drawn = state.draw_one(player)
            msg = f"{player.name} draws a card."
            if state.is_valid_play(drawn):
                drawn_declared: Optional[Suit] = None
                if drawn.rank == WILD_RANK:
                    suit_counts = Counter(c.suit for c in player.hand if c.rank != WILD_RANK)
                    drawn_declared = suit_counts.most_common(1)[0][0] if suit_counts else Suit.HEARTS
                state.play_card(player, drawn, drawn_declared)
                msg += f" Plays {drawn}."
            self.game_screen.set_status(msg)
            self.after_action()
            return

        state.play_card(player, card, declared)
        msg = f"{player.name} plays {card}."
        if declared:
            msg += f" Declares suit: {declared.value}"
        if len(player.hand) == 1:
            msg += "  MAU!"
        elif len(player.hand) == 0:
            msg += "  MAU-MAU!"
        self.game_screen.set_status(msg)
        self.after_action()

    # ------------------------------------------------------------------ #
    # Round / game end
    # ------------------------------------------------------------------ #
    def end_round(self) -> None:
        assert self.state is not None
        winner = self.state.round_winner()

        points_earned = 0
        if winner:
            points_earned = sum(p.hand_value() for p in self.players if p is not winner)

        self.state.tally_round()

        human = next(p for p in self.players if p.is_human)
        opponents = [p.name for p in self.players if not p.is_human]

        record_round_result(
            name=human.name,
            won=human is winner,
            points_earned=points_earned if human is winner else 0,
            total_score=human.score,
            opponents=opponents,
        )

        self.game_screen.render(self.state, self.players, self.round_number)
        self.game_screen.set_controls_enabled(False)

        if winner:
            QMessageBox.information(self.window, "Round over", f"{winner.name} wins the round!")

        if is_game_over(self.players):
            champion = game_winner(self.players)
            assert champion is not None
            record_game_result(human.name, won=champion is human, final_score=human.score)
            QMessageBox.information(
                self.window, "Game over",
                f"\U0001F3C6 {champion.name} wins the game with "
                f"{champion.score} points!\nThanks for playing Mau-Mau!",
            )
            self.show_setup_screen()
            return

        answer = QMessageBox.question(self.window, "Next round", "Start next round?")
        if answer == QMessageBox.StandardButton.Yes:
            self.start_round()
        else:
            self.show_setup_screen()


def main() -> None:
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Mau-Mau")
    window.resize(960, 680)
    window.setMinimumSize(800, 600)
    MauMauApp(window)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
