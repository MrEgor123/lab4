from docx import Document

# Список продукционных правил для генератора плейлистов
rules = [
    {"condition": lambda data: data.get("genre") == "rock" and data.get("mood") == "энергичное" and data.get("time") == "утро",
     "action": "Рекомендуется плейлист 'Утренний рок-буст'"},
    {"condition": lambda data: data.get("genre") == "pop" and data.get("mood") == "радостное" and data.get("time") == "день",
     "action": "Рекомендуется плейлист 'Поп-мотиватор дня'"},
    {"condition": lambda data: data.get("mood") == "расслабленное" and data.get("time") == "вечер",
     "action": "Рекомендуется плейлист 'Вечерний чилл-аут'"},
    {"condition": lambda data: data.get("genre") == "jazz" and int(data.get("popularity", 0)) > 70,
     "action": "Рекомендуется плейлист 'Классический джаз'"},
    {"condition": lambda data: data.get("preferences") == "тренировка" and data.get("mood") == "энергичное",
     "action": "Рекомендуется плейлист 'Workout Boost'"},
    {"condition": lambda data: data.get("genre") == "electronic" and data.get("time") == "ночь",
     "action": "Рекомендуется плейлист 'Ночной электро-микс'"}
]

def read_questionnaire(file_path):
    """
    Считывает данные из файла DOCX и возвращает словарь с параметрами.
    Ожидаемые поля:
      - Жанр (rock/pop/jazz/classical/electronic)
      - Настроение (энергичное/радостное/расслабленное/меланхоличное)
      - Время суток (утро/день/вечер/ночь)
      - Предпочтения (тренировка/работа/отдых)
      - Популярность (число от 0 до 100)
    """
    doc = Document(file_path)
    data = {}
    for paragraph in doc.paragraphs:
        if ": " in paragraph.text:
            parts = paragraph.text.split(": ", 1)
            key = parts[0].strip()
            value = parts[1].strip().lower() if len(parts) > 1 else ""
            data[key] = value

    # Преобразование и переименование ключей для удобства
    try:
        data["genre"] = data.get("Жанр (rock/pop/jazz/classical/electronic)", "")
        data["mood"] = data.get("Настроение (энергичное/радостное/расслабленное/меланхоличное)", "")
        data["time"] = data.get("Время суток (утро/день/вечер/ночь)", "")
        data["preferences"] = data.get("Предпочтения (тренировка/работа/отдых)", "")
        data["popularity"] = int(data.get("Популярность (числовое значение от 0 до 100)", "0") or "0")
    except ValueError:
        return None

    return data

def analyze_data(data):
    required_fields = ["genre", "mood", "time", "preferences", "popularity"]
    if not all(field in data for field in required_fields):
        print("Не все обязательные данные были получены.")
        return

    matched = False
    for rule in rules:
        if rule["condition"](data):
            print(rule["action"])
            matched = True

    if not matched:
        print("К сожалению, по вашим данным не удалось подобрать подходящий плейлист.")

if __name__ == "__main__":
    file_path = "анкета_playlist.docx"
    data = read_questionnaire(file_path)
    if data:
        analyze_data(data)
    else:
        print("Ошибка при считывании данных из анкеты.")
