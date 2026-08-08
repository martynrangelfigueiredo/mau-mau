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
    QInputDialog,
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

from .ai import ai_choose_action, get_random_ai_names
from .cards import Card, Rank, Suit, DRAW_TWO_RANK, WILD_RANK
from .game import (
    GameState,
    Player,
    WINNING_SCORE,
    is_game_over,
    game_winner,
)
from .i18n import SUPPORTED_LANGUAGES, pluralize, t
from .settings import (
    delete_profile,
    ensure_profile,
    get_default_player_name,
    get_language,
    get_profile_history,
    get_profile_stats,
    list_profile_names,
    load_last_profile,
    record_game_result,
    record_round_result,
    rename_profile,
    reset_profile_stats,
    set_language,
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


def extract_country_code(name: str) -> Optional[str]:
    """Extract 2-letter country code from name like '🤖 [DE] Lukas'."""
    if "[" in name and "]" in name:
        code = name.split("[")[1].split("]")[0].strip().upper()
        if len(code) == 2 and code.isalpha():
            return code
    return None


def _draw_country_flag(country_code: str, width: int = 24, height: int = 16) -> QPixmap:
    """Procedurally draw vector flag graphic for 10 Mau-Mau countries."""
    pix = QPixmap(width, height)
    pix.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    w, h = float(width), float(height)
    code = country_code.upper()

    if code == "DE":
        painter.fillRect(QRectF(0, 0, w, h / 3), QColor("#000000"))
        painter.fillRect(QRectF(0, h / 3, w, h / 3), QColor("#DD0000"))
        painter.fillRect(QRectF(0, 2 * h / 3, w, h / 3), QColor("#FFCC00"))
    elif code == "AT":
        painter.fillRect(QRectF(0, 0, w, h / 3), QColor("#ED2939"))
        painter.fillRect(QRectF(0, h / 3, w, h / 3), QColor("#FFFFFF"))
        painter.fillRect(QRectF(0, 2 * h / 3, w, h / 3), QColor("#ED2939"))
    elif code == "CH":
        painter.fillRect(QRectF(0, 0, w, h), QColor("#D52B1E"))
        painter.setBrush(QColor("#FFFFFF"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(QRectF(w * 0.4, h * 0.2, w * 0.2, h * 0.6))
        painter.drawRect(QRectF(w * 0.2, h * 0.4, w * 0.6, h * 0.2))
    elif code == "BR":
        painter.fillRect(QRectF(0, 0, w, h), QColor("#009B3A"))
        path = QPainterPath()
        path.moveTo(w * 0.5, h * 0.15)
        path.lineTo(w * 0.85, h * 0.5)
        path.lineTo(w * 0.5, h * 0.85)
        path.lineTo(w * 0.15, h * 0.5)
        path.closeSubpath()
        painter.fillPath(path, QColor("#FEDF00"))
        painter.setBrush(QColor("#002776"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QRectF(w * 0.35, h * 0.3, w * 0.3, h * 0.4))
    elif code == "NL":
        painter.fillRect(QRectF(0, 0, w, h / 3), QColor("#AE1C28"))
        painter.fillRect(QRectF(0, h / 3, w, h / 3), QColor("#FFFFFF"))
        painter.fillRect(QRectF(0, 2 * h / 3, w, h / 3), QColor("#21468B"))
    elif code == "PL":
        painter.fillRect(QRectF(0, 0, w, h / 2), QColor("#FFFFFF"))
        painter.fillRect(QRectF(0, h / 2, w, h / 2), QColor("#DC143C"))
    elif code == "CZ":
        painter.fillRect(QRectF(0, 0, w, h / 2), QColor("#FFFFFF"))
        painter.fillRect(QRectF(0, h / 2, w, h / 2), QColor("#D7141A"))
        path = QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(w * 0.5, h * 0.5)
        path.lineTo(0, h)
        path.closeSubpath()
        painter.fillPath(path, QColor("#11457E"))
    elif code == "HU":
        painter.fillRect(QRectF(0, 0, w, h / 3), QColor("#CD2A3E"))
        painter.fillRect(QRectF(0, h / 3, w, h / 3), QColor("#FFFFFF"))
        painter.fillRect(QRectF(0, 2 * h / 3, w, h / 3), QColor("#436F4D"))
    elif code == "AR":
        painter.fillRect(QRectF(0, 0, w, h / 3), QColor("#74ACDF"))
        painter.fillRect(QRectF(0, h / 3, w, h / 3), QColor("#FFFFFF"))
        painter.fillRect(QRectF(0, 2 * h / 3, w, h / 3), QColor("#74ACDF"))
        painter.setBrush(QColor("#F6B40E"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QRectF(w * 0.4, h * 0.38, w * 0.2, h * 0.24))
    elif code == "PT":
        painter.fillRect(QRectF(0, 0, w * 0.4, h), QColor("#046A38"))
        painter.fillRect(QRectF(w * 0.4, 0, w * 0.6, h), QColor("#DA291C"))
        painter.setBrush(QColor("#FEDF00"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QRectF(w * 0.3, h * 0.3, w * 0.2, h * 0.4))
    elif code == "GB":
        painter.fillRect(QRectF(0, 0, w, h), QColor("#00247D"))
        painter.setBrush(QColor("#FFFFFF"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(QRectF(w * 0.4, 0, w * 0.2, h))
        painter.drawRect(QRectF(0, h * 0.35, w, h * 0.3))
        painter.setBrush(QColor("#CF142B"))
        painter.drawRect(QRectF(w * 0.44, 0, w * 0.12, h))
        painter.drawRect(QRectF(0, h * 0.4, w, h * 0.2))
    elif code == "ES":
        painter.fillRect(QRectF(0, 0, w, h * 0.25), QColor("#AA151B"))
        painter.fillRect(QRectF(0, h * 0.25, w, h * 0.5), QColor("#F1BF00"))
        painter.fillRect(QRectF(0, h * 0.75, w, h * 0.25), QColor("#AA151B"))
    elif code == "FR":
        painter.fillRect(QRectF(0, 0, w / 3, h), QColor("#002395"))
        painter.fillRect(QRectF(w / 3, 0, w / 3, h), QColor("#FFFFFF"))
        painter.fillRect(QRectF(2 * w / 3, 0, w / 3, h), QColor("#ED2939"))
    elif code == "IT":
        painter.fillRect(QRectF(0, 0, w / 3, h), QColor("#009246"))
        painter.fillRect(QRectF(w / 3, 0, w / 3, h), QColor("#FFFFFF"))
        painter.fillRect(QRectF(2 * w / 3, 0, w / 3, h), QColor("#CE2B37"))
    else:
        painter.fillRect(QRectF(0, 0, w, h), QColor("#888888"))

    painter.setPen(QPen(QColor("#444444"), 1))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawRect(QRectF(0, 0, w - 1, h - 1))

    painter.end()
    return pix


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

    def _get_overlap(self) -> int:
        if self.count <= 8:
            return 16
        return max(8, 120 // max(1, self.count))

    def set_count(self, count: int) -> None:
        self.count = count
        if count <= 0:
            self.setFixedWidth(0)
        else:
            overlap = self._get_overlap()
            self.setFixedWidth(SMALL_CARD_W + (count - 1) * overlap + 10)
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802 (Qt override)
        if self.count <= 0:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        back = PIXMAPS.back(SMALL_CARD_W, SMALL_CARD_H)
        overlap = self._get_overlap()
        for i in range(self.count):
            painter.drawPixmap(5 + i * overlap, 5, back)


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
                f"font-size: 22px; font-weight: bold; color: {SUIT_HEX[suit]};"
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
    """Read-only list of a profile's past rounds and games with option to reset."""

    def __init__(self, parent: QWidget, profile_name: str, on_reset_callback: Optional[Callable[[], None]] = None) -> None:
        super().__init__(parent)
        self.profile_name = profile_name
        self.on_reset_callback = on_reset_callback
        lang = get_language()
        self.setWindowTitle(t("history_title", lang, name=profile_name))
        self.resize(480, 440)
        self.setStyleSheet("background-color: #0b6623; color: white;")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self._populate_list()

    def _populate_list(self) -> None:
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

        lang = get_language()
        entries = get_profile_history(self.profile_name, limit=50)

        if not entries:
            empty_lbl = QLabel(t("no_plays_yet", lang))
            empty_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_lbl.setStyleSheet("font-size: 14px; color: #ffe066; margin: 30px;")
            self.main_layout.addWidget(empty_lbl)
        else:
            list_widget = QListWidget()
            list_widget.setStyleSheet(
                "background-color: rgba(13, 79, 28, 0.95); "
                "border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 6px;"
            )
            for entry in entries:
                list_widget.addItem(self._format_entry(entry))
            self.main_layout.addWidget(list_widget)

        btn_row = QHBoxLayout()
        btn_row.setContentsMargins(0, 8, 0, 0)
        btn_row.setSpacing(12)
        btn_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if entries:
            reset_btn = QPushButton(t("reset_history", lang))
            reset_btn.setStyleSheet(
                "background-color: #d9534f; color: white; font-weight: bold; "
                "padding: 6px 16px; border-radius: 4px;"
            )
            reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            reset_btn.clicked.connect(self._confirm_reset)
            btn_row.addWidget(reset_btn)

        close_btn = QPushButton("OK")
        close_btn.setStyleSheet(
            f"background-color: {ACCENT_COLOR}; color: black; font-weight: bold; "
            "padding: 6px 22px; border-radius: 4px;"
        )
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        btn_row.addWidget(close_btn)

        self.main_layout.addLayout(btn_row)

    def _confirm_reset(self) -> None:
        lang = get_language()
        reply = QMessageBox.question(
            self,
            t("confirm_reset_title", lang),
            t("confirm_reset_msg", lang, name=self.profile_name),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            reset_profile_stats(self.profile_name)
            self._populate_list()
            if self.on_reset_callback:
                self.on_reset_callback()

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


class RulesDialog(QDialog):
    """Detailed game rules modal dialog localized for the active language."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        lang = get_language()
        self.setWindowTitle(t("rules_title", lang))
        self.resize(560, 540)
        self.setStyleSheet("background-color: #0b6623; color: white;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        title = QLabel(t("rules_title", lang))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #ffe066; margin-bottom: 8px;")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: 1px solid rgba(255, 255, 255, 0.2); background-color: rgba(13, 79, 28, 0.95); border-radius: 8px;")

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(18, 18, 18, 18)

        body_label = QLabel(t("rules_content", lang))
        body_label.setTextFormat(Qt.TextFormat.RichText)
        body_label.setWordWrap(True)
        body_label.setStyleSheet("font-size: 14px; line-height: 1.6; color: #ffffff;")
        content_layout.addWidget(body_label)

        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

        close_btn = QPushButton("OK")
        close_btn.setStyleSheet(
            f"background-color: {ACCENT_COLOR}; font-weight: bold; "
            "font-size: 14px; padding: 6px 20px; border-radius: 4px; color: black;"
        )
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)


class ProfileStatsWidget(QFrame):
    """Modern dashboard card for profile statistics and win rate analytics."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setStyleSheet(
            "QFrame { "
            "  background-color: rgba(13, 79, 28, 0.85); "
            "  border: 1px solid rgba(255, 255, 255, 0.18); "
            "  border-radius: 10px; "
            "}"
        )
        layout = QGridLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(8)

        self.matches_label = QLabel()
        self.wins_label = QLabel()
        self.winrate_label = QLabel()
        self.score_label = QLabel()

        for lbl in (self.matches_label, self.wins_label, self.winrate_label, self.score_label):
            lbl.setStyleSheet("color: white; font-size: 13px; border: none; background: transparent;")

        layout.addWidget(self.matches_label, 0, 0)
        layout.addWidget(self.wins_label, 0, 1)
        layout.addWidget(self.winrate_label, 1, 0)
        layout.addWidget(self.score_label, 1, 1)

        self.set_empty()

    def set_empty(self) -> None:
        lang = get_language()
        round_lbl = pluralize(0, "round_sg", "rounds", lang)
        self.matches_label.setText(f"🎮 <b>{t('matches', lang)}:</b> 0 {round_lbl}")
        self.wins_label.setText(f"🏆 <b>{t('wins', lang)}:</b> 0 {round_lbl}")
        self.winrate_label.setText(f"📊 <b>{t('win_rate', lang)}:</b> 0.0%")
        self.score_label.setText(f"⭐ <b>{t('record', lang)}:</b> 0 {t('points', lang)}")

    def update_stats(self, stats: dict) -> None:
        lang = get_language()
        rounds_p = stats.get("rounds_played", 0)
        games_p = stats.get("games_played", 0)
        rounds_w = stats.get("rounds_won", 0)
        games_w = stats.get("games_won", 0)
        win_rate = stats.get("win_rate_rounds", 0.0)
        best_score = stats.get("best_score", 0)

        rounds_p_lbl = pluralize(rounds_p, "round_sg", "rounds", lang)
        games_p_lbl = pluralize(games_p, "game_sg", "games", lang)
        rounds_w_lbl = pluralize(rounds_w, "round_sg", "rounds", lang)
        games_w_lbl = pluralize(games_w, "game_sg", "games", lang)

        matches_text = f"{rounds_p} {rounds_p_lbl}" + (f" ({games_p} {games_p_lbl})" if games_p > 0 else "")
        wins_text = f"<span style='color:#ffe066;'>{rounds_w} {rounds_w_lbl}</span>" + (f" ({games_w} {games_w_lbl})" if games_w > 0 else "")

        self.matches_label.setText(f"🎮 <b>{t('matches', lang)}:</b> {matches_text}")
        self.wins_label.setText(f"🏆 <b>{t('wins', lang)}:</b> {wins_text}")
        self.winrate_label.setText(f"📊 <b>{t('win_rate', lang)}:</b> <span style='color:#75f585;'>{win_rate}%</span>")
        self.score_label.setText(f"⭐ <b>{t('record', lang)}:</b> <span style='color:#ffe066;'>{best_score} {t('points', lang)}</span>")


class SetupScreen(QWidget):
    NEW_PROFILE = "+ New Player…"

    def __init__(self, on_start: Callable[[str, list[str]], None]) -> None:
        super().__init__()
        self._on_start = on_start
        self.setStyleSheet(f"background-color: {TABLE_COLOR};")

        outer = QVBoxLayout(self)

        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.addStretch()

        self.lang_combo = QComboBox()
        self.lang_combo.setIconSize(QSize(24, 16))
        self.lang_combo.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 0.5); padding: 4px 8px; border-radius: 4px;")
        for code, info in SUPPORTED_LANGUAGES.items():
            icon = QIcon(_draw_country_flag(info["flag"], 24, 16))
            self.lang_combo.addItem(icon, f" {info['country']} — {info['name']}", code)

        curr_lang = get_language()
        idx = self.lang_combo.findData(curr_lang)
        if idx >= 0:
            self.lang_combo.setCurrentIndex(idx)

        self.lang_combo.currentIndexChanged.connect(self._on_language_changed)
        top_row.addWidget(self.lang_combo)
        outer.addLayout(top_row)

        outer.addStretch()

        title = QLabel("MAU-MAU")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white; font-size: 40px; font-weight: bold; margin-bottom: 5px;")
        outer.addWidget(title)

        # Profile Hero Card Container
        hero_card = QFrame()
        hero_card.setStyleSheet(
            "QFrame { "
            "  background-color: rgba(13, 79, 28, 0.95); "
            "  border: 1px solid rgba(255, 255, 255, 0.25); "
            "  border-radius: 12px; "
            "}"
        )
        hero_layout = QVBoxLayout(hero_card)
        hero_layout.setContentsMargins(18, 14, 18, 14)
        hero_layout.setSpacing(8)

        # Primary Hero Profile Name Title
        self.profile_title_label = QLabel()
        self.profile_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_title_label.setStyleSheet(
            "color: #ffe066; font-size: 26px; font-weight: bold; border: none; background: transparent;"
        )
        hero_layout.addWidget(self.profile_title_label)

        # Secondary Actions Toolbar (Rename, History, Delete, Switch Combo)
        actions_row = QHBoxLayout()
        actions_row.setContentsMargins(0, 0, 0, 0)
        actions_row.setSpacing(14)
        actions_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rename_btn = QPushButton("✏️ Rename")
        self.rename_btn.setStyleSheet("color: white; text-decoration: underline; border: none; background: transparent; font-size: 13px;")
        self.rename_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.rename_btn.clicked.connect(self._rename_profile)
        actions_row.addWidget(self.rename_btn)

        self.history_btn = QPushButton("📜 History")
        self.history_btn.setStyleSheet("color: white; text-decoration: underline; border: none; background: transparent; font-size: 13px;")
        self.history_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.history_btn.clicked.connect(self._show_history)
        actions_row.addWidget(self.history_btn)

        self.rules_btn = QPushButton("📖 Rules")
        self.rules_btn.setStyleSheet("color: white; text-decoration: underline; border: none; background: transparent; font-size: 13px;")
        self.rules_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.rules_btn.clicked.connect(self._show_rules)
        actions_row.addWidget(self.rules_btn)

        self.delete_btn = QPushButton("🗑️ Delete")
        self.delete_btn.setStyleSheet("color: #ff6b6b; text-decoration: underline; border: none; background: transparent; font-size: 13px;")
        self.delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.delete_btn.clicked.connect(self._delete_profile)
        actions_row.addWidget(self.delete_btn)

        # Profile Switcher Dropdown
        self.profile_combo = QComboBox()
        self.profile_combo.setMinimumWidth(150)
        self.profile_combo.setStyleSheet("color: white; background-color: #1b3a6b; padding: 3px 8px; border-radius: 4px;")
        self.profile_combo.currentTextChanged.connect(self._on_profile_changed)
        actions_row.addWidget(self.profile_combo)

        hero_layout.addLayout(actions_row)

        # New Player Name Widget (Hidden when existing profile is selected)
        self.new_name_widget = QWidget()
        new_name_layout = QHBoxLayout(self.new_name_widget)
        new_name_layout.setContentsMargins(0, 4, 0, 0)
        new_name_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.new_name_label = QLabel("New profile name:")
        self.new_name_label.setStyleSheet("color: white; font-size: 13px; border: none; background: transparent;")
        new_name_layout.addWidget(self.new_name_label)
        self.new_name_edit = QLineEdit()
        default_user = get_default_player_name()
        self.new_name_edit.setPlaceholderText(f"Type a name (default: {default_user})…")
        self.new_name_edit.setFixedWidth(200)
        new_name_layout.addWidget(self.new_name_edit)
        hero_layout.addWidget(self.new_name_widget)

        outer.addWidget(hero_card, alignment=Qt.AlignmentFlag.AlignCenter)

        # Dashboard Stats Widget
        self.stats_widget = ProfileStatsWidget()
        outer.addWidget(self.stats_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # AI Opponents Section
        form = QGridLayout()
        form_widget = QWidget()
        form_widget.setLayout(form)
        form_widget.setStyleSheet("color: white; font-size: 14px;")
        outer.addWidget(form_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        self.ai_opponents_label = QLabel("AI opponents (1-3):")
        form.addWidget(self.ai_opponents_label, 0, 0)
        self.ai_spin = QSpinBox()
        self.ai_spin.setRange(1, 3)
        self.ai_spin.valueChanged.connect(self._on_ai_count_changed)
        form.addWidget(self.ai_spin, 0, 1)

        self.ai_name_labels: list[QLabel] = []
        self.ai_name_edits: list[QLineEdit] = []
        self.ai_flag_labels: list[QLabel] = []
        self.default_ai_names = get_random_ai_names(3)
        for i in range(1, 4):
            lbl = QLabel(f"AI {i} name:")
            edit = QLineEdit()
            flag_lbl = QLabel()
            preset = self.default_ai_names[i - 1]
            edit.setPlaceholderText(preset)
            edit.setText(preset)
            edit.setProperty("_is_preset", True)

            def _update_flag(e=edit, fl=flag_lbl):
                code = extract_country_code(e.text() or e.placeholderText())
                if code:
                    fl.setPixmap(_draw_country_flag(code, 22, 15))
                else:
                    fl.setPixmap(QPixmap())

            edit.textEdited.connect(lambda _, e=edit: e.setProperty("_is_preset", False))
            edit.textChanged.connect(lambda _, u=_update_flag: u())

            self.ai_name_labels.append(lbl)
            self.ai_name_edits.append(edit)
            self.ai_flag_labels.append(flag_lbl)
            row = i
            form.addWidget(lbl, row, 0)
            form.addWidget(edit, row, 1)
            form.addWidget(flag_lbl, row, 2)
            _update_flag()

        self.start_btn = QPushButton("Start Game")
        self.start_btn.setStyleSheet(
            f"background-color: {ACCENT_COLOR}; font-weight: bold; "
            "font-size: 15px; padding: 8px 24px; border-radius: 6px; color: black;"
        )
        self.start_btn.clicked.connect(self._start)
        outer.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        outer.addStretch()

        self._on_ai_count_changed(self.ai_spin.value())
        self.retranslate_ui()
        self.refresh()

    def _on_language_changed(self, index: int) -> None:
        code = self.lang_combo.itemData(index)
        if code:
            set_language(code)
            self.retranslate_ui()
            self._on_profile_changed(self.profile_combo.currentText())

    def retranslate_ui(self) -> None:
        lang = get_language()
        self.rename_btn.setText(t("rename", lang))
        self.history_btn.setText(t("history", lang))
        self.rules_btn.setText(t("rules", lang))
        self.delete_btn.setText(t("delete", lang))
        self.ai_opponents_label.setText(t("ai_opponents", lang))
        self.new_name_label.setText(t("new_profile_name", lang))
        default_user = get_default_player_name()
        self.new_name_edit.setPlaceholderText(t("type_name_placeholder", lang, default=default_user))
        self.start_btn.setText(t("start_game", lang))
        for i in range(1, 4):
            self.ai_name_labels[i-1].setText(t("ai_name_label", lang, i=i))

    def _show_rules(self) -> None:
        dialog = RulesDialog(self)
        dialog.exec()

    def _on_ai_count_changed(self, count: int) -> None:
        for i in range(3):
            visible = i < count
            self.ai_name_labels[i].setVisible(visible)
            self.ai_name_edits[i].setVisible(visible)
            self.ai_flag_labels[i].setVisible(visible)

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

        # Generate fresh random AI preset names for unedited fields
        self.default_ai_names = get_random_ai_names(3)
        for i in range(3):
            preset = self.default_ai_names[i]
            edit = self.ai_name_edits[i]
            flag_lbl = self.ai_flag_labels[i]
            edit.setPlaceholderText(preset)
            if not edit.text() or edit.property("_is_preset"):
                edit.setText(preset)
                edit.setProperty("_is_preset", True)
            code = extract_country_code(edit.text() or preset)
            if code:
                flag_lbl.setPixmap(_draw_country_flag(code, 22, 15))
            else:
                flag_lbl.setPixmap(QPixmap())

    def _on_profile_changed(self, selected: str) -> None:
        is_new = selected == self.NEW_PROFILE or not selected
        self.new_name_widget.setVisible(is_new)
        self.rename_btn.setVisible(not is_new)
        self.delete_btn.setVisible(not is_new)
        self.history_btn.setVisible(not is_new)

        if is_new:
            default_user = get_default_player_name()
            lang = get_language()
            self.profile_title_label.setText(f"👤 {default_user} ({t('new_profile', lang).replace('+', '').strip('… ')})")
            self.new_name_edit.clear()
            self.new_name_edit.setFocus()
            self.stats_widget.set_empty()
        else:
            self.profile_title_label.setText(f"👤 {selected}")
            stats = get_profile_stats(selected)
            self.stats_widget.update_stats(stats)

    def _start(self) -> None:
        selected = self.profile_combo.currentText()
        if selected == self.NEW_PROFILE or not selected:
            name = self.new_name_edit.text().strip() or get_default_player_name()
        else:
            name = selected
        ensure_profile(name)

        count = self.ai_spin.value()
        ai_names: list[str] = []
        for i in range(count):
            text = self.ai_name_edits[i].text().strip()
            placeholder = self.ai_name_edits[i].placeholderText().strip()
            ai_names.append(text or placeholder or f"CPU-{i + 1}")

        self._on_start(name, ai_names)

    def _show_history(self) -> None:
        name = self.profile_combo.currentText()
        if not name or name == self.NEW_PROFILE:
            return

        dialog = HistoryDialog(self, name, on_reset_callback=self._on_history_reset)
        dialog.exec()

    def _on_history_reset(self) -> None:
        name = self.profile_combo.currentText()
        if name and name != self.NEW_PROFILE:
            self._on_profile_changed(name)

    def _delete_profile(self) -> None:
        name = self.profile_combo.currentText()
        if not name or name == self.NEW_PROFILE:
            QMessageBox.warning(self, "Delete Profile", "Please select an existing profile to delete.")
            return

        reply = QMessageBox.question(
            self,
            "Delete Profile",
            f"Are you sure you want to delete profile '{name}'?\nThis will erase all its statistics and history permanently.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            delete_profile(name)
            self.refresh()

    def _rename_profile(self) -> None:
        old_name = self.profile_combo.currentText()
        if not old_name or old_name == self.NEW_PROFILE:
            QMessageBox.warning(self, "Rename Profile", "Please select an existing profile to rename.")
            return

        new_name, ok = QInputDialog.getText(
            self,
            "Rename Profile",
            f"Enter new name for profile '{old_name}':",
            QLineEdit.EchoMode.Normal,
            old_name,
        )
        if not ok or not new_name.strip() or new_name.strip() == old_name:
            return

        clean_new = new_name.strip()
        if not rename_profile(old_name, clean_new):
            QMessageBox.warning(
                self,
                "Rename Profile",
                f"Could not rename profile. A profile named '{clean_new}' already exists.",
            )
            return

        self.refresh()
        self.profile_combo.setCurrentText(clean_new)


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
            f"background-color: {ACCENT_COLOR}; font-weight: bold; "
            "font-size: 13px; padding: 6px 16px; border-radius: 4px; color: black;"
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
        lang = get_language()
        self.draw_button.setText(t("draw_card", lang))
        self.round_label.setText(t("round_num", lang, n=round_number))
        pts_str = t("points", lang)
        first_win_str = t("first_to_win", lang, score=WINNING_SCORE)
        self.score_label.setText(
            "  |  ".join(f"{p.name}: {p.score} {pts_str}" for p in players)
            + f"   {first_win_str}"
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

            name_row = QHBoxLayout()
            name_row.setContentsMargins(0, 0, 0, 0)
            name_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

            code = extract_country_code(p.name)
            if code:
                flag_lbl = QLabel()
                flag_lbl.setPixmap(_draw_country_flag(code, 20, 13))
                name_row.addWidget(flag_lbl)

            hand_cards_str = pluralize(len(p.hand), "hand_cards_count_one", "hand_cards_count", lang)
            name_label = QLabel(f"{p.name} ({hand_cards_str})")
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            name_label.setStyleSheet(
                "color: #000; background-color: #ffe066; font-weight: bold; "
                "border-radius: 4px; padding: 2px 6px;"
                if is_turn else
                "color: white; font-size: 12px;"
            )
            name_row.addWidget(name_label)

            name_widget = QWidget()
            name_widget.setLayout(name_row)
            box.addWidget(name_widget)
            self.opponents_layout.addWidget(col)

        top = state.top_card
        self.top_card_label.setPixmap(PIXMAPS.face(top))
        self.deck_label.setText(pluralize(len(state.deck), "deck_count_one", "deck_count", lang))

        info_lines = []
        if state.declared_suit is not None:
            info_lines.append(t("declared_suit", lang, s=state.declared_suit.value))
        if state.draw_stack > 0:
            info_lines.append(pluralize(state.draw_stack, "draw_stack_alert_one", "draw_stack_alert", lang))
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

    def start_game(self, name: str, ai_names: list[str]) -> None:
        self.players = [Player(name, is_human=True)]
        for ai_name in ai_names:
            self.players.append(Player(ai_name, is_human=False))
        self.round_number = 0
        self.stack.setCurrentWidget(self.game_screen)
        self.start_round()

    # ------------------------------------------------------------------ #
    # Round / turn flow
    # ------------------------------------------------------------------ #
    def start_round(self) -> None:
        self.round_number += 1
        self.state = GameState(self.players)
        lang = get_language()
        self.game_screen.set_status(t("msg_starting_card", lang, card=self.state.top_card))
        self.process_turn()

    def process_turn(self) -> None:
        assert self.state is not None
        if self.state.is_round_over():
            self.end_round()
            return

        lang = get_language()
        if self.state.skip_next:
            skipped = self.state.current_player
            self.state.skip_next = False
            self.state.advance_turn()
            self.game_screen.render(self.state, self.players, self.round_number)
            self.game_screen.set_status(t("msg_skipped", lang, name=skipped.name))
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

        lang = get_language()
        if state.draw_stack > 0:
            if card.rank != DRAW_TWO_RANK or not state.is_valid_play(card):
                return
            state.play_card(player, card)
            self.game_screen.set_status(t("msg_you_chain_penalty", lang, card=card))
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

        lang = get_language()
        msg = t("msg_you_played", lang, card=card)
        if suit:
            msg += t("msg_ai_declares_suit", lang, suit=suit.value)
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

        lang = get_language()
        if state.draw_stack > 0:
            amount = state.draw_stack
            state.apply_draw_penalty(player)
            self.game_screen.set_status(t("msg_you_drew_amount", lang, amount=amount))
            self.game_screen.set_controls_enabled(False)
            self.after_action()
            return

        drawn = state.draw_one(player)
        if state.is_valid_play(drawn):
            self.game_screen.set_controls_enabled(False)
            self._offer_play_drawn(drawn)
        else:
            self.game_screen.set_status(t("msg_you_drew_card", lang, card=drawn))
            self.game_screen.set_controls_enabled(False)
            self.after_action()

    def _offer_play_drawn(self, drawn: Card) -> None:
        assert self.state is not None
        self.game_screen.render(self.state, self.players, self.round_number)
        lang = get_language()
        answer = QMessageBox.question(
            self.window,
            t("dialog_card_drawn_title", lang),
            t("dialog_card_drawn_msg", lang, card=drawn),
        )
        if answer != QMessageBox.StandardButton.Yes:
            self.game_screen.set_status(t("msg_you_drew_kept", lang, card=drawn))
            self.after_action()
            return

        if drawn.rank == WILD_RANK:
            suit = SuitDialog.ask(self.window)
            if suit is None:
                self.game_screen.set_status(t("msg_you_drew_kept", lang, card=drawn))
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
        lang = get_language()

        if state.draw_stack > 0:
            chainable = [c for c in player.hand if state.is_valid_play(c)]
            if not chainable:
                amount = state.draw_stack
                state.apply_draw_penalty(player)
                self.game_screen.set_status(t("msg_ai_draws_amount", lang, name=player.name, amount=amount))
                self.after_action()
                return

        card, declared = ai_choose_action(state, player)
        if card is None:
            drawn = state.draw_one(player)
            msg = t("msg_ai_draws_card", lang, name=player.name)
            if state.is_valid_play(drawn):
                drawn_declared: Optional[Suit] = None
                if drawn.rank == WILD_RANK:
                    suit_counts = Counter(c.suit for c in player.hand if c.rank != WILD_RANK)
                    drawn_declared = suit_counts.most_common(1)[0][0] if suit_counts else Suit.HEARTS
                state.play_card(player, drawn, drawn_declared)
                msg += t("msg_ai_plays_drawn", lang, card=drawn)
            self.game_screen.set_status(msg)
            self.after_action()
            return

        state.play_card(player, card, declared)
        msg = t("msg_ai_plays", lang, name=player.name, card=card)
        if declared:
            msg += t("msg_ai_declares_suit", lang, suit=declared.value)
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
        lang = get_language()

        if winner:
            QMessageBox.information(
                self.window,
                t("dialog_round_over_title", lang),
                t("dialog_round_over_msg", lang, name=winner.name),
            )

        if is_game_over(self.players):
            champion = game_winner(self.players)
            assert champion is not None
            record_game_result(human.name, won=champion is human, final_score=human.score)
            QMessageBox.information(
                self.window,
                t("dialog_game_over_title", lang),
                t("dialog_game_over_msg", lang, name=champion.name, score=champion.score),
            )
            self.show_setup_screen()
            return

        answer = QMessageBox.question(
            self.window,
            t("dialog_next_round_title", lang),
            t("dialog_next_round_msg", lang),
        )
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
