import json
import os
import socket
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.environ.get("PORT", "8080"))


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/plain; charset=utf-8"):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, "ok")
        elif self.path == "/info":
            info = {
                "hostname": socket.gethostname(),
                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "version": os.environ.get("APP_VERSION", "v1"),
            }
            self._send(200, json.dumps(info), "application/json")
        elif self.path == "/":
            self._send(200, f"Hallo vom Amir! Pod: {socket.gethostname()}\n")
        else:
            self._send(404, "not found")


if __name__ == "__main__":
    print(f"Server läuft auf Port {PORT}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
