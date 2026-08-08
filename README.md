# Mau-Mau Card Game

A digital adaptation of Mau-Mau, a fast-paced shedding card game similar to
Crazy Eights and UNO.  Players compete to discard their 5-card hands using a
32-card deck, utilising power cards and strategic calls to be the first to
reach **150 points**.

Play it with a windowed desktop GUI (built with [PySide6](https://www.qt.io/qt-for-python), the free/open-source Qt bindings for Python, LGPLv3) or the original text-based console interface. Card artwork is drawn entirely in code (vector shapes, standard pip layouts, Unicode suit glyphs) — no third-party images, so there are no licensing or trademark concerns.

[![CI](https://github.com/martynrangelfigueiredo/mau-mau/actions/workflows/ci.yml/badge.svg)](https://github.com/martynrangelfigueiredo/mau-mau/actions/workflows/ci.yml)

---

## Game Rules

| Card | Effect |
|------|--------|
| **7** | Next player must draw 2 cards (or chain another 7) |
| **8** | Next player's turn is skipped |
| **J (Jack)** | Wild card — player declares a new suit |
| **A (Ace)** | Reverses play direction (2-player: acts as skip) |

* Each player starts with **5 cards** from a standard **32-card deck**  
  (7, 8, 9, 10, J, Q, K, A × 4 suits).
* On your turn, play a card matching the **suit** or **rank** of the top
  discard card.  If you cannot play, draw one card.
* Call **"Mau!"** when you have one card left.  Call **"Mau-Mau!"** when you
  play your last card to win the round.
* **Scoring:** The round winner earns points equal to the sum of all opponents'
  remaining hand values (J=20, Q=K=10, A=11, 7–10=0).
* The first player to reach **150 points** wins the game.

---

## Requirements

* [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)

---

## Execution (Docker Only)

This project is configured to run exclusively via Docker and Docker Compose.

### 1. Web Application (Recommended)

Start the Web Application and database:

```bash
docker compose up --build
```

Access the application in your browser at `http://localhost:8000`.

### 2. Console Version (CLI)

Run the interactive terminal version inside a container:

```bash
docker compose run --rm maumau-cli
```

### 3. Run Tests via Docker

Run the full pytest suite inside a container:

```bash
docker compose run --rm maumau-web pytest
```


---

## License

**GNU General Public License v3.0 or later** — see [LICENSE](LICENSE).

All tools used in the build pipeline are also open-source:

| Tool | License |
|------|---------|
| Python | PSF (GPL-compatible) |
| PySide6 (Qt for Python) | LGPLv3 |
| PyInstaller | GPL-2.0 |
| NSIS | zlib/libpng (OSI-approved) |
| GitHub Actions | free for public repos |
