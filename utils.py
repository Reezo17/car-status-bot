import gspread

def get_car_status(chat_id, spreadsheet_id, creds):
    try:
        gc = gspread.authorize(creds)
        sh = gc.open_by_key(spreadsheet_id)
        worksheet = sh.sheet1  # или укажи по имени, например: sh.worksheet("Sheet1")
        data = worksheet.get_all_records()

        for row in data:
            if str(row.get("chat_id")) == str(chat_id):
                car = row.get("car", "🚘 Авто")
                status = row.get("status", "❓ Статус не указан")
                comment = row.get("comment", "")
                return f"🚗 *{car}*\n📋 Статус: *{status}*\n📝 {comment}"

        return "⚠️ Вы не зарегистрированы. Используйте /register и сообщите свой chat_id администратору."

    except Exception as e:
        print("❌ Ошибка в utils.get_car_status:", e)
        raise e
