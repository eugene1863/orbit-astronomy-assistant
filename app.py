"""Local web app; text chat needs only the Python standard library."""
import base64
import io
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from chatbot import answer

ROOT = Path(__file__).parent
class Handler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            body = (ROOT / "index.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path == "/api/status":
            self.send_json({"trained": (ROOT / "models/galaxy_cnn.pt").exists()})
        else:
            self.send_json({"error": "Not found"}, 404)

    def do_POST(self):
        if self.headers.get("Origin") not in (None, "http://127.0.0.1:8000", "http://localhost:8000"):
            return self.send_json({"error": "Origin not allowed"}, 403)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 8_000_000:
                return self.send_json({"error": "Request must be below 8 MB."}, 413)
            data = json.loads(self.rfile.read(length))
            if not isinstance(data, dict):
                raise ValueError("Expected a JSON object.")
            if self.path == "/api/chat":
                question = data.get("question", "")
                if not isinstance(question, str) or not question.strip() or len(question) > 2000:
                    raise ValueError("Enter a question between 1 and 2000 characters.")
                return self.send_json(answer(question))
            if self.path == "/api/classify":
                if not (ROOT / "models/galaxy_cnn.pt").exists():
                    return self.send_json({"error": "Train the CNN first. See README.md for the dataset layout and training command."}, 409)
                from cnn import classify
                raw = base64.b64decode(data.get("image", ""), validate=True)
                return self.send_json(classify(io.BytesIO(raw)))
            self.send_json({"error": "Not found"}, 404)
        except ImportError:
            self.send_json({"error": "Install the CNN dependencies: python -m pip install -r requirements-cnn.txt"}, 503)
        except (ValueError, TypeError):
            self.send_json({"error": "Invalid request or image."}, 400)
        except Exception:
            self.send_json({"error": "Image classification failed. Check the image and trained checkpoint."}, 500)

if __name__ == "__main__":
    print("Astronomy Assistant: http://127.0.0.1:8000", flush=True)
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
