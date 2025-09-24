import os
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("7955408930:AAGteNCuLYhIh07vzeNYMpQPT1zjtyRhokc")
GEMINI_API_KEY = os.getenv("AIzaSyAvX_PPsgdB_7JQXiXCTlcNFVVA_d2jhAg")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

@app.route(f"/webhook/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        gemini_response = ask_gemini(text)
        send_message(chat_id, gemini_response)

    return {"ok": True}

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    requests.post(url, json=payload)

def ask_gemini(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY,
    }
    body = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(url, headers=headers, json=body)
    if response.status_code == 200:
        candidates = response.json().get("candidates", [])
        if candidates:
            return candidates[0]["content"]["parts"][0]["text"]
        return "❌ پاسخی از Gemini دریافت نشد."
    else:
        return f"❌ خطا: {response.text}"

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!", 200
