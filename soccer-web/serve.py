#!/usr/bin/env python3
"""
Static file server for the soccer-web pygbag WASM build.

Serves build/web/ with the Cross-Origin isolation headers that SharedArrayBuffer
(required by the pygbag WASM runtime) needs, and binds to 0.0.0.0 so the
Codespace port-forwarder can reach it.

Unlike `pygbag soccer-web/` (dev mode), this server does NOT rewrite CDN URLs
to localhost — the generated index.html already references the real external CDN
(https://pygame-web.github.io/cdn/...) and works correctly when opened via the
Codespace forwarded URL in any browser.

Usage:
    python3 soccer-web/serve.py [port]   # default port: 8000
"""
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVE_DIR = os.path.join(SCRIPT_DIR, "build", "web")


class COIHandler(SimpleHTTPRequestHandler):
    """Add the Cross-Origin isolation headers required by SharedArrayBuffer."""

    def end_headers(self) -> None:
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        # 'credentialless' enables SharedArrayBuffer (required by WASM) while still
        # allowing cross-origin CDN resources that don't send CORP headers.
        # 'require-corp' would block pygame-web.github.io CDN assets.
        self.send_header("Cross-Origin-Embedder-Policy", "credentialless")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def guess_type(self, path):  # type: ignore[override]
        if str(path).endswith(".wasm"):
            return "application/wasm"
        return super().guess_type(path)

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"  {self.address_string()} - {fmt % args}")


def main() -> None:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    if not os.path.isdir(SERVE_DIR):
        print(f"Build directory not found: {SERVE_DIR}", file=sys.stderr)
        print("Run `pygbag --build soccer-web/` first.", file=sys.stderr)
        sys.exit(1)

    os.chdir(SERVE_DIR)
    server = HTTPServer(("0.0.0.0", port), COIHandler)
    print(f"Serving soccer-web from {SERVE_DIR}")
    print(f"Open http://localhost:{port}/ in your browser (via VS Code Ports tab)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
