#!/usr/bin/env python3
"""Local dev server for the site.

    python3 serve.py [port]        # default 8787

Serves this folder and accepts POST /api/save, which writes layout.json and
content.json beside index.html. The in-page editor only appears on localhost.
"""
import http.server, json, os, socketserver, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8787


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=HERE, **kw)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_POST(self):
        n = int(self.headers.get("Content-Length") or 0)
        if self.path.rstrip("/") != "/api/save":
            self.rfile.read(n)          # drain, else the client sees a reset
            self._json(404, {"ok": False, "error": "unknown endpoint"})
            return
        try:
            if n > 4_000_000:
                raise ValueError("payload too large")
            body = json.loads(self.rfile.read(n).decode("utf-8"))
            if not isinstance(body, dict):
                raise ValueError("expected an object")
            written = []
            for key, name in (("layout", "layout.json"), ("content", "content.json")):
                if key in body:
                    path = os.path.join(HERE, name)
                    with open(path, "w", encoding="utf-8") as fh:
                        json.dump(body[key], fh, indent=2, ensure_ascii=False)
                        fh.write("\n")
                    written.append(name)
            print("  saved:", ", ".join(written) or "(nothing)")
            self._json(200, {"ok": True, "written": written})
        except Exception as err:
            print("  save failed:", err)
            self._json(400, {"ok": False, "error": str(err)})

    def _json(self, code, obj):
        raw = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, fmt, *args):
        if "/api/save" in (args[0] if args else ""):
            return
        super().log_message(fmt, *args)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    print(f"serving {HERE}")
    print(f"  http://127.0.0.1:{PORT}   (editor enabled)")
    print("  ctrl-c to stop")
    with Server(("127.0.0.1", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")
