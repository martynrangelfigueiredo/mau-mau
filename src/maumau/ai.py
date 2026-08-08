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

import random
from collections import Counter
from typing import Optional, Tuple

from .cards import Card, Suit, WILD_RANK
from .game import GameState, Player

AI_NAMES: tuple[str, ...] = (
    # Germany [DE] (5 Male, 5 Female)
    "🤖 [DE] Lukas", "🤖 [DE] Maximilian", "🤖 [DE] Felix", "🤖 [DE] Jonas", "🤖 [DE] Elias",
    "🤖 [DE] Emma", "🤖 [DE] Mia", "🤖 [DE] Sophia", "🤖 [DE] Hannah", "🤖 [DE] Anna",
    # Austria [AT] (5 Male, 5 Female)
    "🤖 [AT] Florian", "🤖 [AT] Tobias", "🤖 [AT] Alexander", "🤖 [AT] David", "🤖 [AT] Marcel",
    "🤖 [AT] Lena", "🤖 [AT] Laura", "🤖 [AT] Marie", "🤖 [AT] Emilia", "🤖 [AT] Sarah",
    # Switzerland [CH] (5 Male, 5 Female)
    "🤖 [CH] Luca", "🤖 [CH] Matteo", "🤖 [CH] Noah", "🤖 [CH] Leon", "🤖 [CH] Gabriel",
    "🤖 [CH] Elena", "🤖 [CH] Lara", "🤖 [CH] Nina", "🤖 [CH] Julia", "🤖 [CH] Alice",
    # Brazil [BR] (5 Male, 5 Female)
    "🤖 [BR] Gabriel", "🤖 [BR] Lucas", "🤖 [BR] Pedro", "🤖 [BR] Mateus", "🤖 [BR] Guilherme",
    "🤖 [BR] Maria", "🤖 [BR] Alice", "🤖 [BR] Julia", "🤖 [BR] Sophia", "🤖 [BR] Isabella",
    # Netherlands [NL] (5 Male, 5 Female)
    "🤖 [NL] Daan", "🤖 [NL] Sem", "🤖 [NL] Milan", "🤖 [NL] Luuk", "🤖 [NL] Bram",
    "🤖 [NL] Tess", "🤖 [NL] Sophie", "🤖 [NL] Julia", "🤖 [NL] Lieke", "🤖 [NL] Eva",
    # Poland [PL] (5 Male, 5 Female)
    "🤖 [PL] Jan", "🤖 [PL] Antoni", "🤖 [PL] Jakub", "🤖 [PL] Szymon", "🤖 [PL] Aleksander",
    "🤖 [PL] Zofia", "🤖 [PL] Julia", "🤖 [PL] Maja", "🤖 [PL] Zuzanna", "🤖 [PL] Hanna",
    # Czech Republic [CZ] (5 Male, 5 Female)
    "🤖 [CZ] Jakub", "🤖 [CZ] Jan", "🤖 [CZ] Tomáš", "🤖 [CZ] Matyáš", "🤖 [CZ] Adam",
    "🤖 [CZ] Eliška", "🤖 [CZ] Anna", "🤖 [CZ] Adéla", "🤖 [CZ] Tereza", "🤖 [CZ] Sofie",
    # Hungary [HU] (5 Male, 5 Female)
    "🤖 [HU] Bence", "🤖 [HU] Máté", "🤖 [HU] Levente", "🤖 [HU] Dominik", "🤖 [HU] Marcell",
    "🤖 [HU] Hanna", "🤖 [HU] Anna", "🤖 [HU] Zoé", "🤖 [HU] Luca", "🤖 [HU] Emma",
    # Argentina [AR] (5 Male, 5 Female)
    "🤖 [AR] Mateo", "🤖 [AR] Thiago", "🤖 [AR] Benjamin", "🤖 [AR] Felipe", "🤖 [AR] Joaquín",
    "🤖 [AR] Catalina", "🤖 [AR] Emma", "🤖 [AR] Martina", "🤖 [AR] Olivia", "🤖 [AR] Sofia",
    # Portugal [PT] (5 Male, 5 Female)
    "🤖 [PT] Martim", "🤖 [PT] Rodrigo", "🤖 [PT] Lourenço", "🤖 [PT] Bernardo", "🤖 [PT] Afonso",
    "🤖 [PT] Maria", "🤖 [PT] Leonor", "🤖 [PT] Matilde", "🤖 [PT] Beatriz", "🤖 [PT] Carolina",
)


def get_random_ai_names(count: int, exclude: Optional[list[str]] = None) -> list[str]:
    """Return *count* distinct random AI names from AI_NAMES."""
    excluded_set = set(exclude or [])
    available = [n for n in AI_NAMES if n not in excluded_set]
    if len(available) < count:
        available = list(AI_NAMES)
    return random.sample(available, min(count, len(available)))


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
