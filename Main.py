import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os
from datetime import datetime

# Начальный список задач с категориями
TASKS = [
    {"task": "Прочитать статью", "category": "учёба"},
    {"task": "Сделать зарядку", "category": "спорт"},
    {"task": "Написать отчёт", "category": "работа"}
]

HISTORY_FILE = "task_history.json"

def load_history():
    """Загружает историю из JSON-файла"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    """Сохраняет историю в JSON-файл"""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.history = load_history()

        # Элементы интерфейса
        self.current_task_label = tk.Label(root, text="Нажмите 'Сгенерировать задачу'", wraplength=300)
        self.current_task_label.pack(pady=10)

        self.generate_btn = tk.Button(root, text="Сгенерировать задачу", command=self.generate_task)
        self.generate_btn.pack(pady=5)

        # Фильтрация
        tk.Label(root, text="Фильтр по категории:").pack()
        self.filter_var = tk.StringVar(value="Все")
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)
        for category in ["Все", "учёба", "спорт", "работа"]:
            tk.Radiobutton(filter_frame, text=category, variable=self.filter_var,
                           value=category, command=self.update_history_list).pack(side=tk.LEFT)

        # Список истории
        tk.Label(root, text="История задач:").pack()
        self.history_listbox = tk.Listbox(root, width=50, height=15)
        self.history_listbox.pack(pady=5)

        self.update_history_list()

    def generate_task(self):
        """Генерирует случайную задачу и добавляет в историю"""
        task_data = random.choice(TASKS)
        full_task = {
            "task": task_data["task"],
            "category": task_data["category"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Уточнённый формат времени
        }
        self.history.append(full_task)
        save_history(self.history)  # Сохраняем историю

        self.current_task_label.config(text=f"Задача: {task_data['task']} ({task_data['category']})")
        self.update_history_list()  # Обновляем отображение истории

    def update_history_list(self):
        """Обновляет отображение истории с учётом фильтра"""
        self.history_listbox.delete(0, tk.END)
        selected_category = self.filter_var.get()

        for entry in self.history:
            if selected_category == "Все" or entry["category"] == selected_category:
                self.history_listbox.insert(tk.END,
                    f"{entry['timestamp']} | {entry['task']} ({entry['category']})")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()
