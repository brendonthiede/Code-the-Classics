# Substitute Soccer – Browser Edition

This is a browser-native port of **Substitute Soccer** from the *Code the Classics* book.  
The game runs directly in your browser as WebAssembly – **no VNC or remote desktop required**.

## How it works

The original game was written with [Pygame Zero](https://pygame-zero.readthedocs.io/) (`pgzero`).  
This version replaces the pgzero runtime with a thin compatibility shim and uses
[pygbag](https://pygame-web.github.io/) to compile the game to WebAssembly (WASM) so it
runs natively in any modern browser.

## Running in a Codespace

> **Note on `pygbag` dev mode**: Running `pygbag soccer-web/` rewrites CDN URLs to
> `http://localhost:8000` at serve time. When accessed from an external browser via the
> Codespace forwarded URL, those localhost requests fail. Use `serve.py` instead (see below).

Build the WASM bundle once, then start the static server:

```bash
pygbag --build soccer-web/   # pack & build into soccer-web/build/web/
python3 soccer-web/serve.py  # static server on port 8000
```

Open the app via the **Ports** panel in VS Code (port 8000) — click the globe icon to
open in your browser, or use the forwarded URL shown there.

## Running locally

```bash
pip install pygbag
pygbag --build soccer-web/   # build static WASM bundle
python3 soccer-web/serve.py  # serve on port 8000
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
