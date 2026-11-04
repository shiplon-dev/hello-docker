"""Minimal Python HTTP server for testing Shiplon's Dockerfile runtime.

GET /         page with runtime details
GET /healthz  200 "ok" (set the health check path to /healthz)
"""
import html
import json
import os
import signal
import socket
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "8080"))
STARTED = datetime.now(timezone.utc).isoformat(timespec="seconds")


def info():
    return {
        "app": "hello-docker",
        "message": os.environ.get("APP_MESSAGE", "(APP_MESSAGE is not set)"),
        "python": sys.version.split()[0],
        "pod": socket.gethostname(),
        "uid": os.getuid(),
        "port": PORT,
        "startedAt": STARTED,
    }


class Handler(BaseHTTPRequestHandler):
    def send(self, code, body, ctype):
        data = body.encode()
        self.send_response(code)
        self.send_header("content-type", ctype)
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/healthz":
            return self.send(200, "ok\n", "text/plain")
        if path == "/api/info":
            return self.send(200, json.dumps(info(), indent=2) + "\n", "application/json")
        if path != "/":
            return self.send(404, "not found\n", "text/plain")
        rows = "".join(
            f"<tr><th>{html.escape(k)}</th><td>{html.escape(str(v))}</td></tr>" for k, v in info().items()
        )
        page = (
            '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            "<title>hello-docker</title><style>body{font-family:system-ui,sans-serif;max-width:640px;margin:40px auto;"
            "padding:0 16px}th{text-align:left;padding:6px 16px 6px 0;color:#555;font-weight:500}"
            "td{font-family:ui-monospace,monospace}</style>"
            f"<h1>hello-docker is running</h1><p>Dockerfile runtime test app for Shiplon (Python).</p><table>{rows}</table>"
        )
        return self.send(200, page, "text/html; charset=utf-8")

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} {fmt % args}", flush=True)


server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
signal.signal(signal.SIGTERM, lambda *_: (print("SIGTERM received, closing", flush=True), server.shutdown()))
print(f"hello-docker listening on :{PORT}", flush=True)
server.serve_forever()
