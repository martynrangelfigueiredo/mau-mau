# Mau-Mau Card Game - AI opponent
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

from __future__ import annotations

from collections import Counter
from typing import Optional, Tuple

from .cards import Card, Suit, WILD_RANK
from .game import GameState, Player


def ai_choose_action(state: GameState, player: Player) -> Tuple[Optional[Card], Optional[Suit]]:
    """Return (card_to_play, declared_suit) or (None, None) to draw."""
    playable = [c for c in player.hand if state.is_valid_play(c)]

    if not playable:
        return None, None

    # Prefer non-Jacks first; play Jacks only as last resort
    non_wilds = [c for c in playable if c.rank != WILD_RANK]
    chosen = non_wilds[0] if non_wilds else playable[0]

    declared: Optional[Suit] = None
    if chosen.rank == WILD_RANK:
        # Declare the suit we have the most of
        suit_counts = Counter(c.suit for c in player.hand if c.rank != WILD_RANK)
        if suit_counts:
            declared = suit_counts.most_common(1)[0][0]
        else:
            declared = Suit.HEARTS  # fallback

    return chosen, declared
