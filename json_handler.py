import json

with open('history.json', encoding='utf-8') as f:
    templates = json.load(f)


class ExpeditionsData:
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

    def get_by_year(self, year):
        """Получить информацию об экспедиции по году"""
        if not self.data:
            print("Данные не загружены")
            return None

        if 'expeditions' in self.data:
            for travel in self.data['expeditions']:
                if travel['year'] == year:
                    return travel
        print(f"Путешествие за {year} год не найдено")
        return None

    def get_expedition_info(self, year):
        """Вывод информации об экспедиции"""
        expedition_info = self.get_by_year(year)
        if expedition_info:
            return f"\n=== Экспедиция за {year} год ===\n\n" \
                   f"Место: {expedition_info['place']}\n\n" \
                   f"{expedition_info['description']}"
        else:
            return f"Информация за {year} не найдена"