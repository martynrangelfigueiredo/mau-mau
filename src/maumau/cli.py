# Mau-Mau Card Game - Command-line interface
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

import sys
from collections import Counter
from typing import Optional

from .cards import Card, Suit, WILD_RANK
from .game import (
    GameState,
    Player,
    WINNING_SCORE,
    is_game_over,
    game_winner,
)
from .ai import ai_choose_action


SUITS = list(Suit)
SUIT_NAMES = {s.value: s for s in Suit}


def _clear_line() -> None:
    print()


def _print_header() -> None:
    print("=" * 50)
    print("         MAU-MAU  Card Game")
    print("=" * 50)


def _print_scores(players: list[Player]) -> None:
    print("\n--- Scores ---")
    for p in players:
        print(f"  {p.name}: {p.score} pts")
    print(f"  (First to {WINNING_SCORE} wins)\n")


def _display_hand(player: Player) -> None:
    print(f"\nYour hand ({len(player.hand)} cards):")
    for i, card in enumerate(player.hand):
        print(f"  [{i}] {card}")


def _ask_int(prompt: str, lo: int, hi: int) -> int:
    while True:
        try:
            value = int(input(prompt))
            if lo <= value <= hi:
                return value
        except ValueError:
            pass
        print(f"  Please enter a number between {lo} and {hi}.")


def _ask_suit() -> Suit:
    print("  Choose a suit:")
    for i, s in enumerate(SUITS):
        print(f"    [{i}] {s.value} ({s.name.capitalize()})")
    idx = _ask_int("  Your choice: ", 0, len(SUITS) - 1)
    return SUITS[idx]


def human_turn(state: GameState, player: Player) -> None:
    print(f"\n{'─' * 40}")
    print(f"  Top card: {state.top_card}")
    if state.declared_suit:
        print(f"  Declared suit: {state.declared_suit.value}")
    if state.draw_stack > 0:
        print(f"  ⚠  Draw stack: {state.draw_stack} cards pending!")

    _display_hand(player)

    if state.draw_stack > 0:
        # Check if player can chain a 7
        chainable = [c for c in player.hand if state.is_valid_play(c)]
        if chainable:
            print("\n  You can chain a 7 or take the draw penalty.")
            print("  Options:")
            for i, c in enumerate(chainable):
                print(f"    [{i}] Play {c}")
            print(f"    [{len(chainable)}] Draw {state.draw_stack} cards")
            choice = _ask_int("  Your choice: ", 0, len(chainable))
            if choice < len(chainable):
                state.play_card(player, chainable[choice])
                print(f"  You played {chainable[choice]}.")
                return
        # No chainable card — must take penalty
        print(f"\n  No 7 in hand. Drawing {state.draw_stack} cards...")
        state.apply_draw_penalty(player)
        return

    playable = [c for c in player.hand if state.is_valid_play(c)]

    if not playable:
        input("  No playable cards. Press Enter to draw...")
        drawn = state.draw_one(player)
        print(f"  Drew: {drawn}")
        # Check if drawn card is playable
        if state.is_valid_play(drawn):
            yn = input(f"  {drawn} is playable. Play it? (y/n): ").strip().lower()
            if yn == "y":
                declared: Optional[Suit] = None
                if drawn.rank == WILD_RANK:
                    declared = _ask_suit()
                state.play_card(player, drawn, declared)
                print(f"  You played {drawn}.")
        return

    print("\n  Playable cards:")
    for i, c in enumerate(playable):
        print(f"    [{i}] {c}")
    print(f"    [{len(playable)}] Draw a card instead")

    choice = _ask_int("  Your choice: ", 0, len(playable))
    if choice == len(playable):
        drawn = state.draw_one(player)
        print(f"  Drew: {drawn}")
        return

    card = playable[choice]
    declared = None
    if card.rank == WILD_RANK:
        declared = _ask_suit()
    state.play_card(player, card, declared)
    print(f"  You played {card}.")
    if declared:
        print(f"  Declared suit: {declared.value}")

    if len(player.hand) == 1:
        print('  *** MAU! (one card left) ***')
    elif len(player.hand) == 0:
        print('  *** MAU-MAU! (no cards left — round over!) ***')


def ai_turn(state: GameState, player: Player) -> None:
    print(f"\n{'─' * 40}")
    print(f"  {player.name}'s turn ({len(player.hand)} cards in hand).")
    print(f"  Top card: {state.top_card}")
    if state.declared_suit:
        print(f"  Declared suit: {state.declared_suit.value}")

    if state.draw_stack > 0:
        chainable = [c for c in player.hand if state.is_valid_play(c)]
        if not chainable:
            print(f"  {player.name} draws {state.draw_stack} cards.")
            state.apply_draw_penalty(player)
            return

    card, declared = ai_choose_action(state, player)
    if card is None:
        drawn = state.draw_one(player)
        print(f"  {player.name} draws a card.")
        if state.is_valid_play(drawn):
            # Determine declared suit specifically for the drawn card
            drawn_declared: Optional[Suit] = None
            if drawn.rank == WILD_RANK:
                suit_counts = Counter(c.suit for c in player.hand if c.rank != WILD_RANK)
                drawn_declared = suit_counts.most_common(1)[0][0] if suit_counts else Suit.HEARTS
            state.play_card(player, drawn, drawn_declared)
            print(f"  {player.name} plays {drawn}.")
        return

    state.play_card(player, card, declared)
    print(f"  {player.name} plays {card}.")
    if declared:
        print(f"  {player.name} declares suit: {declared.value}")
    if len(player.hand) == 1:
        print(f"  {player.name} says MAU!")
    elif len(player.hand) == 0:
        print(f"  {player.name} says MAU-MAU!")


def play_round(players: list[Player]) -> Player:
    state = GameState(players)
    print(f"\n  Starting card: {state.top_card}")
    _print_scores(players)

    while not state.is_round_over():
        current = state.current_player

        if state.skip_next:
            print(f"\n  {current.name} is skipped!")
            state.skip_next = False
            state.advance_turn()
            continue

        if current.is_human:
            human_turn(state, current)
        else:
            ai_turn(state, current)
            input("  (Press Enter to continue...)")

        if state.is_round_over():
            break

        state.advance_turn()

    winner = state.round_winner()
    state.tally_round()
    return winner


def setup_players() -> list[Player]:
    _print_header()
    print("\nHow many players? (1 human + 1-3 AI opponents)")
    num_ai = _ask_int("Number of AI opponents (1-3): ", 1, 3)
    name = input("Enter your name: ").strip() or "Player"
    players: list[Player] = [Player(name, is_human=True)]
    for i in range(1, num_ai + 1):
        players.append(Player(f"CPU-{i}", is_human=False))
    return players


def main() -> None:
    players = setup_players()
    round_number = 0

    while not is_game_over(players):
        round_number += 1
        _print_header()
        print(f"\n  === Round {round_number} ===")
        winner = play_round(players)
        if winner:
            print(f"\n  *** {winner.name} wins the round! ***")
        _print_scores(players)

        if not is_game_over(players):
            cont = input("Start next round? (y/n): ").strip().lower()
            if cont != "y":
                print("Thanks for playing!")
                sys.exit(0)

    champion = game_winner(players)
    _print_header()
    print(f"\n🏆  {champion.name} wins the game with {champion.score} points!")
    print("Thanks for playing Mau-Mau!\n")


if __name__ == "__main__":
    main()
