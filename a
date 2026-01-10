import os
import json
import urllib.parse
import requests
from http.server import BaseHTTPRequestHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    requests.post(
        f"{API_URL}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text
        },
        timeout=5
    )

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers.get("content-length", 0))
        body = json.loads(self.rfile.read(length))

        message = body.get("message")
        if not message:
            self.send_response(200)
            self.end_headers()
            return

        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text == "/start":
            reply = "Welcome to last hour bot send your search tag"
        else:
            query = urllib.parse.quote(text)
            reply = f"https://www.youtube.com/results?search_query={query}&sp=EgIIAQ%3D%3D"

        send_message(chat_id, reply)

        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"YouTube bot running")
