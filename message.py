import json


class MessageData:
    def __init__(self, filename):
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        """Загружает данные из JSON файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Файл {self.filename} не найден")
            return None
        except json.JSONDecodeError as e:
            print(f"Ошибка чтения JSON: {e}")
            return None

    def get_mes(self, mes, one="one"):
        if not self.data:
            return None

        if mes in self.data:
            if mes == "welcome_text":
                return self.data[mes][one]

            return self.data[mes]

        return "Такого сообщения нет"

    def get_year(self, end="start"):
        if not self.data:
            return None

        if "years" in self.data:
            if end in self.data["years"]:
                return self.data["years"][end]

        return None

    def get_list_of_years(self):
        start = self.get_year()
        end = self.get_year("end")
        years = []
        if start is not None and end is not None:
            for y in range(start, end + 1):
                years.append(f"{y} г.")
            return years
        return years