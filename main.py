import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

DIARY_FILE = 'diary.json'

def load_data():
    try:
        with open(DIARY_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(DIARY_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def validate_input():
    temperature = entry_temperature.get()
    description = entry_description.get()
    precipitation = var_precipitation.get()
    
    try:
        datetime.strptime(entry_date.get(), "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Ошибка", "Неверный формат даты.")
        return False
        
    if not temperature.replace('.', '', 1).isdigit():
        messagebox.showerror("Ошибка", "Температура должна быть числом.")
        return False
        
    if len(description.strip()) == 0:
        messagebox.showerror("Ошибка", "Описание не должно быть пустым.")
        return False
        
    return True

def add_entry():
    if validate_input():
        new_entry = {
            'date': entry_date.get(),
            'temperature': float(entry_temperature.get()),
            'description': entry_description.get(),
            'precipitation': bool(var_precipitation.get())
        }
        diary_entries.append(new_entry)
        save_data(diary_entries)
        refresh_table()
        clear_fields()

def refresh_table(filter_date=None, min_temp=None):
    for item in table.get_children():
        table.delete(item)
    for entry in diary_entries:
        if filter_date and entry['date'] != filter_date:
            continue
        if min_temp is not None and entry['temperature'] < min_temp:
            continue
        table.insert("", "end", values=(entry['date'], entry['temperature'], entry['description'], "Да" if entry['precipitation'] else "Нет"))

def apply_filters():
    filter_date = entry_filter_date.get() if entry_filter_date.get() else None
    min_temp = float(entry_min_temp.get()) if entry_min_temp.get() else None
    refresh_table(filter_date, min_temp)

def clear_fields():
    entry_date.delete(0, tk.END)
    entry_temperature.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    var_precipitation.set(False)

# Загрузка данных
diary_entries = load_data()

# Интерфейс приложения
root = tk.Tk()
root.title("Weather Diary")

frame_input = ttk.Frame(root)
frame_input.pack(padx=10, pady=10)

ttk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="W")
entry_date = ttk.Entry(frame_input)
entry_date.grid(row=0, column=1, pady=5)

ttk.Label(frame_input, text="Температура:").grid(row=1, column=0, sticky="W")
entry_temperature = ttk.Entry(frame_input)
entry_temperature.grid(row=1, column=1, pady=5)

ttk.Label(frame_input, text="Описание погоды:").grid(row=2, column=0, sticky="W")
entry_description = ttk.Entry(frame_input)
entry_description.grid(row=2, column=1, pady=5)

var_precipitation = tk.BooleanVar(value=False)
ttk.Checkbutton(frame_input, text="Осадки", variable=var_precipitation).grid(row=3, column=0, columnspan=2, pady=5)

btn_add = ttk.Button(frame_input, text="Добавить запись", command=add_entry)
btn_add.grid(row=4, column=0, columnspan=2, pady=10)

table_frame = ttk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=10, pady=10)

columns = ('Date', 'Temperature', 'Description', 'Precipitation')
table = ttk.Treeview(table_frame, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
table.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
scrollbar.pack(side="right", fill="y")
table.configure(yscrollcommand=scrollbar.set)

refresh_table()

# Фильтрация
frame_filters = ttk.Frame(root)
frame_filters.pack(padx=10, pady=10)

ttk.Label(frame_filters, text="Фильтр по дате:").grid(row=0, column=0, sticky="W")
entry_filter_date = ttk.Entry(frame_filters)
entry_filter_date.grid(row=0, column=1, pady=5)

ttk.Label(frame_filters, text="Минимальная температура:").grid(row=1, column=0, sticky="W")
entry_min_temp = ttk.Entry(frame_filters)
entry_min_temp.grid(row=1, column=1, pady=5)

btn_apply_filter = ttk.Button(frame_filters, text="Применить фильтры", command=apply_filters)
btn_apply_filter.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
