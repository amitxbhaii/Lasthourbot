import os
import json
import urllib.parse
import requests
import time
from http.server import BaseHTTPRequestHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

SESSION = requests.Session()

def send_with_retry(chat_id, text):
    payload = {"chat_id": chat_id, "text": text}

    for attempt in range(3):  # max 3 tries
        try:
            r = SESSION.post(
                f"{API_URL}/sendMessage",
                json=payload,
                timeout=3
            )

            if r.status_code == 200:
                return True  # sent successfully

            # Telegram rate limit / temporary error
            time.sleep(1.5)

        except:
            time.sleep(1.5)

    return False  # give up after retries


class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        try:
            length = int(self.headers.get("content-length", 0))
            if length <= 0:
                return self._ok()

            raw = self.rfile.read(length)
            try:
                body = json.loads(raw)
            except:
                return self._ok()

            message = body.get("message")
            if not message:
                return self._ok()

            chat = message.get("chat", {})
            chat_id = chat.get("id")
            if not chat_id:
                return self._ok()

            text = message.get("text", "")
            if not isinstance(text, str):
                return self._ok()

            if text == "/start":
                reply = "Welcome to last hour bot send your search tag"
            else:
                query = urllib.parse.quote(text[:200])
                reply = (
                    "https://www.youtube.com/results"
                    f"?search_query={query}&sp=EgIIAQ%3D%3D"
                )

            send_with_retry(chat_id, reply)

        except:
            pass  # absolutely never crash

        self._ok()

    def do_GET(self):
        self._ok(b"YouTube bot running")

    def _ok(self, msg=b"ok"):
        self.send_response(200)
        self.end_headers()
        try:
            self.wfile.write(msg)
        except:
            pass
