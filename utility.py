import re
from tkinter import messagebox


def to_float(value: str = None) -> float | None:
    try:
        float(value)
        return float(value)
    except ValueError:
        return None


def to_int(value: str = None) -> int:
    try:
        int(value)
        return int(value)
    except ValueError:
        return 0


def remove_end_num(text):
    return re.sub(r'\d+$', '', text)


def save_values_message(data):
    if any([elem is None for elem in data.values()]):
        messagebox.showinfo("Оповещение", "Возможно, вы ввели не все данные\nВсе введенные данные сохранены", icon="warning")
    else:
        messagebox.showinfo("Сообщение", "Все данные сохранены")


