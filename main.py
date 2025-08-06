import os
import json
import requests
from flask import Flask, request
from utils import get_car_status
from google.oauth2 import service_account

TOKEN = os.environ["BOT_TOKEN"]
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
ADMIN_CHAT_IDS = os.environ["ADMIN_CHAT_IDS"].split(",")

# 🆕 Загружаем Google-учётку из переменной окружения
creds_info = json.loads(os.environ["GOOGLE_CREDS_JSON"])
creds = service_account.Credentials.from_service_account_info(creds_info)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print("👉 Входящий запрос от Telegram:", data)

    message = data.get("message") or data.get("edited_message")
    if not message:
        print("⚠️ Нет message в запросе")
        return "ok"

    chat_id = str(message["chat"]["id"])
    text = message.get("text", "").strip()
    print(f"📩 Сообщение от {chat_id}: {text}")

    if text == "/start":
        reply = (
            "👋 Здравствуйте! Используйте /register, чтобы узнать свой chat_id и зарегистрироваться.\n"
            "Или /status, если уже зарегистрированы."
        )
    elif text == "/register":
        reply = f"🆔 Ваш chat_id: `{chat_id}`\n\nСообщите его регистратору."
    elif text == "/status":
        try:
            reply = get_car_status(chat_id, SPREADSHEET_ID, creds)
        except Exception as e:
            reply = f"❌ Ошибка при получении статуса: {e}"
            print("❌ Ошибка в get_car_status:", e)
    else:
        reply = "❗ Неизвестная команда. Используйте /start, /register или /status."

    print("📤 Ответ бота:", reply)

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": reply,
                "parse_mode": "Markdown"
            }
        )
        print(f"✅ Запрос в Telegram: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"❌ Ошибка при отправке в Telegram: {e}")

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
