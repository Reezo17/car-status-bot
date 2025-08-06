import os
import requests
from flask import Flask, request
from utils import get_car_status

TOKEN = os.environ["BOT_TOKEN"]
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
ADMIN_CHAT_IDS = os.environ["ADMIN_CHAT_IDS"].split(",")

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    
    print("📩 Входящий апдейт:", data)  # Печать входящего сообщения

    message = data.get("message") or data.get("edited_message")
    if not message:
        return "ok"

    chat_id = str(message["chat"]["id"])
    text = message.get("text", "").strip()

    if text == "/start":
        reply = (
            "📌 Здравствуйте! Используйте /register, чтобы узнать свой chat_id и зарегистрироваться.\n"
            "Или /status, если уже зарегистрированы."
        )
    elif text == "/register":
        reply = f"👤 Ваш chat_id: `{chat_id}`\n\nСообщите его регистратору."
    elif text == "/status":
        reply = get_car_status(chat_id, SPREADSHEET_ID)
    else:
        reply = "⚠️ Неизвестная команда. Используйте /start, /register или /status."

    print("📤 Ответ бота:", reply)  # Печать текста, который бот собирается отправить

    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": reply,
            "parse_mode": "Markdown"
        }
    )

    print(f"📦 Результат запроса к Telegram API: {response.status_code}", response.text)

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
