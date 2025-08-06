import os
import requests
from flask import Flask, request
from utils import get_car_status

TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
ADMIN_CHAT_IDS = os.getenv("ADMIN_CHAT_IDS", "").split(",")

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("📩 Входящий апдейт:", data)  # DEBUG

    message = data.get("message") or data.get("edited_message")
    if not message:
        return "No message"

    chat_id = str(message["chat"]["id"])
    text = message.get("text", "").strip()

    if text == "/start":
        reply = "Нажмите /register, чтобы узнать свой chat_id и зарегистрироваться. Или /status, если уже зарегистрированы."
    elif text == "/register":
        reply = f"Ваш chat_id: `{chat_id}`\n\nСообщите его регистратору."
    elif text == "/status":
        reply = get_car_status(chat_id, SPREADSHEET_ID)
    else:
        reply = "Неизвестная команда. Используйте /start, /register или /status."

    print("📤 Ответ бота:", reply)  # DEBUG

    response = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
        "chat_id": chat_id,
        "text": reply,
        "parse_mode": "Markdown"
    })

    print(f"📦 Результат запроса к Telegram API: {response.status_code}, {response.text}")  # DEBUG

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
