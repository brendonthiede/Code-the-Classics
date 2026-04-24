# Substitute Soccer – Browser Edition

This is a browser-native port of **Substitute Soccer** from the _Code the Classics_ book.  
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
bash soccer-web/build.sh          # resolve symlinks, pack & build into soccer-web/build/web/
python3 soccer-web/serve.py       # static server on port 8000
```

Open the app via the **Ports** panel in VS Code (port 8000) — click the globe icon to
open in your browser, or use the forwarded URL shown there.

## Running locally

```bash
pip install pygbag
bash soccer-web/build.sh          # resolve symlinks and build static WASM bundle
python3 soccer-web/serve.py       # serve on port 8000
```

To build static files for deployment:

```bash
bash soccer-web/build.sh  # output: soccer-web/build/web/
```

## Controls

| Action                | Player 1   | Player 2   |
| --------------------- | ---------- | ---------- |
| Move                  | Arrow keys | W A S D    |
| Shoot / Switch player | Space      | Left Shift |

## Files

| File      | Description                                               |
| --------- | --------------------------------------------------------- |
| `main.py` | Game code (faithful port of `../soccer-master/soccer.py`) |
| `images/` | Symlink → `../soccer-master/images/`                      |
| `sounds/` | Symlink → `../soccer-master/sounds/`                      |
| `music/`  | Symlink → `../soccer-master/music/`                       |

> **Windows note:** The asset directories (`images/`, `music/`, `sounds/`) are
> stored as symlinks in the repository. On Windows these can be checked out as
> plain text files instead of real symlinks, which causes asset loading to fail
> silently (the `_load_image` helper in `main.py` falls back to a 1×1 transparent
> surface when an image cannot be found). To avoid this, enable Git symlink
> support before cloning: run `git config --global core.symlinks true` and enable
> **Developer Mode** in Windows Settings (Settings → Privacy & Security → For
> developers), then re-clone the repository.
