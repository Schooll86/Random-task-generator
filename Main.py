import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
from datetime import datetime

class RandomTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("600x500")

        # Загрузка данных
        self.tasks = self.load_tasks()
        self.history = self.load_history()

        self.setup_ui()

    def load_tasks(self):
        """Загрузка списка задач из JSON"""
        try:
            with open('tasks.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Предопределённые задачи с категориями
            return {
                "учёба": ["Прочитать статью", "Изучить главу учебника", "Решить 5 задач", "Подготовиться к семинару"],
                "спорт": ["Сделать зарядку", "Пробежать 3 км", "Позаниматься йогой", "Отжаться 50 раз"],
                "работа": ["Проверить почту", "Составить отчёт", "Провести встречу", "Обновить документацию"]
            }

    def load_history(self):
        """Загрузка истории из JSON"""
        try:
            with open('task_history.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_tasks(self):
        """Сохранение задач в JSON"""
        with open('tasks.json', 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)

    def save_history(self):
        """Сохранение истории в JSON"""
        with open('task_history.json', 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def setup_ui(self):
        """Настройка интерфейса"""
        # Верхняя часть — генерация задачи
        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=10, fill='x')

        ttk.Button(top_frame, text="Сгенерировать задачу", command=self.generate_task).pack(side='left', padx=5)

        # Фильтрация
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=5, fill='x')

        ttk.Label(filter_frame, text="Фильтр по типу:").pack(side='left')
        self.filter_var = tk.StringVar(value="все")
        filters = ["все"] + list(self.tasks.keys())
        ttk.Combobox(filter_frame, textvariable=self.filter_var, values=filters, state="readonly").pack(side='left', padx=5)
        ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter).pack(side='left', padx=5)

        # Отображение текущей задачи
        self.current_task_label = ttk.Label(self.root, text="Нажмите кнопку для генерации задачи", wraplength=550)
        self.current_task_label.pack(pady=10)

        # История задач
        history_frame = ttk.LabelFrame(self.root, text="История задач")
        history_frame.pack(padx=10, pady=5, fill='both', expand=True)

        self.history_listbox = tk.Listbox(history_frame, height=15)
        scrollbar = ttk.Scrollbar(history_frame, orient='vertical', command=self.history_listbox.yview)
        self.history_listbox.configure(yscrollcommand=scrollbar.set)

        self.history_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Кнопки управления
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Очистить историю", command=self.clear_history).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Добавить новую задачу", command=self.add_task_dialog).pack(side='left', padx=5)

        self.update_history_display()

    def generate_task(self):
        """Генерация случайной задачи"""
        all_tasks = []
        for category, tasks in self.tasks.items():
            all_tasks.extend([(task, category) for task in tasks])

        if not all_tasks:
            messagebox.showwarning("Предупреждение", "Нет доступных задач!")
            return
          
          task, category = random.choice(all_tasks)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Добавляем в историю
        self.history.append({
            "task": task,
            "category": category,
            "timestamp": timestamp
        })
        self.save_history()

        # Обновляем отображение
        self.current_task_label.config(text=f"[{category}] {task}")
        self.update_history_display()

    def apply_filter(self):
        """Применение фильтра к истории"""
        self.update_history_display()

    def update_history_display(self):
        """Обновление отображения истории с учётом фильтра"""
        self.history_listbox.delete(0, tk.END)
        selected_filter = self.filter_var.get()

        for entry in reversed(self.history):  # От новых к старым
            if selected_filter == "все" or entry["category"] == selected_filter:
                self.history_listbox.insert(tk.END, f"{entry['timestamp']} | [{entry['category']}] {entry['task']}")

    def clear_history(self):
        """Очистка истории"""
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
            self.history = []
            self.save_history()
            self.update_history_display()

    def add_task_dialog(self):
        """Диалог добавления новой задачи"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить новую задачу")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Задача:").pack(pady=5)
        task_entry = ttk.Entry(dialog, width=40)
        task_entry.pack(pady=5)

        ttk.Label(dialog, text="Категория:").pack(pady=5)
        category_var = tk.StringVar(value="учёба")
        category_combo = ttk.Combobox(dialog, textvariable=category_var,
                                   values=list(self.tasks.keys()), state="readonly")
        category_combo.pack(pady=5)

        def save_new_task():
            task = task_entry.get().strip()
            category = category_var.get()

            if not task:
                messagebox.showerror("Ошибка", "Задача не может быть пустой!")
                return

            if category not in self.tasks:
                self.tasks[category] = []

            self.tasks[category].append(task)
            self.save_tasks()
            dialog.destroy()
            messagebox.showinfo("Успех", "Задача добавлена!")

        ttk.Button(dialog, text="Сохранить", command=save_new_task).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = RandomTaskGenerator(root)
    root.mainloop()
