# Mau-Mau Card Game

A digital adaptation of Mau-Mau, a fast-paced shedding card game similar to
Crazy Eights and UNO.  Players compete to discard their 5-card hands using a
32-card deck, utilising power cards and strategic calls to be the first to
reach **150 points**.

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

* Python ≥ 3.9 (GPL-compatible, open-source)

---

## Installation

### Run from source

```bash
git clone https://github.com/martynrangelfigueiredo/mau-mau.git
cd mau-mau
pip install -e .
mau-mau          # or: python -m maumau
```

### Download Windows binary

Pre-built Windows binaries are attached to every
[GitHub Release](https://github.com/martynrangelfigueiredo/mau-mau/releases):

| File | Description |
|------|-------------|
| `mau-mau.exe` | Standalone portable executable (no installer needed) |
| `mau-mau-setup.exe` | Full installer — adds Start Menu shortcut and uninstaller |

---

## Building from Source (Windows)

### Prerequisites

* [Python 3.12](https://www.python.org/downloads/) (GPL-compatible)
* [PyInstaller](https://pyinstaller.org/) — builds the standalone `.exe`
* [NSIS 3.x](https://nsis.sourceforge.io/Download) — builds the `.exe`
  installer (GPL-compatible)

### Steps

```powershell
# 1. Install PyInstaller
pip install pyinstaller

# 2. Build standalone .exe
pyinstaller --onefile --name mau-mau --console src/maumau/__main__.py

# 3. Build installer  (requires NSIS in PATH)
makensis installer/mau-mau.nsi
```

The installer is written to `installer/mau-mau-setup.exe`.

### Automated build (GitHub Actions)

Push a tag to trigger the full build pipeline:

```bash
git tag v1.0.0
git push origin v1.0.0
```

The workflow (`.github/workflows/build-windows.yml`) will:
1. Run all tests
2. Build `mau-mau.exe` with PyInstaller on `windows-latest`
3. Build `mau-mau-setup.exe` with NSIS
4. Publish both as a GitHub Release

---

## Windows Store

To publish on the **Microsoft Store** you need to repackage the NSIS installer
as an **MSIX** package using the
[MSIX Packaging Tool](https://docs.microsoft.com/windows/msix/packaging-tool/tool-overview)
(free, from Microsoft Store).  Steps:

1. Build `mau-mau-setup.exe` as described above.
2. Open the **MSIX Packaging Tool** → *Create package from existing installer*.
3. Point it at `mau-mau-setup.exe` and follow the wizard.
4. Sign the resulting `.msix` with a code-signing certificate.
5. Submit via [Partner Center](https://partner.microsoft.com/dashboard).

---

## Development

```bash
pip install -e . pytest
python -m pytest tests/ -v
```

---

## License

**GNU General Public License v3.0 or later** — see [LICENSE](LICENSE).

All tools used in the build pipeline are also open-source:

| Tool | License |
|------|---------|
| Python | PSF (GPL-compatible) |
| PyInstaller | GPL-2.0 |
| NSIS | zlib/libpng (OSI-approved) |
| GitHub Actions | free for public repos |
