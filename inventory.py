"""Small inventory HTTP service used by the Kubernetes lab."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path

POD_NAME = os.getenv("POD_NAME", "local-inventory")
READY_FILE = Path("/tmp/ready")


class InventoryHandler(BaseHTTPRequestHandler):
    def send_json(self, status, body):
        encoded = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path == "/ready":
            ready = READY_FILE.exists()
            self.send_json(200 if ready else 503, {
                "status": "ready" if ready else "not ready",
                "pod": POD_NAME,
            })
            return
        if self.path == "/healthz":
            self.send_json(200, {"status": "ok", "pod": POD_NAME})
            return
        if self.path.startswith("/items/"):
            item_id = self.path.removeprefix("/items/") or "unknown"
            print(f"served item={item_id} pod={POD_NAME}", flush=True)
            self.send_json(200, {
                "item_id": item_id,
                "available": True,
                "served_by": POD_NAME,
            })
            return
        self.send_json(404, {"error": "not found", "pod": POD_NAME})

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    READY_FILE.touch()
    server = ThreadingHTTPServer(("0.0.0.0", 8000), InventoryHandler)
    print(f"inventory pod={POD_NAME} listening on port 8000", flush=True)
    server.serve_forever()
