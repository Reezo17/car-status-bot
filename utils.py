import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_car_status(chat_id, spreadsheet_id):
    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(spreadsheet_id).worksheet("Автопарк")
        data = sheet.get_all_values()

        for i in range(1, len(data)):
            if data[i][6] == chat_id:
                car_model = data[i][1]
                plate = data[i][2]
                sheet_name = f"{car_model} {plate}".strip()
                car_sheet = client.open_by_key(spreadsheet_id).worksheet(sheet_name)
                car_data = car_sheet.get_all_values()

                last_row = len(car_data) - 1
                while last_row > 0 and not car_data[last_row][1]:
                    last_row -= 1

                if last_row <= 0:
                    return f"🚫 Нет данных по пробегу для {sheet_name}"

                row = car_data[last_row]
                return f"""📋 *Отчет по авто {sheet_name}*

📅 Дата: {row[0]}
📍 Пробег: {row[1]} км
🔧 Состояние: {row[2]}
🛠 Рекомендации: {row[3]}
🛢 Замена масла: {row[4]} км
💧 Замена жидкостей: {row[5]} км
🧾 Техосмотр: {row[6]}"""

        return "🚫 Ваш chat_id не найден в таблице 'Автопарк'. Обратитесь к администратору."
    except Exception as e:
        return f"❌ Ошибка при получении данных: {str(e)}"