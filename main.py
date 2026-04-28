import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import random
import string
import json
import os

# Настройки темы
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PasswordGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Random Password Generator")
        self.geometry("500x600")
        self.history_file = "history.json"
        self.history_data = self.load_history()

        # --- UI Элементы ---
        self.label_title = ctk.CTkLabel(self, text="Password Generator", font=("Arial", 24, "bold"))
        self.label_title.pack(pady=20)

        # Ползунок длины
        self.slider_label = ctk.CTkLabel(self, text=f"Длина пароля: 12")
        self.slider_label.pack()
        self.length_slider = ctk.CTkSlider(self, from_=4, to_=32, number_of_steps=28, command=self.update_label)
        self.length_slider.set(12)
        self.length_slider.pack(pady=10)

        # Чекбоксы
        self.use_letters = ctk.CTkCheckBox(self, text="Буквы (a-z, A-Z)")
        self.use_letters.select()
        self.use_letters.pack(pady=5)

        self.use_numbers = ctk.CTkCheckBox(self, text="Цифры (0-9)")
        self.use_numbers.select()
        self.use_numbers.pack(pady=5)

        self.use_symbols = ctk.CTkCheckBox(self, text="Спецсимволы (!@#$)")
        self.use_symbols.pack(pady=5)

        # Кнопка генерации
        self.generate_btn = ctk.CTkButton(self, text="Сгенерировать", command=self.generate_password)
        self.generate_btn.pack(pady=20)

        # Поле вывода
        self.result_entry = ctk.CTkEntry(self, placeholder_text="Ваш пароль", width=300, justify="center")
        self.result_entry.pack(pady=10)

        # Таблица истории (простой список)
        self.history_list = tk.Listbox(self, bg="#2b2b2b", fg="white", borderwidth=0, highlightthickness=0)
        self.history_list.pack(fill="both", expand=True, padx=20, pady=20)
        self.refresh_history_display()

    def update_label(self, value):
        self.slider_label.configure(text=f"Длина пароля: {int(value)}")

    def generate_password(self):
        length = int(self.length_slider.get())
        chars = ""
        if self.use_letters.get(): chars += string.ascii_letters
        if self.use_numbers.get(): chars += string.digits
        if self.use_symbols.get(): chars += string.punctuation

        if not chars:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
            return

        password = "".join(random.choice(chars) for _ in range(length))
        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, password)
        
        self.save_to_history(password)

    def save_to_history(self, pwd):
        self.history_data.append(pwd)
        if len(self.history_data) > 10: self.history_data.pop(0) # Храним последние 10
        with open(self.history_file, "潮流", encoding="utf-8") as f:
            json.dump(self.history_data, f)
        self.refresh_history_display()

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                return json.load(f)
        return []

    def refresh_history_display(self):
        self.history_list.delete(0, tk.END)
        for item in reversed(self.history_data):
            self.history_list.insert(tk.END, item)

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
