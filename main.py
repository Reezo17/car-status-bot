import os
from flask import Flask, request
import requests
from utils import get_car_status

TOKEN = os.getenv("TELEGRAM_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
ADMIN_CHAT_IDS = os.getenv("ADMIN_CHAT_IDS", "").split(",")

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        return "no data"

    message = data.get('message') or data.get('edited_message')
    if not message:
        return "no message"

    chat_id = str(message['chat']['id'])
    text = message.get('text', '').strip()

    if text == '/start':
        reply = "👋 Привет! Напиши /register, чтобы узнать свой chat_id и зарегистрироваться. Или /status, если уже зарегистрирован."
    elif text == '/register':
        reply = f"✅ Ваш chat_id: `{chat_id}`\n\nСкопируйте и передайте администратору."
    elif text == '/status':
        reply = get_car_status(chat_id, SPREADSHEET_ID)
    else:
        reply = "❓ Неизвестная команда. Используйте /start, /register или /status."

    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
        "chat_id": chat_id,
        "text": reply,
        "parse_mode": "Markdown"
    })

    return "ok"
    if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
