import tkinter as tk
from tkinter import font


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip_window or not self.text:
            return
        x = event.x_root + 10
        y = event.y_root + 10
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label_font = font.Font(family="Helvetica", size=10, weight="normal")
        label = tk.Label(tw, text=self.text, font=label_font, bg="#ffffff", fg="#000000", bd=1, relief="solid", padx=5, pady=3)
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None
