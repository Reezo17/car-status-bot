# Telegram Car Status Bot

## Описание
Бот принимает команды от водителей и отправляет им данные по состоянию автомобиля из Google Таблицы.

## Команды
- `/start` — приветствие и справка
- `/register` — отправка chat_id водителя
- `/status` — получение текущего состояния авто

## Установка

1. Установите зависимости:
```
pip install -r requirements.txt
```

2. Добавьте переменные окружения:
```
TELEGRAM_TOKEN=your_telegram_token
SPREADSHEET_ID=your_spreadsheet_id
ADMIN_CHAT_IDS=comma_separated_admin_chat_ids
```

3. Запустите сервер:
```
python main.py
```

4. Настройте webhook:
```
https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=https://<your-host>/webhook
```