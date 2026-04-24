#!/usr/bin/env bash
# Build script for soccer-web that resolves symlinks before running pygbag,
# so that images/music/sounds are included in the generated tar.gz archive.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$SCRIPT_DIR"

echo "==> Resolving asset symlinks..."
for dir in images music sounds; do
    if [ -L "$dir" ]; then
        TARGET="$(readlink -f "$dir")"
        rm "$dir"
        cp -r "$TARGET" "$dir"
        echo "    Copied $TARGET -> $dir"
    fi
done

echo "==> Running pygbag --build ..."
cd "$REPO_ROOT"
pygbag --build soccer-web/

echo "==> Restoring symlinks..."
cd "$SCRIPT_DIR"
for dir in images music sounds; do
    if [ -d "$dir" ] && [ ! -L "$dir" ]; then
        rm -rf "$dir"
        ln -s "../soccer-master/$dir" "$dir"
        echo "    Restored $dir -> ../soccer-master/$dir"
    fi
done

echo "==> Done. Run: python3 soccer-web/serve.py"
