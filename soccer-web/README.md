# Substitute Soccer – Browser Edition

This is a browser-native port of **Substitute Soccer** from the *Code the Classics* book.  
The game runs directly in your browser as WebAssembly – **no VNC or remote desktop required**.

## How it works

The original game was written with [Pygame Zero](https://pygame-zero.readthedocs.io/) (`pgzero`).  
This version replaces the pgzero runtime with a thin compatibility shim and uses
[pygbag](https://pygame-web.github.io/) to compile the game to WebAssembly (WASM) so it
runs natively in any modern browser.

## Running in a Codespace

When you open this repository in a Codespace using the **"Browser Native (pygbag)"** dev
container (`/.devcontainer/browser-native/`), the game server starts automatically on
port **8000** and the browser tab opens for you.

If you need to (re)start it manually:

```bash
pygbag --port 8000 soccer-web/
```

Then open <http://localhost:8000> in your browser.

## Running locally

```bash
pip install pygbag
pygbag soccer-web/          # dev server with hot-reload on port 8000
```

To build static files for deployment:

```bash
pygbag --build soccer-web/  # output: soccer-web/build/web/
```

## Controls

| Action | Player 1 | Player 2 |
|--------|----------|----------|
| Move   | Arrow keys | W A S D |
| Shoot / Switch player | Space | Left Shift |

## Files

| File | Description |
|------|-------------|
| `main.py` | Game code (faithful port of `../soccer-master/soccer.py`) |
| `images/` | Symlink → `../soccer-master/images/` |
| `sounds/` | Symlink → `../soccer-master/sounds/` |
| `music/`  | Symlink → `../soccer-master/music/`  |
