// Mau-Mau Web Client Application Script
let currentSession = null;
let currentTranslations = {};
let pendingCardPlay = null;

// DOM Elements
const viewSetup = document.getElementById('view-setup');
const viewGame = document.getElementById('view-game');
const btnStart = document.getElementById('btn-start');
const btnDraw = document.getElementById('btn-draw');
const btnRules = document.getElementById('btn-rules');
const btnStats = document.getElementById('btn-stats');
const btnResetStats = document.getElementById('btn-reset-stats');
const langSelector = document.getElementById('lang-selector');

const playerNameInput = document.getElementById('player-name-input');
const aiCountSelect = document.getElementById('ai-count-select');
const opponentsContainer = document.getElementById('opponents-container');
const playerHandContainer = document.getElementById('player-hand');
const topCardSlot = document.getElementById('top-card');
const deckCountBadge = document.getElementById('deck-count-badge');
const drawDeck = document.getElementById('draw-deck');
const statusNarration = document.getElementById('status-narration');
const suitIndicator = document.getElementById('suit-indicator');

const modalRules = document.getElementById('modal-rules');
const modalStats = document.getElementById('modal-stats');
const modalSuit = document.getElementById('modal-suit');
const rulesBody = document.getElementById('rules-body');
const statsBody = document.getElementById('stats-body');

// Initialize App
document.addEventListener('DOMContentLoaded', async () => {
  await loadLanguages();
  setupEventListeners();
});

async function loadLanguages() {
  try {
    const res = await fetch('/api/languages');
    const data = await res.json();
    
    langSelector.innerHTML = '';
    for (const [code, info] of Object.entries(data.languages)) {
      const opt = document.createElement('option');
      opt.value = code;
      opt.textContent = `${info.country} — ${info.name}`;
      if (code === data.current) opt.selected = true;
      langSelector.appendChild(opt);
    }

    await fetchTranslations(data.current);
  } catch (err) {
    console.error('Failed loading languages:', err);
  }
}

async function fetchTranslations(langCode) {
  try {
    const res = await fetch(`/api/translations?lang=${langCode}`);
    const data = await res.json();
    currentTranslations = data.translations;
    applyTranslations();
  } catch (err) {
    console.error('Failed loading translations:', err);
  }
}

function t(key, fallback = '') {
  return currentTranslations[key] || fallback || key;
}

function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (currentTranslations[key]) {
      el.textContent = currentTranslations[key];
    }
  });
}

function setupEventListeners() {
  langSelector.addEventListener('change', async (e) => {
    const lang = e.target.value;
    await fetch('/api/set_language', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ language: lang })
    });
    await fetchTranslations(lang);
    if (currentSession) renderGameState(currentSession);
  });

  btnStart.addEventListener('click', startNewGame);
  btnDraw.addEventListener('click', onDrawCard);
  drawDeck.addEventListener('click', onDrawCard);

  btnRules.addEventListener('click', showRules);
  btnStats.addEventListener('click', showStats);
  btnResetStats.addEventListener('click', resetStats);

  document.querySelectorAll('.close-modal').forEach(btn => {
    btn.addEventListener('click', () => {
      modalRules.classList.remove('active');
      modalStats.classList.remove('active');
    });
  });

  document.querySelectorAll('.suit-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const suit = e.target.getAttribute('data-suit');
      modalSuit.classList.remove('active');
      if (pendingCardPlay) {
        executePlayCard(pendingCardPlay, suit);
        pendingCardPlay = null;
      }
    });
  });
}

async function startNewGame() {
  const name = playerNameInput.value.trim() || 'Player';
  const aiCount = parseInt(aiCountSelect.value, 10);

  try {
    const res = await fetch('/api/game/new', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ human_name: name, ai_count: aiCount })
    });
    currentSession = await res.json();

    viewSetup.classList.remove('active');
    viewGame.classList.add('active');

    renderGameState(currentSession);
    checkTurnLoop();
  } catch (err) {
    alert('Failed to start game: ' + err.message);
  }
}

function renderGameState(state) {
  currentSession = state;

  document.getElementById('player-name-display').textContent = state.players[0].name;
  document.getElementById('player-score-display').textContent = `${state.players[0].score} pts`;

  deckCountBadge.textContent = state.deck_count;

  // Render Top Card
  renderTopCard(state.top_card);

  // Render Declared Suit
  if (state.declared_suit) {
    suitIndicator.textContent = `🎨 Suit: ${state.declared_suit}`;
    suitIndicator.classList.remove('hidden');
  } else {
    suitIndicator.classList.add('hidden');
  }

  // Render Opponents
  opponentsContainer.innerHTML = '';
  for (let i = 1; i < state.players.length; i++) {
    const p = state.players[i];
    const isCurrent = state.current_player_index === i;
    const oppEl = document.createElement('div');
    oppEl.className = `opponent-card ${isCurrent ? 'active-turn' : ''}`;
    
    let backsHtml = '';
    for (let c = 0; c < Math.min(p.hand_count, 8); c++) {
      backsHtml += '<div class="mini-card-back"></div>';
    }

    oppEl.innerHTML = `
      <div style="font-weight:bold;">${p.name}</div>
      <div style="font-size:0.85rem; color:#ffe066;">${p.score} pts (${p.hand_count} cards)</div>
      <div class="card-fan-back">${backsHtml}</div>
    `;
    opponentsContainer.appendChild(oppEl);
  }

  // Render Player Hand
  renderPlayerHand(state);

  // Update Status Narration
  if (state.message) {
    statusNarration.textContent = state.message;
  } else if (state.is_round_over) {
    statusNarration.textContent = `🎉 ${state.round_winner} won this round!`;
  } else {
    statusNarration.textContent = `Turn: ${state.current_player_name}`;
  }

  btnDraw.disabled = !state.is_human_turn;
}

function renderTopCard(card) {
  topCardSlot.innerHTML = createCardHTML(card);
}

function createCardHTML(card, isPlayable = false) {
  const isRed = card.color === 'red';
  return `
    <div class="card-item ${isRed ? 'red' : 'black'} ${isPlayable ? '' : 'disabled'}"
         data-rank="${card.rank}" data-suit="${card.suit}">
      <div class="card-corner">${card.symbol}<br>${card.suit}</div>
      <div class="card-center-suit">${card.suit}</div>
      <div class="card-corner" style="transform: rotate(180deg); align-self: flex-end;">${card.symbol}<br>${card.suit}</div>
    </div>
  `;
}

function renderPlayerHand(state) {
  playerHandContainer.innerHTML = '';
  const human = state.players[0];

  human.hand.forEach(card => {
    const isPlayable = state.is_human_turn && isValidPlay(card, state);
    const cardWrapper = document.createElement('div');
    cardWrapper.innerHTML = createCardHTML(card, isPlayable);
    const cardEl = cardWrapper.firstElementChild;

    if (isPlayable) {
      cardEl.addEventListener('click', () => onCardClicked(card));
    }
    playerHandContainer.appendChild(cardEl);
  });
}

function isValidPlay(card, state) {
  if (state.draw_stack > 0) return card.rank === 'SEVEN';
  if (state.declared_suit) return card.rank === 'JACK' || card.suit === state.declared_suit;
  return card.suit === state.top_card.suit || card.rank === state.top_card.rank || card.rank === 'JACK';
}

async function onCardClicked(card) {
  if (!currentSession || !currentSession.is_human_turn) return;

  if (card.rank === 'JACK') {
    pendingCardPlay = card;
    modalSuit.classList.add('active');
    return;
  }

  await executePlayCard(card, null);
}

async function executePlayCard(card, declaredSuit) {
  try {
    const res = await fetch('/api/game/play', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: currentSession.session_id,
        rank: card.rank,
        suit: card.suit,
        declared_suit: declaredSuit
      })
    });
    const state = await res.json();
    renderGameState(state);
    checkTurnLoop();
  } catch (err) {
    console.error('Play error:', err);
  }
}

async function onDrawCard() {
  if (!currentSession || !currentSession.is_human_turn) return;

  try {
    const res = await fetch('/api/game/draw', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: currentSession.session_id })
    });
    const state = await res.json();
    renderGameState(state);
    checkTurnLoop();
  } catch (err) {
    console.error('Draw error:', err);
  }
}

async function checkTurnLoop() {
  if (!currentSession || currentSession.is_round_over || currentSession.is_human_turn) return;

  setTimeout(async () => {
    try {
      const res = await fetch('/api/game/ai_turn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: currentSession.session_id })
      });
      const state = await res.json();
      renderGameState(state);
      checkTurnLoop();
    } catch (err) {
      console.error('AI turn error:', err);
    }
  }, 1000);
}

function showRules() {
  rulesBody.innerHTML = currentTranslations['rules_content'] || 'Loading rules...';
  modalRules.classList.add('active');
}

async function showStats() {
  const name = playerNameInput.value.trim() || 'Player';
  try {
    const res = await fetch(`/api/stats?name=${encodeURIComponent(name)}`);
    const data = await res.json();
    
    let html = `
      <p>🎮 <b>Matches:</b> ${data.stats.games_played}</p>
      <p>🏆 <b>Wins:</b> ${data.stats.games_won}</p>
      <p>⭐ <b>Best Score:</b> ${data.stats.best_score} pts</p>
      <hr style="margin: 10px 0; border-color: rgba(255,255,255,0.2);">
      <h4>Match History:</h4>
    `;

    if (data.history.length === 0) {
      html += '<p style="color:#aaa;">No matches recorded yet.</p>';
    } else {
      html += '<ul>';
      data.history.forEach(item => {
        html += `<li>${item.won ? '🏆 WON' : '❌ LOST'} — ${item.final_score || item.points_earned || 0} pts</li>`;
      });
      html += '</ul>';
    }

    statsBody.innerHTML = html;
    modalStats.classList.add('active');
  } catch (err) {
    alert('Failed to load stats: ' + err.message);
  }
}

async function resetStats() {
  const name = playerNameInput.value.trim() || 'Player';
  if (!confirm(`Are you sure you want to reset history for ${name}?`)) return;

  try {
    await fetch('/api/reset_stats', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: name })
    });
    await showStats();
  } catch (err) {
    alert('Failed resetting stats: ' + err.message);
  }
}
