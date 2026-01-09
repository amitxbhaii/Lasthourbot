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

def send_button(chat_id, text, button_url):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "▶️ Open on YouTube",
                        "url": button_url
                    }
                ]
            ]
        }
    }

    for _ in range(3):
        try:
            r = SESSION.post(
                f"{API_URL}/sendMessage",
                json=payload,
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
                SESSION.post(
                    f"{API_URL}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": "Send search tag. Result will open via button."
                    },
                    timeout=3
                )
            else:
                q = urllib.parse.quote(text[:200])
                host = self.headers.get("host")

                # hidden redirect link
                redirect_url = (
                    f"https://{host}/go?"
                    f"q={q}"
                )

                send_button(
                    chat_id,
                    "🔍 Your search is ready",
                    redirect_url
                )

        except:
            pass

        self._ok()

    def do_GET(self):
        try:
            parsed = urlparse(self.path)

            # redirect handler
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
