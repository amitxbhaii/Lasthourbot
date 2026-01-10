import os
import json
import urllib.parse
import requests
import time
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

SESSION = requests.Session()

def send_text(chat_id, text):
    for _ in range(3):
        try:
            r = SESSION.post(
                f"{API_URL}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text
                },
                timeout=3
            )
            if r.status_code == 200:
                return
            time.sleep(1)
        except:
            time.sleep(1)

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            length = int(self.headers.get("content-length", 0))
            raw = self.rfile.read(length)
            body = json.loads(raw)

            msg = body.get("message")
            if not msg:
                return self._ok()

            chat_id = msg["chat"]["id"]
            text = msg.get("text", "")

            if text == "/start":
                send_text(
                    chat_id,
                    "Send search tag. Result will open automatically."
                )
            else:
                q = urllib.parse.quote(text[:200])
                host = self.headers.get("host")

                # 🔒 secret redirect link (YouTube hidden)
                redirect_url = f"https://{host}/go?q={q}"

                send_text(chat_id, redirect_url)

        except:
            pass

        self._ok()

    def do_GET(self):
        try:
            parsed = urlparse(self.path)

            # redirect handler (SAME AS BEFORE)
            if parsed.path == "/go":
                qs = parse_qs(parsed.query)
                q = qs.get("q", [""])[0]

                yt = (
                    "https://www.youtube.com/results"
                    f"?search_query={q}&sp=EgIIAQ%3D%3D"
                )

                self.send_response(302)
                self.send_header("Location", yt)
                self.end_headers()
                return

        except:
            pass

        self._ok(b"Bot running")

    def _ok(self, msg=b"ok"):
        self.send_response(200)
        self.end_headers()
        try:
            self.wfile.write(msg)
        except:
            pass
