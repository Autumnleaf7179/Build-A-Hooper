"""Small dependency-free server for the downloaded static site.

The original project was captured from a Next.js site, so this serves the
downloaded assets directly and falls back to index.html for client routes.
No request is proxied to the source website.
"""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent


class OfflineHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        clean_path = urlsplit(self.path).path
        if clean_path in ("/", "/achievements", "/leaderboard", "/login"):
            # Remove the only outbound link from the captured document at
            # response time without rewriting the one-line HTML export.
            document = (ROOT / "index.html").read_bytes()
            document = document.replace(
                b"https://x.com/BuildAHooper", b"#"
            )
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(document)))
            self.end_headers()
            self.wfile.write(document)
            return
        super().do_GET()

    def translate_path(self, path):
        # Keep query strings out of the filesystem lookup. This also lets the
        # captured favicon links with Next's cache-busting query load locally.
        clean_path = urlsplit(path).path
        if clean_path == "/apple-icon.png":
            return str(ROOT / "apple-icon_0441f29e.png")
        translated = super().translate_path(clean_path)
        candidate = Path(translated)
        if candidate.exists():
            return str(candidate)

        # The capture contains only the root document. Returning it for the
        # captured site's client routes keeps navigation local instead of
        # reaching for the original server.
        if clean_path.startswith(("/achievements", "/leaderboard", "/login")):
            return str(ROOT / "index.html")
        return str(candidate)

    def log_message(self, format, *args):
        # Keep the workflow output useful while making it explicit that this
        # is a local-only server.
        print("[offline]", format % args)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 5000), OfflineHandler)
    print("Offline site available on port 5000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()