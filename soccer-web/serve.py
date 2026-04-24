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
import urllib.request
import urllib.error
from http.server import HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SERVE_DIR = os.path.join(SCRIPT_DIR, "build", "web")


_CDN_LOCAL_PREFIX = "/cdn/"
_CDN_REMOTE_BASE = "https://pygame-web.github.io/cdn/"

# Injected into every index.html response (just before </head>).
# Suspends the Emscripten/SDL2 Web Audio AudioContext the moment the browser
# fires `beforeunload` (i.e. before the "Leave site?" dialog freezes JS
# execution).  Without this, SDL2's audio callback keeps looping its last
# buffer while the dialog is open, producing an annoying repeating glitch.
_AUDIO_STOP_SCRIPT = b"""
<script>
(function () {
    function _stopSDL2Audio() {
        // Emscripten SDL2 stores the AudioContext on Module.SDL2.audioContext.
        try { Module.SDL2.audioContext.suspend(); return; } catch (e) {}
        // Fallback: scan globalThis for any live AudioContext instances.
        try {
            for (var k in globalThis) {
                var v = globalThis[k];
                if (v && typeof v.suspend === "function" &&
                        typeof v.state === "string" && v.state !== "closed") {
                    v.suspend();
                }
            }
        } catch (e) {}
    }
    // beforeunload fires before the "Leave site?" dialog pauses execution.
    window.addEventListener("beforeunload", _stopSDL2Audio);
    // pagehide handles bfcache/mobile cases where beforeunload may not fire.
    window.addEventListener("pagehide", _stopSDL2Audio);
})();
</script>
"""


class COIHandler(SimpleHTTPRequestHandler):
    """Add the Cross-Origin isolation headers required by SharedArrayBuffer."""

    def do_GET(self) -> None:
        # Proxy /cdn/* requests to the real pygame-web CDN.
        # pythons.js tries a local-first lookup at http://localhost:PORT/cdn/...
        # before falling back to the remote CDN; proxying here makes that work.
        path = self.path.split("#")[0].split("?")[0]  # strip fragment & query

        # Serve index.html with the audio-stop script injected so that the fix
        # survives pygbag rebuilds without touching the generated file.
        if path in ("/", "/index.html"):
            index_path = os.path.join(SERVE_DIR, "index.html")
            try:
                with open(index_path, "rb") as f:
                    content = f.read()
                content = content.replace(b"</head>", _AUDIO_STOP_SCRIPT + b"</head>", 1)
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception:
                pass  # fall through to default static serving

        if path.startswith(_CDN_LOCAL_PREFIX):
            remote_url = _CDN_REMOTE_BASE + path[len(_CDN_LOCAL_PREFIX) :]
            try:
                with urllib.request.urlopen(remote_url) as resp:
                    data = resp.read()
                    content_type = resp.headers.get("Content-Type", "application/octet-stream")
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            except urllib.error.HTTPError as exc:
                self.send_response(exc.code)
                self.end_headers()
            except Exception:
                self.send_response(502)
                self.end_headers()
            return
        super().do_GET()

    def end_headers(self) -> None:
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        # 'credentialless' enables SharedArrayBuffer (required by WASM) while still
        # allowing cross-origin CDN resources that don't send CORP headers.
        # 'require-corp' would block pygame-web.github.io CDN assets.
        self.send_header("Cross-Origin-Embedder-Policy", "credentialless")
        self.send_header("Access-Control-Allow-Origin", "*")
        # Prevent browsers from caching WASM/APK across iterative builds.
        self.send_header("Cache-Control", "no-store")
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
    server = ThreadingHTTPServer(("0.0.0.0", port), COIHandler)
    print(f"Serving soccer-web from {SERVE_DIR}")
    print(f"Open http://localhost:{port}/ in your browser (via VS Code Ports tab)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
