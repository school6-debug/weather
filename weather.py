import tkinter as tk
from tkinter import messagebox, Listbox, StringVar, OptionMenu
import json
from datetime import datetime

class WeatherDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")

        # Поля ввода
        self.date_label = tk.Label(root, text="Дата (YYYY-MM-DD):")
        self.date_label.pack(pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.pack(pady=5)

        self.temp_label = tk.Label(root, text="Температура (°C):")
        self.temp_label.pack(pady=5)
        self.temp_entry = tk.Entry(root)
        self.temp_entry.pack(pady=5)

        self.desc_label = tk.Label(root, text="Описание погоды:")
        self.desc_label.pack(pady=5)
        self.desc_entry = tk.Entry(root)
        self.desc_entry.pack(pady=5)

        self.precip_label = tk.Label(root, text="Осадки (да/нет):")
        self.precip_label.pack(pady=5)
        self.precip_var = StringVar(root)
        self.precip_var.set("Нет")  # Значение по умолчанию
        self.precip_menu = OptionMenu(root, self.precip_var, "Да", "Нет")
        self.precip_menu.pack(pady=5)

        # Кнопка добавления записи
        self.add_button = tk.Button(root, text="Добавить запись", command=self.add_record)
        self.add_button.pack(pady=10)

        # Таблица записей о погоде
        self.record_list_label = tk.Label(root, text="Записи о погоде:")
        self.record_list_label.pack(pady=5)

        self.record_list = Listbox(root, width=50)
        self.record_list.pack(pady=5)

        # Фильтрация
        self.filter_label = tk.Label(root, text="Фильтрация по температуре:")
        self.filter_label.pack(pady=5)
        
        self.filter_temp_entry = tk.Entry(root)
        self.filter_temp_entry.pack(pady=5)

        self.filter_button = tk.Button(root, text="Фильтровать", command=self.filter_records)
        self.filter_button.pack(pady=5)

        # Загрузка данных из файла
        self.records = []
        self.load_records()

    def add_record(self):
        date_str = self.date_entry.get()
        temp_str = self.temp_entry.get()
        description = self.desc_entry.get()
        precip = self.precip_var.get()

        if not self.validate_input(date_str, temp_str, description):
            return

        record = {
            "date": date_str,
            "temperature": float(temp_str),
            "description": description,
            "precipitation": precip
        }

        self.records.append(record)
        self.update_record_display()
        self.save_records()

    def validate_input(self, date_str, temp_str, description):
        # Проверка даты
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте YYYY-MM-DD.")
            return False

        # Проверка температуры
        try:
            float(temp_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом.")
            return False

        # Проверка описания
        if not description.strip():
            messagebox.showerror("Ошибка", "Описание не должно быть пустым.")
            return False

        return True

    def update_record_display(self):
        self.record_list.delete(0, tk.END)
        
        for record in self.records:
            display_text = f"{record['date']} - {record['temperature']}°C - {record['description']} - Осадки: {record['precipitation']}"
            self.record_list.insert(tk.END, display_text)

    def filter_records(self):

        filter_temp_str = self.filter_temp_entry.get()
        
        try:
            filter_temp = float(filter_temp_str)
            filtered_records = [record for record in self.records if record["temperature"] > filter_temp]
            
            self.record_list.delete(0, tk.END)
            for record in filtered_records:
                display_text = f"{record['date']} - {record['temperature']}°C - {record['description']} - Осадки: {record['precipitation']}"
                self.record_list.insert(tk.END, display_text)
                
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное значение температуры для фильтрации.")

    def load_records(self, filename='records.json'):
        try:
            with open(filename, 'r') as f:
                self.records = json.load(f)
                self.update_record_display()
        except FileNotFoundError:
            pass

    def save_records(self, filename='records.json'):
        with open(filename, 'w') as f:
            json.dump(self.records, f)

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiaryApp(root)
    root.mainloop()
