#!/usr/bin/env bash
# Build script for soccer-web that resolves symlinks before running pygbag,
# so that images/music/sounds are included in the generated tar.gz archive.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Restore the asset symlinks – registered as a trap so it runs even if pygbag fails.
restore_symlinks() {
    cd "$SCRIPT_DIR"
    for dir in images music sounds; do
        if [ -d "$dir" ] && [ ! -L "$dir" ]; then
            rm -rf "$dir"
            ln -s "../soccer-master/$dir" "$dir"
            echo "    Restored $dir -> ../soccer-master/$dir"
        fi
    done
}

cd "$SCRIPT_DIR"

echo "==> Resolving asset symlinks..."
for dir in images music sounds; do
    if [ -L "$dir" ]; then
        # readlink -f is not available on older macOS; fall back to python3.
        TARGET="$(readlink -f "$dir" 2>/dev/null || python3 -c "import os,sys; print(os.path.realpath(sys.argv[1]))" "$dir")"
        rm "$dir"
        cp -r "$TARGET" "$dir"
        echo "    Copied $TARGET -> $dir"
    fi
done

# Register the trap after copies are made so restore only runs when needed.
trap restore_symlinks EXIT

echo "==> Running pygbag --build ..."
cd "$REPO_ROOT"
pygbag --build soccer-web/

echo "==> Done. Run: python3 soccer-web/serve.py"
