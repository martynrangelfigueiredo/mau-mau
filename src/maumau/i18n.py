# Mau-Mau Card Game - Internationalization (i18n)
# Copyright (C) 2024 mau-mau contributors
# GPL-3.0-or-later
"""Localization module supporting 10 languages with objective, accessible rules."""

from __future__ import annotations
from typing import Dict, Any

SUPPORTED_LANGUAGES: dict[str, dict[str, str]] = {
    "pt_BR": {"country": "Brasil", "name": "Português (Brasil)", "flag": "BR"},
    "pt_PT": {"country": "Portugal", "name": "Português (Portugal)", "flag": "PT"},
    "en": {"country": "Reino Unido", "name": "English", "flag": "GB"},
    "de": {"country": "Alemanha", "name": "Deutsch", "flag": "DE"},
    "nl": {"country": "Holanda", "name": "Nederlands", "flag": "NL"},
    "pl": {"country": "Polônia", "name": "Polski", "flag": "PL"},
    "cs": {"country": "República Checa", "name": "Čeština", "flag": "CZ"},
    "hu": {"country": "Hungria", "name": "Magyar", "flag": "HU"},
    "es": {"country": "Espanha", "name": "Español", "flag": "ES"},
    "fr": {"country": "França", "name": "Français", "flag": "FR"},
    "it": {"country": "Itália", "name": "Italiano", "flag": "IT"},
}

DEFAULT_LANGUAGE = "en"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "start_game": "🚀 Start Playing Now!",
        "ai_opponents": "Choose number of AI opponents (1 to 3):",
        "ai_name_label": "Opponent {i} Name (AI):",
        "rename": "✏️ Rename Profile",
        "history": "📜 Match History",
        "rules": "📖 Game Rules",
        "delete": "🗑️ Delete Profile",
        "new_profile": "+ Create New Profile…",
        "new_profile_name": "New Player Profile Name:",
        "type_name_placeholder": "Type player name (default: {default})…",
        "matches": "Matches Played",
        "wins": "Victories Won",
        "win_rate": "Win Rate & Success",
        "record": "Best Score Record",
        "rounds": "rounds",
        "round_sg": "round",
        "games": "matches",
        "game_sg": "match",
        "draw_card": "📥 Draw a Card",
        "round_num": "Round {n}",
        "deck_count": "Draw Deck: {c} cards remaining",
        "deck_count_one": "Draw Deck: 1 card remaining",
        "hand_cards_count": "{c} cards in hand",
        "hand_cards_count_one": "1 card in hand",
        "declared_suit": "Current active suit: {s}",
        "draw_stack_alert": "⚠️ Penalty Challenge Active: {c} cards pending to draw!",
        "draw_stack_alert_one": "⚠️ Penalty Challenge Active: 1 card pending to draw!",
        "language": "Language / Idioma",
        "history_title": "Match History for {name}",
        "no_plays_yet": "No plays recorded yet for this profile.",
        "confirm_delete_title": "Delete Profile Confirmation",
        "confirm_delete_msg": "Are you sure you want to permanently delete profile '{name}'?\nThis will erase all past game statistics and records.",
        "reset_history": "🧹 Reset History",
        "confirm_reset_title": "Reset Profile History",
        "confirm_reset_msg": "Are you sure you want to reset all game statistics and history for profile '{name}'?",
        "rename_title": "Rename Player Profile",
        "rename_msg": "Enter a new name for profile '{name}':",
        "rename_duplicate": "Could not rename profile. A profile named '{name}' already exists.",
        "points": "pts",
        "first_to_win": "(First player to reach {score} pts wins!)",
        "msg_starting_card": "🌟 Starting card on table: {card}",
        "msg_skipped": "🛑 Turn skipped! {name} loses their turn.",
        "msg_you_chain_penalty": "⚡ You played {card} and passed the draw penalty challenge!",
        "msg_you_played": "✨ You played card {card}! Keep going!",
        "msg_you_drew_amount": "📥 You drew {amount} penalty cards from the deck.",
        "msg_you_drew_card": "🎒 You drew card {card} and kept it in your hand.",
        "msg_you_drew_kept": "🎒 You drew card {card} and stored it in your hand.",
        "msg_ai_draws_amount": "📥 {name} drew {amount} penalty cards from the deck.",
        "msg_ai_draws_card": "🤖 {name} drew 1 card from the deck.",
        "msg_ai_plays_drawn": " And played {card} right away!",
        "msg_ai_plays": "🤖 {name} played card {card}.",
        "msg_ai_declares_suit": " 🎨 Declared new suit: {suit}",
        "dialog_card_drawn_title": "Playable Card Drawn!",
        "dialog_card_drawn_msg": "🎉 Special card drawn! You drew {card}, which can be played right now. Do you want to play it immediately?",
        "dialog_round_over_title": "Round Completed!",
        "dialog_round_over_msg": "🎉 Congratulations! {name} emptied their hand and won this round!",
        "dialog_game_over_title": "Grand Match Champions!",
        "dialog_game_over_msg": "🏆 GRAND CHAMPION!\n{name} reached {score} points and won the complete Mau-Mau match! Congratulations on your victory!",
        "dialog_next_round_title": "Continue Playing?",
        "dialog_next_round_msg": "Do you want to start the next round now?",
        "rules_title": "Game Rules - Mau-Mau",
        "rules_content": """<h3 style='color: #ffe066;'>📌 Step 1: Main Goal of the Game</h3>
<p>The goal is to discard all cards from your hand onto the table before the other players. The first player to run out of cards wins the round.</p>

<h3 style='color: #ffe066;'>🃏 Step 2: How to Play Your Turn</h3>
<p>Look at the face-up card in the center of the table. You can play a card from your hand if it matches either:</p>
<ul>
  <li><b>The Same Suit</b> (Example: Hearts on Hearts) <i>OR</i></li>
  <li><b>The Same Rank/Number</b> (Example: 7 on 7, King on King).</li>
</ul>

<h3 style='color: #ffe066;'>📥 Step 3: What to Do When You Have No Match?</h3>
<p>If you don't have a valid card to play, click the deck to <b>draw 1 card</b>. If the drawn card is valid, you may play it immediately.</p>

<h3 style='color: #ffe066;'>⚡ Step 4: Special Effect Cards</h3>
<ul>
  <li>🃏 <b>Jack - Change Suit:</b><br>Can be played on any card. The player declares the new suit for the table. (Worth 20 points)</li>
  <li>⚡ <b>7 (Seven) - Draw Two:</b><br>Forces the next player to draw 2 cards and forfeit their turn, unless they also play a 7 (stacking penalty to 4 cards).</li>
  <li>🛑 <b>8 (Eight) - Skip Turn:</b><br>Skips the next player's turn.</li>
  <li>🔄 <b>9 (Nine) - Reverse Direction:</b><br>Reverses the turn order direction around the table.</li>
</ul>

<h3 style='color: #ffe066;'>🏆 Step 5: Scoring and Match Victory</h3>
<p>At the end of each round, the winner receives points for all cards remaining in opponents' hands. The first player to reach <b>150 cumulative points</b> wins the match.</p>""",
    },
    "pt_BR": {
        "start_game": "🚀 Iniciar Partida Agora!",
        "ai_opponents": "Escolha a quantidade de oponentes (1 a 3):",
        "ai_name_label": "Nome do Oponente {i} (IA):",
        "rename": "✏️ Renomear Perfil",
        "history": "📜 Histórico de Jogos",
        "rules": "📖 Regras do Jogo",
        "delete": "🗑️ Excluir Perfil",
        "new_profile": "+ Criar Novo Perfil…",
        "new_profile_name": "Nome do Novo Perfil de Jogador:",
        "type_name_placeholder": "Digite o seu nome (padrão: {default})…",
        "matches": "Partidas Jogadas",
        "wins": "Vitórias Conquistadas",
        "win_rate": "Aproveitamento de Vitórias",
        "record": "Melhor Pontuação",
        "rounds": "rodadas",
        "round_sg": "rodada",
        "games": "jogos",
        "game_sg": "jogo",
        "draw_card": "📥 Comprar Carta",
        "round_num": "Rodada {n}",
        "deck_count": "Baralho de Compra: {c} cartas restantes",
        "deck_count_one": "Baralho de Compra: 1 carta restante",
        "hand_cards_count": "{c} cartas na mão",
        "hand_cards_count_one": "1 carta na mão",
        "declared_suit": "Naipe ativo na mesa: {s}",
        "draw_stack_alert": "⚠️ Desafio Ativo: {c} cartas pendentes para comprar!",
        "draw_stack_alert_one": "⚠️ Desafio Ativo: 1 carta pendente para comprar!",
        "language": "Idioma / Language",
        "history_title": "Histórico de Partidas de {name}",
        "no_plays_yet": "Nenhuma partida registrada ainda para este perfil.",
        "confirm_delete_title": "Confirmar Exclusão de Perfil",
        "confirm_delete_msg": "Tem certeza que deseja excluir permanentemente o perfil '{name}'?\nTodas as suas estatísticas e recordes serão apagados.",
        "reset_history": "🧹 Zerar Histórico",
        "confirm_reset_title": "Zerar Histórico de Jogos",
        "confirm_reset_msg": "Tem certeza que deseja zerar todas as estatísticas e histórico do perfil '{name}'?",
        "rename_title": "Renomear Perfil do Jogador",
        "rename_msg": "Digite o novo nome para o perfil '{name}':",
        "rename_duplicate": "Não foi possível renomear. Já existe um perfil cadastrado com o nome '{name}'.",
        "points": "pts",
        "first_to_win": "(Primeiro jogador a atingir {score} pts vence!)",
        "msg_starting_card": "🌟 Carta inicial na mesa: {card}",
        "msg_skipped": "🛑 Vez pulada! A vez de {name} foi pulada.",
        "msg_you_chain_penalty": "⚡ Você jogou a carta {card} e repassou o desafio de compra!",
        "msg_you_played": "✨ Você jogou a carta {card}! Siga em frente!",
        "msg_you_drew_amount": "📥 Você comprou {amount} cartas de penalidade do baralho.",
        "msg_you_drew_card": "🎒 Você comprou a carta {card} e a guardou na sua mão.",
        "msg_you_drew_kept": "🎒 Você comprou a carta {card} e a guardou no seu monte.",
        "msg_ai_draws_amount": "📥 {name} comprou {amount} cartas de penalidade do baralho.",
        "msg_ai_draws_card": "🤖 {name} comprou 1 carta do baralho.",
        "msg_ai_plays_drawn": " E jogou a carta {card} imediatamente!",
        "msg_ai_plays": "🤖 {name} jogou a carta {card}.",
        "msg_ai_declares_suit": " 🎨 Escolheu o novo naipe: {suit}",
        "dialog_card_drawn_title": "Carta Jogável Comprada!",
        "dialog_card_drawn_msg": "🎉 Carta especial sorteada! Você comprou {card}, que pode ser jogada agora mesmo. Deseja jogá-la imediatamente?",
        "dialog_round_over_title": "Rodada Concluída!",
        "dialog_round_over_msg": "🎉 Parabéns! {name} esvaziou a mão e venceu esta rodada com brilho!",
        "dialog_game_over_title": "Grande Campeão da Partida!",
        "dialog_game_over_msg": "🏆 GRANDIOSO CAMPEÃO!\n{name} atingiu a marca de {score} pontos e venceu a partida completa do Mau-Mau! Parabéns pela vitória!",
        "dialog_next_round_title": "Continuar Jogando?",
        "dialog_next_round_msg": "Deseja iniciar a próxima rodada agora?",
        "rules_title": "Regras do Jogo - Mau-Mau",
        "rules_content": """<h3 style='color: #ffe066;'>📌 Passo 1: Objetivo Principal do Jogo</h3>
<p>O objetivo é descartar todas as cartas da sua mão na mesa antes dos outros jogadores. O primeiro a ficar sem cartas vence a rodada.</p>

<h3 style='color: #ffe066;'>🃏 Passo 2: Como Jogar no Seu Turno</h3>
<p>Observe a carta aberta no centro da mesa. Você pode jogar uma carta da sua mão se ela corresponder a:</p>
<ul>
  <li><b>Ao Mesmo Naipe</b> (Exemplo: Copas sobre Copas) <i>OU</i></li>
  <li><b>Ao Mesmo Número/Figura</b> (Exemplo: 7 sobre 7, Rei sobre Rei).</li>
</ul>

<h3 style='color: #ffe066;'>📥 Passo 3: O que Fazer se Não Tiver Carta Válida?</h3>
<p>Se você não tiver uma carta correspondente para jogar, clique no baralho para <b>comprar 1 carta</b>. Se a carta comprada for válida, você poderá jogá-la imediatamente.</p>

<h3 style='color: #ffe066;'>⚡ Passo 4: Cartas de Efeito Especial</h3>
<ul>
  <li>🃏 <b>Valete (Jack) - Troca de Naipe:</b><br>Pode ser jogado sobre qualquer carta. O jogador que jogar o Valete define o novo naipe para a mesa. (Vale 20 pontos)</li>
  <li>⚡ <b>7 (Sete) - Compra Duas:</b><br>O próximo jogador deve comprar 2 cartas do baralho e perder o turno, a menos que também jogue um 7 (acumulando para 4 cartas).</li>
  <li>🛑 <b>8 (Oito) - Pula Turno:</b><br>Pula a vez do próximo jogador.</li>
  <li>🔄 <b>9 (Nove) - Inverte Sentido:</b><br>Inverte a direção de rotação dos turnos na mesa.</li>
</ul>

<h3 style='color: #ffe066;'>🏆 Passo 5: Pontuação e Vitória na Partida</h3>
<p>No final de cada rodada, o vencedor recebe a soma dos pontos das cartas restantes nas mãos dos oponentes. O primeiro jogador a atingir <b>150 pontos acumulados</b> vence a partida.</p>""",
    },
    "pt_PT": {
        "start_game": "🚀 Iniciar Jogo Agora!",
        "ai_opponents": "Escolha a quantidade de oponentes (1 a 3):",
        "ai_name_label": "Nome do Oponente {i} (IA):",
        "rename": "✏️ Renomear Perfil",
        "history": "📜 Histórico de Jogos",
        "rules": "📖 Regras do Jogo",
        "delete": "🗑️ Eliminar Perfil",
        "new_profile": "+ Criar Novo Perfil…",
        "new_profile_name": "Nome do Novo Perfil de Jogador:",
        "type_name_placeholder": "Escreva o seu nome (por omissão: {default})…",
        "matches": "Partidas Jogadas",
        "wins": "Vitórias Conquistadas",
        "win_rate": "Aproveitamento de Vitórias",
        "record": "Melhor Pontuação",
        "rounds": "rondas",
        "round_sg": "ronda",
        "games": "jogos",
        "game_sg": "jogo",
        "draw_card": "📥 Tirar Carta",
        "round_num": "Ronda {n}",
        "deck_count": "Baralho de Tirar: {c} cartas restantes",
        "deck_count_one": "Baralho de Tirar: 1 carta restante",
        "hand_cards_count": "{c} cartas na mão",
        "hand_cards_count_one": "1 carta na mão",
        "declared_suit": "Naipe ativo na mesa: {s}",
        "draw_stack_alert": "⚠️ Desafio Ativo: {c} cartas pendentes para tirar!",
        "draw_stack_alert_one": "⚠️ Desafio Ativo: 1 carta pendente para tirar!",
        "language": "Idioma / Language",
        "history_title": "Histórico de Partidas de {name}",
        "no_plays_yet": "Nenhuma partida registada ainda para este perfil.",
        "confirm_delete_title": "Confirmar Eliminação de Perfil",
        "confirm_delete_msg": "Tem a certeza que deseja eliminar permanentemente o perfil '{name}'?\nTodas as estatísticas e registos serão apagados.",
        "reset_history": "🧹 Zerar Histórico",
        "confirm_reset_title": "Zerar Histórico de Jogos",
        "confirm_reset_msg": "Tem a certeza que deseja zerar todas as estatísticas e histórico do perfil '{name}'?",
        "rename_title": "Renomear Perfil do Jogador",
        "rename_msg": "Escreva o novo nome para o perfil '{name}':",
        "rename_duplicate": "Não foi possível renomear. Já existe um perfil registado com o nome '{name}'.",
        "points": "pts",
        "first_to_win": "(Primeiro jogador a atingir {score} pts vence!)",
        "msg_starting_card": "🌟 Carta inicial na mesa: {card}",
        "msg_skipped": "🛑 Vez saltada! A vez de {name} foi saltada.",
        "msg_you_chain_penalty": "⚡ Jogaste a carta {card} e repassaste o desafio!",
        "msg_you_played": "✨ Jogaste a carta {card}! Continua!",
        "msg_you_drew_amount": "📥 Tiraste {amount} cartas de penalização do baralho.",
        "msg_you_drew_card": "🎒 Tiraste a carta {card} e guardaste-a na tua mão.",
        "msg_you_drew_kept": "🎒 Tiraste a carta {card} e guardaste-a no teu monte.",
        "msg_ai_draws_amount": "📥 {name} tirou {amount} cartas de penalização do baralho.",
        "msg_ai_draws_card": "🤖 {name} tirou 1 carta do baralho.",
        "msg_ai_plays_drawn": " E jogou a carta {card} imediatamente!",
        "msg_ai_plays": "🤖 {name} jogou a carta {card}.",
        "msg_ai_declares_suit": " 🎨 Escolheu o novo naipe: {suit}",
        "dialog_card_drawn_title": "Carta Jogável Tirada!",
        "dialog_card_drawn_msg": "🎉 Carta especial tirada! Tiraste {card}, que pode ser jogada agora. Desejas jogá-la imediatamente?",
        "dialog_round_over_title": "Ronda Concluída!",
        "dialog_round_over_msg": "🎉 Parabéns! {name} ficou sem cartas e venceu esta ronda com brilho!",
        "dialog_game_over_title": "Grande Campeão da Partida!",
        "dialog_game_over_msg": "🏆 GRANDIOSO CAMPEÃO!\n{name} atingiu a marca de {score} pontos e venceu a partida completa do Mau-Mau! Parabéns pela vitória!",
        "dialog_next_round_title": "Continuar a Jogar?",
        "dialog_next_round_msg": "Desejas iniciar a próxima ronda agora?",
        "rules_title": "Regras do Jogo - Mau-Mau",
        "rules_content": """<h3 style='color: #ffe066;'>📌 Passo 1: Objetivo Principal do Jogo</h3>
<p>O objetivo é descartar todas as cartas da sua mão na mesa antes dos outros jogadores. O primeiro a ficar sem cartas vence a ronda.</p>

<h3 style='color: #ffe066;'>🃏 Passo 2: Como Jogar no Seu Turno</h3>
<p>Observe a carta aberta no centro da mesa. Pode jogar uma carta da sua mão se corresponder a:</p>
<ul>
  <li><b>Ao Mesmo Naipe</b> <i>OU</i></li>
  <li><b>Ao Mesmo Número/Figura</b> (Exemplo: 7 sobre 7, Rei sobre Rei).</li>
</ul>

<h3 style='color: #ffe066;'>📥 Passo 3: O que Fazer se Não Tiver Carta Válida?</h3>
<p>Se não tiver uma carta correspondente para jogar, clique no baralho para <b>tirar 1 carta</b>. Se a carta tirada for válida, poderá jogá-la imediatamente.</p>

<h3 style='color: #ffe066;'>⚡ Passo 4: Cartas de Efeito Especial</h3>
<ul>
  <li>🃏 <b>Valete (Jack) - Troca de Naipe:</b><br>Pode ser jogado sobre qualquer carta. Quem joga o Valete define o novo naipe. (Vale 20 pontos)</li>
  <li>⚡ <b>7 (Sete) - Tira Duas:</b><br>O próximo jogador deve tirar 2 cartas do baralho e perder o turno.</li>
  <li>🛑 <b>8 (Oito) - Salta Turno:</b><br>Salta a vez do próximo jogador.</li>
  <li>🔄 <b>9 (Nove) - Inverte Sentido:</b><br>Inverte a direção da rotação do jogo.</li>
</ul>

<h3 style='color: #ffe066;'>🏆 Passo 5: Pontuação e Vitória na Partida</h3>
<p>No final de cada ronda, o vencedor recebe a soma dos pontos das cartas restantes nas mãos dos oponentes. O primeiro jogador a atingir <b>150 pontos acumulados</b> vence a partida.</p>""",
    },
    "de": {
        "start_game": "🚀 Jetzt Spiel starten!",
        "ai_opponents": "Wähle Anzahl der KI-Gegner (1 bis 3):",
        "ai_name_label": "Name des Gegners {i} (KI):",
        "rename": "✏️ Profil umbenennen",
        "history": "📜 Spielverlauf",
        "rules": "📖 Spielregeln",
        "delete": "🗑️ Profil löschen",
        "new_profile": "+ Neues Profil erstellen…",
        "new_profile_name": "Name des neuen Spielers:",
        "type_name_placeholder": "Name eingeben (Standard: {default})…",
        "matches": "Gespielte Spiele",
        "wins": "Errungene Siege",
        "win_rate": "Erfolgsquote & Siege %",
        "record": "Höchstpunktzahl-Rekord",
        "rounds": "Runden",
        "round_sg": "Runde",
        "games": "Spiele",
        "game_sg": "Spiel",
        "draw_card": "📥 Karte ziehen",
        "round_num": "Runde {n}",
        "deck_count": "Ziehstapel: {c} Karten verbleibend",
        "deck_count_one": "Ziehstapel: 1 Karte verbleibend",
        "hand_cards_count": "{c} Karten auf der Hand",
        "hand_cards_count_one": "1 Karte auf der Hand",
        "declared_suit": "Aktive Farbe auf dem Tisch: {s}",
        "draw_stack_alert": "⚠️ Strafkarten-Herausforderung: {c} Karten ausstehend!",
        "draw_stack_alert_one": "⚠️ Strafkarten-Herausforderung: 1 Karte ausstehend!",
        "language": "Sprache / Language",
        "history_title": "Spielverlauf von {name}",
        "no_plays_yet": "Noch keine Spiele für dieses Profil aufgezeichnet.",
        "confirm_delete_title": "Profil löschen bestätigen",
        "confirm_delete_msg": "Möchten Sie das Profil '{name}' wirklich dauerhaft löschen?\nAlle Statistiken gehen verloren.",
        "reset_history": "🧹 Verlauf zurücksetzen",
        "confirm_reset_title": "Verlauf zurücksetzen",
        "confirm_reset_msg": "Möchten Sie den gesamten Verlauf und die Statistiken des Profils '{name}' zurücksetzen?",
        "rename_title": "Spielerprofil umbenennen",
        "rename_msg": "Neuen Namen für Profil '{name}' eingeben:",
        "rename_duplicate": "Name '{name}' ist bereits vergeben.",
        "points": "Pkt.",
        "first_to_win": "(Wer zuerst {score} Punkte erreicht, gewinnt!)",
        "msg_starting_card": "🌟 Startkarte auf dem Tisch: {card}",
        "msg_skipped": "🛑 Aussetzen! {name} wird übersprungen.",
        "msg_you_chain_penalty": "⚡ Du hast {card} gespielt und die Strafe weitergegeben!",
        "msg_you_played": "✨ Du hast die Karte {card} gespielt! Weiter so!",
        "msg_you_drew_amount": "📥 Du hast {amount} Strafkarten gezogen.",
        "msg_you_drew_card": "🎒 Du hast die Karte {card} gezogen und auf die Hand genommen.",
        "msg_you_drew_kept": "🎒 Du hast die Karte {card} gezogen und behalten.",
        "msg_ai_draws_amount": "📥 {name} hat {amount} Strafkarten gezogen.",
        "msg_ai_draws_card": "🤖 {name} hat 1 Karte gezogen.",
        "msg_ai_plays_drawn": " Und hat {card} sofort ausgespielt!",
        "msg_ai_plays": "🤖 {name} hat Karte {card} gespielt.",
        "msg_ai_declares_suit": " 🎨 Wünscht sich neue Farbe: {suit}",
        "dialog_card_drawn_title": "Spielbare Karte gezogen!",
        "dialog_card_drawn_msg": "🎉 Glück gehabt! Du hast {card} gezogen. Möchtest du diese Karte sofort ausspielen?",
        "dialog_round_over_title": "Runde beendet!",
        "dialog_round_over_msg": "🎉 Herzlichen Glückwunsch! {name} hat alle Karten abgelegt und diese Runde gewonnen!",
        "dialog_game_over_title": "Großer Gesamtsieger!",
        "dialog_game_over_msg": "🏆 GROSSER CHAMPION!\n{name} hat {score} Punkte erreicht und das Mau-Mau-Spiel gewonnen! Herzlichen Glückwunsch!",
        "dialog_next_round_title": "Weiterspielen?",
        "dialog_next_round_msg": "Möchtest du die nächste Runde starten?",
        "rules_title": "Spielregeln - Mau-Mau",
        "rules_content": """<h3 style='color: #ffe066;'>📌 Schritt 1: Hauptziel des Spiels</h3>
<p>Das Ziel ist es, alle Karten von der Hand abzulegen. Wer zuerst keine Karten mehr hat, gewinnt die Runde.</p>

<h3 style='color: #ffe066;'>🃏 Schritt 2: Spielablauf im eigenen Zug</h3>
<p>Sie können eine Karte legen, wenn sie übereinstimmt mit:</p>
<ul>
  <li><b>Gleicher Farbe</b> <i>ODER</i></li>
  <li><b>Gleichem Wert/Zahl</b> (z. B. 7 auf 7, König auf König).</li>
</ul>

<h3 style='color: #ffe066;'>📥 Schritt 3: Keine passende Karte?</h3>
<p>Wenn Sie keine passende Karte haben, ziehen Sie <b>1 Karte vom Stapel</b>. Passt sie, dürfen Sie sie sofort legen.</p>

<h3 style='color: #ffe066;'>⚡ Schritt 4: Sonderkarten mit Effekt</h3>
<ul>
  <li>🃏 <b>Bube - Farbwunsch:</b> Kann auf jede Karte gelegt werden. Bestimmt die neue Farbe. (20 Punkte)</li>
  <li>⚡ <b>7 (Sieben) - Zwei ziehen:</b> Der nächste Spieler muss 2 Karten ziehen und aussetzen, außer er legt auch eine 7.</li>
  <li>🛑 <b>8 (Acht) - Aussetzen:</b> Der nächste Spieler wird übersprungen.</li>
  <li>🔄 <b>9 (Neun) - Richtungswechsel:</b> Ändert die Spielrichtung.</li>
</ul>

<h3 style='color: #ffe066;'>🏆 Schritt 5: Punkte und Gesamtsieg</h3>
<p>Der Gewinner erhält die Punkte aller verbliebenen Karten der Gegner. Wer zuerst <b>150 Punkte</b> erreicht, gewinnt das Spiel.</p>""",
    },
    "nl": {
        "start_game": "🚀 Nu Spelen!",
        "ai_opponents": "Kies aantal AI-tegenstanders (1 tot 3):",
        "ai_name_label": "Naam Tegenstander {i} (AI):",
        "rename": "✏️ Profiel Hernoemen",
        "history": "📜 Wedstrijdgeschiedenis",
        "rules": "📖 Spelregels",
        "delete": "🗑️ Profiel Verwijderen",
        "new_profile": "+ Nieuw Profiel Maken…",
        "new_profile_name": "Naam Nieuwe Speler:",
        "type_name_placeholder": "Typ naam (standaard: {default})…",
        "matches": "Gespelde Wedstrijden",
        "wins": "Behaalde Overwinningen",
        "win_rate": "Winpercentage & Succes",
        "record": "Beste Score Record",
        "rounds": "rondes",
        "round_sg": "ronde",
        "games": "wedstrijden",
        "game_sg": "wedstrijd",
        "draw_card": "📥 Kaart Trekken",
        "round_num": "Ronde {n}",
        "deck_count": "Trekstapel: {c} kaarten over",
        "deck_count_one": "Trekstapel: 1 kaart over",
        "hand_cards_count": "{c} kaarten in hand",
        "hand_cards_count_one": "1 kaart in hand",
        "declared_suit": "Actieve kleur op tafel: {s}",
        "draw_stack_alert": "⚠️ Strafkaarten Uitdaging: {c} kaarten te trekken!",
        "draw_stack_alert_one": "⚠️ Strafkaarten Uitdaging: 1 kaart te trekken!",
        "language": "Taal / Language",
        "history_title": "Wedstrijdgeschiedenis van {name}",
        "no_plays_yet": "Nog geen gespeelde wedstrijden voor dit profiel.",
        "confirm_delete_title": "Profiel Verwijderen Bevestigen",
        "confirm_delete_msg": "Weet u zeker dat u profiel '{name}' wilt verwijderen?",
        "reset_history": "🧹 Geschiedenis wissen",
        "confirm_reset_title": "Geschiedenis wissen",
        "confirm_reset_msg": "Weet u zeker dat u de geschiedenis en statistieken van profiel '{name}' wilt wissen?",
        "rename_title": "Spelersprofiel Hernoemen",
        "rename_msg": "Voer nieuwe naam in voor '{name}':",
        "rename_duplicate": "Profiel '{name}' bestaat al.",
        "points": "ptn",
        "first_to_win": "(Eerste speler die {score} ptn bereikt wint!)",
        "msg_starting_card": "🌟 Startkaart op tafel: {card}",
        "msg_skipped": "🛑 Beurt overgeslagen! {name} slaat een beurt over.",
        "msg_you_chain_penalty": "⚡ Je speelde {card} en gaf de straf door!",
        "msg_you_played": "✨ Je speelde kaart {card}! Ga zo door!",
        "msg_you_drew_amount": "📥 Je trok {amount} strafkaarten.",
        "msg_you_drew_card": "🎒 Je trok kaart {card} en hield deze vast.",
        "msg_you_drew_kept": "🎒 Je trok kaart {card} en bewaarde deze.",
        "msg_ai_draws_amount": "📥 {name} trok {amount} strafkaarten.",
        "msg_ai_draws_card": "🤖 {name} trok 1 kaart.",
        "msg_ai_plays_drawn": " En speelde {card} direct!",
        "msg_ai_plays": "🤖 {name} speelde kaart {card}.",
        "msg_ai_declares_suit": " 🎨 Kiest nieuwe kleur: {suit}",
        "dialog_card_drawn_title": "Speelbare Kaart Getrokken!",
        "dialog_card_drawn_msg": "🎉 Geluk! Je trok {card}. Wil je deze kaart direct spelen?",
        "dialog_round_over_title": "Ronde Afgelopen!",
        "dialog_round_over_msg": "🎉 Gefeliciteerd! {name} heeft alle kaarten weggespeld en deze ronde gewonnen!",
        "dialog_game_over_title": "Grote Kampioen!",
        "dialog_game_over_msg": "🏆 GROTE KAMPIOEN!\n{name} heeft {score} punten behaald en de Mau-Mau wedstrijd gewonnen! Gefeliciteerd!",
        "dialog_next_round_title": "Verder Spelen?",
        "dialog_next_round_msg": "Wil je de volgende ronde starten?",
        "rules_title": "Spelregels - Mau-Mau",
        "rules_content": """<h3 style='color: #ffe066;'>📌 Stap 1: Hoofddoel van het Spel</h3>
<p>Het doel is om al je kaarten af te leggen. Wie als eerste geen kaarten meer heeft, wint de ronde.</p>

<h3 style='color: #ffe066;'>🃏 Stap 2: Hoe speel je in jouw beurt?</h3>
<p>Leg een kaart af die matcht op:</p>
<ul>
  <li><b>Zelfde Kleur</b> <i>OF</i></li>
  <li><b>Zelfde Waarde/Nummer</b> (bijv. 7 op 7, Koning op Koning).</li>
</ul>

<h3 style='color: #ffe066;'>📥 Stap 3: Geen passende kaart?</h3>
<p>Trek <b>1 kaart van de stapel</b>. Als deze past, mag je hem direct spelen.</p>

<h3 style='color: #ffe066;'>⚡ Stap 4: Speciale Effectkaarten</h3>
<ul>
  <li>🃏 <b>Boer - Kleur kiezen:</b> Past op alles. Bepaalt de nieuwe kleur. (20 ptn)</li>
  <li>⚡ <b>7 - Twee trekken:</b> De volgende speler trekt 2 kaarten, tenzij hij ook een 7 speelt.</li>
  <li>🛑 <b>8 - Beurt overslaan:</b> De volgende speler slaat een beurt over.</li>
  <li>🔄 <b>9 - Richting omdraaien:</b> Verandert de speelrichting.</li>
</ul>

<h3 style='color: #ffe066;'>🏆 Stap 5: Punten en Winst</h3>
<p>Wie als eerste <b>150 punten</b> verzamelt, wint het spel.</p>""",
    },
    "pl": {
        "start_game": "🚀 Rozpocznij Grę Teraz!",
        "ai_opponents": "Wybierz liczbę przeciwników SI (1 do 3):",
        "ai_name_label": "Nazwa Przeciwnika {i} (SI):",
        "rename": "✏️ Zmień Nazwę Profilu",
        "history": "📜 Historia Meczów",
        "rules": "📖 Zasady Gry",
        "delete": "🗑️ Usuń Profil",
        "new_profile": "+ Utwórz Nowy Profil…",
        "new_profile_name": "Nazwa Nowego Gracza:",
        "type_name_placeholder": "Wpisz nazwę (domyślnie: {default})…",
        "matches": "Rozegrane Mecze",
        "wins": "Zdobyte Wygrane",
        "win_rate": "Wskaźnik Wygranych %",
        "record": "Najlepszy Wynik",
        "rounds": "rund",
        "round_sg": "runda",
        "games": "meczów",
        "game_sg": "mecz",
        "draw_card": "📥 Dobierz Kartę",
        "round_num": "Runda {n}",
        "deck_count": "Talia: Pozostało {c} kart",
        "deck_count_one": "Talia: Pozostała 1 karta",
        "hand_cards_count": "{c} kart w ręce",
        "hand_cards_count_one": "1 karta w ręce",
        "declared_suit": "Aktywny kolor na stole: {s}",
        "draw_stack_alert": "⚠️ Wyzwanie: Do dobrania {c} kart kary!",
        "draw_stack_alert_one": "⚠️ Wyzwanie: Do dobrania 1 karta kary!",
        "language": "Język / Language",
        "history_title": "Historia Meczów Gracza {name}",
        "no_plays_yet": "Brak zarejestrowanych gier dla tego profilu.",
        "confirm_delete_title": "Potwierdź Usunięcie Profilu",
        "confirm_delete_msg": "Czy na pewno chcesz trwale usunąć profil '{name}'?",
        "reset_history": "🧹 Wyczyszczenie historii",
        "confirm_reset_title": "Wyczyszczenie historii",
        "confirm_reset_msg": "Czy na pewno chcesz wyczyścić historię i statystyki profilu '{name}'?",
        "rename_title": "Zmień Nazwę Gracza",
        "rename_msg": "Wpisz nową nazwę dla '{name}':",
        "rename_duplicate": "Profil o nazwie '{name}' już istnieje.",
        "points": "pkt",
        "first_to_win": "(Pierwszy gracz, który zdobędzie {score} pkt wygrywa!)",
        "msg_starting_card": "🌟 Karta startowa na stole: {card}",
        "msg_skipped": "🛑 Czekaj! {name} traci kolejkę.",
        "msg_you_chain_penalty": "⚡ Zagrałeś {card} i przekazałeś karę!",
        "msg_you_played": "✨ Zagrałeś kartę {card}! O tak!",
        "msg_you_drew_amount": "📥 Dobrałeś {amount} kart kary.",
        "msg_you_drew_card": "🎒 Dobrałeś kartę {card} i zachowałeś ją w ręce.",
        "msg_you_drew_kept": "🎒 Dobrałeś kartę {card} i zatrzymałeś ją.",
        "msg_ai_draws_amount": "📥 {name} dobrał {amount} kart kary.",
        "msg_ai_draws_card": "🤖 {name} dobrał 1 kartę.",
        "msg_ai_plays_drawn": " I zagrał kartę {card} natychmiast!",
        "msg_ai_plays": "🤖 {name} zagrał kartę {card}.",
        "msg_ai_declares_suit": " 🎨 Wybrał nowy kolor: {suit}",
        "dialog_card_drawn_title": "Szczęśliwe Dobranie!",
        "dialog_card_drawn_msg": "🎉 Szczęśliwe dobranie! Dobrałeś {card}. Czy chcesz zagrać ją natychmiast?",
        "dialog_round_over_title": "Runda Zakończona!",
        "dialog_round_over_msg": "🎉 Gratulacje! {name} pozbył się wszystkich kart i wygrał tę rundę!",
        "dialog_game_over_title": "Wielki Mistrz!",
        "dialog_game_over_msg": "🏆 WIELKI MISTRZ!\n{name} zdobył {score} punktów i wygrał cały mecz Mau-Mau! Gratulacje!",
        "dialog_next_round_title": "Grasz Dalej?",
        "dialog_next_round_msg": "Czy chcesz rozpocząć następną rundę?",
        "rules_title": "Zasady Gry - Mau-Mau",
        "rules_content": """<h3 style='color: #ffe066;'>📌 Krok 1: Główny cel gry</h3>
<p>Celem jest pozbycie się wszystkich kart z ręki. Kto pierwszy pozbędzie się kart, wygrywa rundę.</p>

<h3 style='color: #ffe066;'>🃏 Krok 2: Przebieg kolejki</h3>
<p>Zagrywaj kartę pasującą:</p>
<ul>
  <li><b>Kolorem</b> <i>LUB</i></li>
  <li><b>Figurą/Numerem</b> (np. 7 na 7, Król na Króla).</li>
</ul>

<h3 style='color: #ffe066;'>📥 Krok 3: Brak pasującej karty?</h3>
<p>Dobierz <b>1 kartę z talii</b>. Jeśli pasuje, możesz ją od razu zagrać.</p>

<h3 style='color: #ffe066;'>⚡ Krok 4: Karty Specjalne</h3>
<ul>
  <li>🃏 <b>Walet - Zmiana koloru:</b> Pasuje na wszystko i wybiera nowy kolor. (20 pkt)</li>
  <li>⚡ <b>7 - Dobierz dwie:</b> Następny gracz dobiera 2 karty i traci kolejkę.</li>
  <li>🛑 <b>8 - Czekaj:</b> Następny gracz traci kolejkę.</li>
  <li>🔄 <b>9 - Zmiana kierunku:</b> Odwraca kierunek gry.</li>
</ul>

<h3 style='color: #ffe066;'>🏆 Krok 5: Punktacja i wygrana</h3>
<p>Gracz, który jako pierwszy zdobędzie <b>150 punktów</b>, wygrywa mecz.</p>""",
    },
    "cs": {
        "start_game": "🚀 Spustit Hru Hned!",
        "ai_opponents": "Zvolte počet soupeřů AI (1 až 3):",
        "ai_name_label": "Jméno Soupeře {i} (AI):",
        "rename": "✏️ Přejmenovat Profil",
        "history": "📜 Historie Zápasů",
        "rules": "📖 Pravidla Hry",
        "delete": "🗑️ Smazat Profil",
        "new_profile": "+ Vytvořit Nový Profil…",
        "new_profile_name": "Jméno Nového Hráče:",
        "type_name_placeholder": "Zadejte jméno (výchozí: {default})…",
        "matches": "Odehrané Zápasy",
        "wins": "Získané Výhry",
        "win_rate": "Míra Úspěšnosti %",
        "record": "Nejlepší Skóre",
        "rounds": "kol",
        "round_sg": "kolo",
        "games": "zápasů",
        "game_sg": "zápas",
        "draw_card": "📥 Lízat Kartu",
        "round_num": "Kolo {n}",
        "deck_count": "Balíček: Zbývá {c} karet",
        "deck_count_one": "Balíček: Zbývá 1 karta",
        "hand_cards_count": "{c} karet v ruce",
        "hand_cards_count_one": "1 karta v ruce",
        "declared_suit": "Aktivní barva na stole: {s}",
        "draw_stack_alert": "⚠️ Trestná Výzva: K líznutí {c} karet!",
        "draw_stack_alert_one": "⚠️ Trestná Výzva: K líznutí 1 karta!",
        "language": "Jazyk / Language",
        "history_title": "Historie Zápasů Hráče {name}",
        "no_plays_yet": "Zatím nebyly zaznamenány žádné hry pro tento profil.",
        "confirm_delete_title": "Potvrdit Smazání Profilu",
        "confirm_delete_msg": "Opravdu chcete trvale smazat profil '{name}'?",
        "reset_history": "🧹 Vynulovat historii",
        "confirm_reset_title": "Vynulovat historii",
        "confirm_reset_msg": "Opravdu chcete vynulovat historii a statistiky profilu '{name}'?",
        "rename_title": "Přejmenovat Hráče",
        "rename_msg": "Zadejte nové jméno pro '{name}':",
        "rename_duplicate": "Profil se jménem '{name}' již existuje.",
        "points": "b.",
        "first_to_win": "(První hráč, který dosáhne {score} b. vyhrává!)",
        "msg_starting_card": "🌟 Startovní karta na stole: {card}",
        "msg_skipped": "🛑 Stojíš! {name} nehraje.",
        "msg_you_chain_penalty": "⚡ Zahrál jsi {card} a předal trest!",
        "msg_you_played": "✨ Zahrál jsi kartu {card}! Jen tak dál!",
        "msg_you_drew_amount": "📥 Líznul jsi {amount} trestných karet.",
        "msg_you_drew_card": "🎒 Líznul jsi kartu {card} a nechal si ji v ruce.",
        "msg_you_drew_kept": "🎒 Líznul jsi kartu {card} a schoval ji.",
        "msg_ai_draws_amount": "📥 {name} líznul {amount} trestných karet.",
        "msg_ai_draws_card": "🤖 {name} líznul 1 kartu.",
        "msg_ai_plays_drawn": " A ihned zahrál kartu {card}!",
        "msg_ai_plays": "🤖 {name} zahrál kartu {card}.",
        "msg_ai_declares_suit": " 🎨 Zvolil novou barvu: {suit}",
        "dialog_card_drawn_title": "Šťastné Líznutí!",
        "dialog_card_drawn_msg": "🎉 Šťastné líznutí! Líznul jsi {card}. Chceš ji ihned zahrát?",
        "dialog_round_over_title": "Kolo Dokončeno!",
        "dialog_round_over_msg": "🎉 Gratulujeme! {name} odhodil všechny karty a vyhrál toto kolo!",
        "dialog_game_over_title": "Velký Šampion!",
        "dialog_game_over_msg": "🏆 VELKÝ ŠAMPION!\n{name} dosáhl {score} bodů a vyhrál celý zápas Mau-Mau! Gratulujeme!",
        "dialog_next_round_title": "Hrát Dál?",
        "dialog_next_round_msg": "Chceš spustit další kolo?",
        "rules_title": "Pravidla Hry - Mau-Mau",
        "rules_content": """<h3 style='color: #ffe066;'>📌 Krok 1: Hlavní cíl hry</h3>
<p>Cílem je odhodit všechny karty z ruky. Kdo první nemá karty, vyhrává kolo.</p>

<h3 style='color: #ffe066;'>🃏 Krok 2: Jak hrát v tahu?</h3>
<p>Zahrajte kartu stejné:</p>
<ul>
  <li><b>Barvy</b> <i>NEBO</i></li>
  <li><b>Hodnoty/Císla</b> (např. 7 na 7, Král na Krále).</li>
</ul>

<h3 style='color: #ffe066;'>📥 Krok 3: Nemáte kartu?</h3>
<p>Lízněte si <b>1 kartu z balíčku</b>. Pokud pasuje, můžete ji hned zahrát.</p>

<h3 style='color: #ffe066;'>⚡ Krok 4: Speciální karty</h3>
<ul>
  <li>🃏 <b>Kluk - Změna barvy:</b> Lze zahrát na cokoliv a určí novou barvu. (20 b.)</li>
  <li>⚡ <b>7 - Ber dvě:</b> Další hráč bere 2 karty a nehraje.</li>
  <li>🛑 <b>8 - Stojíš:</b> Další hráč nehraje.</li>
  <li>🔄 <b>9 - Změna směru:</b> Mění směr hry.</li>
</ul>

<h3 style='color: #ffe066;'>🏆 Krok 5: Bodování a výhra</h3>
<p>Kdo dosáhne <b>150 bodů</b> jako první, vyhrává zápas.</p>""",
    },
    "hu": {
        "start_game": "🚀 Játék Indítása Most!",
        "ai_opponents": "Válassz AI ellenfelek számát (1 és 3 között):",
        "ai_name_label": "Ellenfele {i} Neve (AI):",
        "rename": "✏️ Profil Átnevezése",
        "history": "📜 Mérkőzés Előzmények",
        "rules": "📖 Játékszabályok",
        "delete": "🗑️ Profil Törlése",
        "new_profile": "+ Új Profil Létrehozása…",
        "new_profile_name": "Új Játékos Neve:",
        "type_name_placeholder": "Írj be egy nevet (alapértelmezett: {default})…",
        "matches": "Lejátszott Mérkőzések",
        "wins": "Elért Győzelmek",
        "win_rate": "Győzelmi Arány %",
        "record": "Legjobb Pontszám",
        "rounds": "menet",
        "round_sg": "menet",
        "games": "mérkőzés",
        "game_sg": "mérkőzés",
        "draw_card": "📥 Kártya Húzása",
        "round_num": "Menet {n}",
        "deck_count": "Húzópakli: {c} kártya maradt",
        "deck_count_one": "Húzópakli: 1 kártya maradt",
        "hand_cards_count": "{c} kártya a kézben",
        "hand_cards_count_one": "1 kártya a kézben",
        "declared_suit": "Aktív szín az asztalon: {s}",
        "draw_stack_alert": "⚠️ Büntetés Kihívás: {c} kártya húzandó!",
        "draw_stack_alert_one": "⚠️ Büntetés Kihívás: 1 kártya húzandó!",
        "language": "Nyelv / Language",
        "history_title": "{name} Mérkőzés Előzményei",
        "no_plays_yet": "Még nincsenek rögzített játékok ehhez a profilhoz.",
        "confirm_delete_title": "Profil Törlésének Megerősítése",
        "confirm_delete_msg": "Biztosan törölni szeretnéd a(z) '{name}' profilját?",
        "reset_history": "🧹 Előzmények törlése",
        "confirm_reset_title": "Előzmények törlése",
        "confirm_reset_msg": "Biztosan törölni szeretné a(z) '{name}' profil összes előzményét és statisztikáját?",
        "rename_title": "Játékos Profil Átnevezése",
        "rename_msg": "Új név a(z) '{name}' profilhoz:",
        "rename_duplicate": "Már létezik '{name}' nevű profil.",
        "points": "pont",
        "first_to_win": "(Az nyeri a játékot, aki először éri el a {score} pontot!)",
        "msg_starting_card": "🌟 Kezdőkártya az asztalon: {card}",
        "msg_skipped": "🛑 Kimaradsz! {name} kimarad a körből.",
        "msg_you_chain_penalty": "⚡ Kijátszottad a(z) {card} lapot és továbbadtad a büntetést!",
        "msg_you_played": "✨ Kijátszottad a(z) {card} lapot! Csak így tovább!",
        "msg_you_drew_amount": "📥 Húztál {amount} büntetőkártyát.",
        "msg_you_drew_card": "🎒 Húztad a(z) {card} lapot és megtartottad.",
        "msg_you_drew_kept": "🎒 Húztad a(z) {card} lapot és elrakad.",
        "msg_ai_draws_amount": "📥 {name} húzott {amount} büntetőkártyát.",
        "msg_ai_draws_card": "🤖 {name} húzott 1 kártyát.",
        "msg_ai_plays_drawn": " És azonnal kijátszotta a(z) {card} lapot!",
        "msg_ai_plays": "🤖 {name} kijátszotta: {card}.",
        "msg_ai_declares_suit": " 🎨 Új színt kért: {suit}",
        "dialog_card_drawn_title": "Szerencsés Húzás!",
        "dialog_card_drawn_msg": "🎉 Szerencsés húzás! A(z) {card} lapot húztad. Kijátszod azonnal?",
        "dialog_round_over_title": "Menet Befejeződött!",
        "dialog_round_over_msg": "🎉 Gratulálunk! {name} letette az összes kártyáját és megnyerte ezt a menetet!",
        "dialog_game_over_title": "Nagy Bajnok!",
        "dialog_game_over_msg": "🏆 NAGY BAJNOK!\n{name} elérte a(z) {score} pontot és megnyerte a Mau-Mau mérkőzést! Gratulálunk!",
        "dialog_next_round_title": "Folytatod a Játékot?",
        "dialog_next_round_msg": "Indítod a következő menetet?",
        "rules_title": "Játékszabályok - Mau-Mau",
        "rules_content": """<h3 style='color: #ffe066;'>📌 1. Lépés: A játék célja</h3>
<p>A cél az összes kártya letétele. Aki először leteszi a lapjait, megnyeri a menetet.</p>

<h3 style='color: #ffe066;'>🃏 2. Lépés: Hogyan játssz?</h3>
<p>Tegyél le azonos:</p>
<ul>
  <li><b>Színű</b> <i>VAGY</i></li>
  <li><b>Értékű</b> kártyát (pl. 7-est 7-esre).</li>
</ul>

<h3 style='color: #ffe066;'>📥 3. Lépés: Nincs kártyád?</h3>
<p>Húzz <b>1 kártyát a pakliból</b>. Ha jó, azonnal leteheted.</p>

<h3 style='color: #ffe066;'>⚡ 4. Lépés: Speciális kártyák</h3>
<ul>
  <li>🃏 <b>Bubi - Színváltó:</b> Bármire letehető, új színt kérhetsz. (20 pont)</li>
  <li>⚡ <b>7-es - Húzz kettőt:</b> A következő játékos 2 lapot húz.</li>
  <li>🛑 <b>8-as - Kimaradsz:</b> A következő játékos kimarad.</li>
  <li>🔄 <b>9-es - Irányváltás:</b> Megfordítja a játék irányát.</li>
</ul>

<h3 style='color: #ffe066;'>🏆 5. Lépés: Pontszámítás és győzelem</h3>
<p>Aki először éri el a <b>150 pontot</b>, megnyeri a mérkőzést.</p>""",
    },
    "es": {
        "start_game": "🚀 ¡Iniciar Juego Ahora!",
        "ai_opponents": "Elige la cantidad de oponentes (1 a 3):",
        "ai_name_label": "Nombre del Oponente {i} (IA):",
        "rename": "✏️ Renombrar Perfil",
        "history": "📜 Historial de Partidas",
        "rules": "📖 Reglas del Juego",
        "delete": "🗑️ Eliminar Perfil",
        "new_profile": "+ Crear Nuevo Perfil…",
        "new_profile_name": "Nombre del Nuevo Jugador:",
        "type_name_placeholder": "Escribe tu nombre (por defecto: {default})…",
        "matches": "Partidas Jugadas",
        "wins": "Victorias Conseguidas",
        "win_rate": "Tasa de Éxito & Victorias",
        "record": "Mejor Puntuación",
        "rounds": "rondas",
        "round_sg": "ronda",
        "games": "juegos",
        "game_sg": "juego",
        "draw_card": "📥 Robar Carta",
        "round_num": "Ronda {n}",
        "deck_count": "Mazo de Robo: {c} cartas restantes",
        "deck_count_one": "Mazo de Robo: 1 carta restante",
        "hand_cards_count": "{c} cartas en mano",
        "hand_cards_count_one": "1 carta en mano",
        "declared_suit": "Palo activo en la mesa: {s}",
        "draw_stack_alert": "⚠️ Desafío Activo: ¡{c} cartas pendientes para robar!",
        "draw_stack_alert_one": "⚠️ Desafío Activo: ¡1 carta pendiente para robar!",
        "language": "Idioma / Language",
        "history_title": "Historial de Partidas de {name}",
        "no_plays_yet": "No hay partidas registradas aún para este perfil.",
        "confirm_delete_title": "Confirmar Eliminación de Perfil",
        "confirm_delete_msg": "¿Seguro que deseas eliminar permanentemente el perfil '{name}'?",
        "reset_history": "🧹 Reiniciar Historial",
        "confirm_reset_title": "Reiniciar Historial",
        "confirm_reset_msg": "¿Seguro que deseas reiniciar todo el historial y estadísticas del perfil '{name}'?",
        "rename_title": "Renombrar Perfil de Jugador",
        "rename_msg": "Ingresa el nuevo nombre para el perfil '{name}':",
        "rename_duplicate": "Ya existe un perfil registrado con el nombre '{name}'.",
        "points": "pts",
        "first_to_win": "(¡El primer jugador en alcanzar {score} pts gana!)",
        "msg_starting_card": "🌟 Carta inicial en la mesa: {card}",
        "msg_skipped": "🛑 Turno saltado! Se salta a {name}.",
        "msg_you_chain_penalty": "⚡ ¡Jugaste {card} y pasaste el desafío de robar!",
        "msg_you_played": "✨ ¡Jugaste la carta {card}! ¡Sigue así!",
        "msg_you_drew_amount": "📥 Robaste {amount} cartas de castigo del mazo.",
        "msg_you_drew_card": "🎒 Robaste la carta {card} y la guardaste en tu mano.",
        "msg_you_drew_kept": "🎒 Robaste la carta {card} y la guardaste.",
        "msg_ai_draws_amount": "📥 {name} robó {amount} cartas de castigo del mazo.",
        "msg_ai_draws_card": "🤖 {name} robó 1 carta del mazo.",
        "msg_ai_plays_drawn": " ¡Y jugó la carta {card} inmediatamente!",
        "msg_ai_plays": "🤖 {name} jugó la carta {card}.",
        "msg_ai_declares_suit": " 🎨 Eligió nuevo palo: {suit}",
        "dialog_card_drawn_title": "¡Carta Jugable Robada!",
        "dialog_card_drawn_msg": "🎉 ¡Carta especial robada! Robaste {card}, que se puede jugar. ¿Deseas jugarla inmediatamente?",
        "dialog_round_over_title": "¡Ronda Completada!",
        "dialog_round_over_msg": "🎉 ¡Felicitaciones! ¡{name} se quedó sin cartas y ganó esta ronda con éxito!",
        "dialog_game_over_title": "¡Gran Campeón del Juego!",
        "dialog_game_over_msg": "🏆 ¡GRAN CAMPEÓN!\n¡{name} alcanzó {score} puntos y ganó la partida completa de Mau-Mau! ¡Felicitaciones por la victoria!",
        "dialog_next_round_title": "¿Continuar Jugando?",
        "dialog_next_round_msg": "¿Deseas iniciar la siguiente ronda ahora?",
        "rules_title": "Reglas del Juego - Mau-Mau",
        "rules_content": """<h3 style='color: #ffe066;'>📌 Paso 1: Objetivo Principal</h3>
<p>El objetivo es descartar todas las cartas de tu mano antes que los demás jugadores. El primero en quedarse sin cartas gana la ronda.</p>

<h3 style='color: #ffe066;'>🃏 Paso 2: ¿Cómo Jugar en tu Turno?</h3>
<p>Juega una carta que coincida en:</p>
<ul>
  <li><b>Mismo Palo</b> <i>O</i></li>
  <li><b>Mismo Número/Valor</b> (ejemplo: 7 sobre 7, Rey sobre Rey).</li>
</ul>

<h3 style='color: #ffe066;'>📥 Paso 3: ¿Qué hacer si no tienes carta válida?</h3>
<p>Pulsa en el mazo para <b>robar 1 carta</b>. Si sirve, puedes jugarla inmediatamente.</p>

<h3 style='color: #ffe066;'>⚡ Paso 4: Cartas de Efecto Especial</h3>
<ul>
  <li>🃏 <b>Sota (Jack) - Cambiar Palo:</b> Se puede jugar sobre cualquier carta. Elige el nuevo palo de la mesa. (20 pts)</li>
  <li>⚡ <b>7 (Siete) - Roba Dos:</b> El siguiente jugador roba 2 cartas y pierde el turno.</li>
  <li>🛑 <b>8 (Ocho) - Salta Turno:</b> Salta al siguiente jugador.</li>
  <li>🔄 <b>9 (Nueve) - Invertir Sentido:</b> Invierte la dirección del juego.</li>
</ul>

<h3 style='color: #ffe066;'>🏆 Paso 5: Puntuación y Victoria</h3>
<p>El primer jugador en acumular <b>150 puntos</b> gana el juego completo.</p>""",
    },
    "fr": {
        "start_game": "🚀 Jouer Maintenant !",
        "ai_opponents": "Choisissez le nombre d'adversaires (1 à 3) :",
        "ai_name_label": "Nom de l'Adversaire {i} (IA) :",
        "rename": "✏️ Renommer Profil",
        "history": "📜 Historique des Parties",
        "rules": "📖 Règles du Jeu",
        "delete": "🗑️ Supprimer Profil",
        "new_profile": "+ Créer Nouveau Profil…",
        "new_profile_name": "Nom du Nouveau Joueur :",
        "type_name_placeholder": "Entrez votre nom (par défaut : {default})…",
        "matches": "Parties Jouées",
        "wins": "Victoires Remportées",
        "win_rate": "Taux de Réussite %",
        "record": "Meilleur Score Record",
        "rounds": "manches",
        "round_sg": "manche",
        "games": "parties",
        "game_sg": "partie",
        "draw_card": "📥 Piocher une Carte",
        "round_num": "Manche {n}",
        "deck_count": "Pioche : {c} cartes restantes",
        "deck_count_one": "Pioche : 1 carte restante",
        "hand_cards_count": "{c} cartes en main",
        "hand_cards_count_one": "1 carte en main",
        "declared_suit": "Couleur active sur la table : {s}",
        "draw_stack_alert": "⚠️ Défi Pénalité : {c} cartes à piocher !",
        "draw_stack_alert_one": "⚠️ Défi Pénalité : 1 carte à piocher !",
        "language": "Langue / Language",
        "history_title": "Historique des Parties de {name}",
        "no_plays_yet": "Aucune partie enregistrée pour ce profil.",
        "confirm_delete_title": "Confirmer Supprimer Profil",
        "confirm_delete_msg": "Voulez-vous vraiment supprimer définitivement le profil '{name}' ?",
        "reset_history": "🧹 Réinitialiser l'historique",
        "confirm_reset_title": "Réinitialiser l'historique",
        "confirm_reset_msg": "Voulez-vous vraiment réinitialiser l'historique et les statistiques du profil '{name}' ?",
        "rename_title": "Renommer Profil Joueur",
        "rename_msg": "Entrez le nouveau nom pour le profil '{name}' :",
        "rename_duplicate": "Un profil nommé '{name}' existe déjà.",
        "points": "pts",
        "first_to_win": "(Le premier joueur à atteindre {score} pts gagne !)",
        "msg_starting_card": "🌟 Carte de départ sur la table : {card}",
        "msg_skipped": "🛑 Tour passé ! {name} passe son tour.",
        "msg_you_chain_penalty": "⚡ Vous avez joué {card} et transmis le défi !",
        "msg_you_played": "✨ Vous avez joué la carte {card} ! Continuez comme ça !",
        "msg_you_drew_amount": "📥 Vous avez pioché {amount} cartes de pénalité.",
        "msg_you_drew_card": "🎒 Vous avez pioché la carte {card} et l'avez gardée en main.",
        "msg_you_drew_kept": "🎒 Vous avez pioché la carte {card} et l'avez gardée.",
        "msg_ai_draws_amount": "📥 {name} a pioché {amount} cartes de pénalité.",
        "msg_ai_draws_card": "🤖 {name} a pioché 1 carte.",
        "msg_ai_plays_drawn": " Et a joué la carte {card} immédiatement !",
        "msg_ai_plays": "🤖 {name} a joué la carte {card}.",
        "msg_ai_declares_suit": " 🎨 a choisi la nouvelle couleur : {suit}",
        "dialog_card_drawn_title": "Carte Jouable Piochée !",
        "dialog_card_drawn_msg": "🎉 Chance ! Vous avez pioché {card}, qui est jouable. Souhaitez-vous la jouer immédiatement ?",
        "dialog_round_over_title": "Manche Terminée !",
        "dialog_round_over_msg": "🎉 Félicitations ! {name} a posé toutes ses cartes et gagne cette manche !",
        "dialog_game_over_title": "Grand Champion !",
        "dialog_game_over_msg": "🏆 GRAND CHAMPION !\n{name} a atteint {score} points et remporte la partie complète de Mau-Mau ! Félicitations !",
        "dialog_next_round_title": "Continuer à Jouer ?",
        "dialog_next_round_msg": "Souhaitez-vous démarrer la manche suivante ?",
        "rules_title": "Règles du Jeu - Mau-Mau",
        "rules_content": """<h3 style='color: #ffe066;'>📌 Étape 1 : But Principal du Jeu</h3>
<p>Le but est de poser toutes ses cartes. Le premier à poser toutes ses cartes remporte la manche.</p>

<h3 style='color: #ffe066;'>🃏 Étape 2 : Déroulement d'un Tour</h3>
<p>Posez une carte correspondant à :</p>
<ul>
  <li><b>Même Couleur</b> <i>OU</i></li>
  <li><b>Même Valeur/Hauteur</b> (ex. 7 sur 7, Roi sur Roi).</li>
</ul>

<h3 style='color: #ffe066;'>📥 Étape 3 : Que faire sans carte jouable ?</h3>
<p>Piochez <b>1 carte</b>. Si elle est jouable, vous pouvez la poser immédiatement.</p>

<h3 style='color: #ffe066;'>⚡ Étape 4 : Cartes à Effet Spécial</h3>
<ul>
  <li>🃏 <b>Valet - Changer de couleur :</b> Se joue sur tout. Choisit la nouvelle couleur. (20 pts)</li>
  <li>⚡ <b>7 - Pioche deux :</b> Le joueur suivant pioche 2 cartes et passe son tour.</li>
  <li>🛑 <b>8 - Passe ton tour :</b> Le joueur suivant passe son tour.</li>
  <li>🔄 <b>9 - Changement de sens :</b> Inverse le sens du jeu.</li>
</ul>

<h3 style='color: #ffe066;'>🏆 Étape 5 : Score et Victoire</h3>
<p>Le premier joueur à atteindre <b>150 points</b> remporte la partie.</p>""",
    },
    "it": {
        "start_game": "🚀 Gioca Ora!",
        "ai_opponents": "Scegli il numero di avversari IA (da 1 a 3):",
        "ai_name_label": "Nome Avversario {i} (IA):",
        "rename": "✏️ Rinomina Profilo",
        "history": "📜 Cronologia Partite",
        "rules": "📖 Regole del Gioco",
        "delete": "🗑️ Elimina Profilo",
        "new_profile": "+ Crea Nuovo Profilo…",
        "new_profile_name": "Nome del Nuovo Giocatore:",
        "type_name_placeholder": "Inserisci il tuo nome (predefinito: {default})…",
        "matches": "Partite Giocate",
        "wins": "Vittorie Conquistate",
        "win_rate": "Tasso di Successo %",
        "record": "Miglior Punteggio",
        "rounds": "turni",
        "round_sg": "turno",
        "games": "partite",
        "game_sg": "partita",
        "draw_card": "📥 Gioca Ora",
        "round_num": "Turno {n}",
        "deck_count": "Mazzo di Pesca: {c} carte rimaste",
        "deck_count_one": "Mazzo di Pesca: 1 carta rimasta",
        "hand_cards_count": "{c} carte in mano",
        "hand_cards_count_one": "1 carta in mano",
        "declared_suit": "Seme attivo sul tavolo: {s}",
        "draw_stack_alert": "⚠️ Sfida Penalità: {c} carte da pescare!",
        "draw_stack_alert_one": "⚠️ Sfida Penalità: 1 carta da pescare!",
        "language": "Lingua / Language",
        "history_title": "Cronologia Partite di {name}",
        "no_plays_yet": "Nessuna partita registrata per questo profilo.",
        "confirm_delete_title": "Conferma Eliminazione Profilo",
        "confirm_delete_msg": "Sei sicuro di voler eliminare permanentemente il profilo '{name}'?",
        "reset_history": "🧹 Azzera cronologia",
        "confirm_reset_title": "Azzera cronologia",
        "confirm_reset_msg": "Sei sicuro di voler azzerare tutta la cronologia e le statistiche del profilo '{name}'?",
        "rename_title": "Rinomina Profilo Giocatore",
        "rename_msg": "Inserisci il nuovo nome per il profilo '{name}':",
        "rename_duplicate": "Un profilo chiamato '{name}' esiste già.",
        "points": "pt",
        "first_to_win": "(Il primo giocatore che raggiunge {score} pt vince!)",
        "msg_starting_card": "🌟 Carta iniziale sul tavolo: {card}",
        "msg_skipped": "🛑 Turno saltato! {name} salta il turno.",
        "msg_you_chain_penalty": "⚡ Hai giocato {card} e accumulato la penalità!",
        "msg_you_played": "✨ Hai giocato la carta {card}! Continua così!",
        "msg_you_drew_amount": "📥 Hai pescato {amount} carte di penalità.",
        "msg_you_drew_card": "🎒 Hai pescato la carta {card} e l'hai tenuta in mano.",
        "msg_you_drew_kept": "🎒 Hai pescato la carta {card} e l'hai salvata.",
        "msg_ai_draws_amount": "📥 {name} ha pescato {amount} carte di penalità.",
        "msg_ai_draws_card": "🤖 {name} ha pescato 1 carta.",
        "msg_ai_plays_drawn": " E ha giocato la carta {card} subito!",
        "msg_ai_plays": "🤖 {name} ha giocato la carta {card}.",
        "msg_ai_declares_suit": " 🎨 ha scelto il nuovo seme: {suit}",
        "dialog_card_drawn_title": "Carta Giocabile Pescata!",
        "dialog_card_drawn_msg": "🎉 Fortunato! Hai pescato {card}, che è giocabile. Vuoi giocarla subito?",
        "dialog_round_over_title": "Turno Concluso!",
        "dialog_round_over_msg": "🎉 Congratulazioni! {name} ha scartato tutte le carte e vince questo turno!",
        "dialog_game_over_title": "Grande Campione!",
        "dialog_game_over_msg": "🏆 GRANDE CAMPIONE!\n{name} ha raggiunto {score} punti e vince la partita completa di Mau-Mau! Congratulazioni!",
        "dialog_next_round_title": "Continuare a Giocare?",
        "dialog_next_round_msg": "Vuoi iniziare il prossimo turno?",
        "rules_title": "Regole del Gioco - Mau-Mau",
        "rules_content": """<h3 style='color: #ffe066;'>📌 Passo 1: Obiettivo Principale</h3>
<p>L'obiettivo è scartare tutte le carte dalla mano. Il primo che rimane senza carte vince il turno.</p>

<h3 style='color: #ffe066;'>🃏 Passo 2: Come Giocare nel Proprio Turno</h3>
<p>Gioca una carta che corrisponde per:</p>
<ul>
  <li><b>Stesso Seme</b> <i>OPPURE</i></li>
  <li><b>Stesso Valore/Numero</b> (es. 7 su 7, Re su Re).</li>
</ul>

<h3 style='color: #ffe066;'>📥 Passo 3: Se non hai una carta valida?</h3>
<p>Pesca <b>1 carta dal mazzo</b>. Se è valida, puoi giocarla subito.</p>

<h3 style='color: #ffe066;'>⚡ Passo 4: Carte a Effetto Speciale</h3>
<ul>
  <li>🃏 <b>Fante (Jack) - Cambia Seme:</b> Si gioca su qualsiasi carta. Sceglie il nuovo seme del tavolo. (20 pt)</li>
  <li>⚡ <b>7 - Pesca Due:</b> Il giocatore successivo pesca 2 carte e salta il turno.</li>
  <li>🛑 <b>8 - Salta Turno:</b> Il giocatore successivo salta il turno.</li>
  <li>🔄 <b>9 - Inverti Giro:</b> Inverte la direzione del gioco.</li>
</ul>

<h3 style='color: #ffe066;'>🏆 Passo 5: Punteggio e Vittoria</h3>
<p>Il primo giocatore a raggiungere <b>150 punti</b> vince la partita.</p>""",
    },
}


def t(key: str, lang: str = DEFAULT_LANGUAGE, **kwargs: Any) -> str:
    """Retrieve localized string for *key* in language *lang* with optional format placeholders."""
    actual_lang = "pt_BR" if lang == "pt" else lang
    lang_dict = TRANSLATIONS.get(actual_lang, TRANSLATIONS.get(DEFAULT_LANGUAGE, {}))
    template = lang_dict.get(key) or TRANSLATIONS[DEFAULT_LANGUAGE].get(key, key)
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template


def pluralize(count: int, singular_key: str, plural_key: str, lang: str = DEFAULT_LANGUAGE, **kwargs: Any) -> str:
    """Return singular or plural localized string based on count."""
    key = singular_key if count == 1 else plural_key
    return t(key, lang, c=count, n=count, count=count, **kwargs)
