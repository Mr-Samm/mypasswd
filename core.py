import tkinter as tk
from tkinter import ttk
import json

FONT = ("Comic Sans MS", 14)


class URL:
    def __init__(self):
        url_lb = tk.Label(text="URL", font=FONT, bg="white")
        url_lb.place(x=230, y=500)
        self.url_en = tk.Entry(highlightbackground="black", highlightthickness=1, width=30, font=FONT)
        self.url_en.place(x=315, y=500)


class User:
    def __init__(self):
        user_lb = tk.Label(text="User/Email", font=FONT, bg="white")
        user_lb.place(x=200, y=550)
        self.user_en = tk.Entry(highlightbackground="black", highlightthickness=1, width=30, font=FONT)
        self.user_en.place(x=315, y=550)


class Password:
    def __init__(self):
        pass_lb = tk.Label(text="Password", font=FONT, bg="white")
        pass_lb.place(x=200, y=600)
        self.pass_en = tk.Entry(highlightbackground="black", highlightthickness=1, width=30, font=FONT)
        self.pass_en.place(x=315, y=600)


class Button:
    def __init__(self, x, y, text, command):
        style = ttk.Style()
        self.width = 8
        style.configure("Cute.TButton",
                        background="pink",
                        foreground="black",
                        font=("Comic Sans MS", 12, "bold"),
                        relief="flat",
                        borderwidth=2,
                        width=6,
                        padding=4)

        self.button = ttk.Button(text=text, style="Cute.TButton", command=command, width=self.width)
        self.button.place(x=x, y=y)


class Message:
    def __init__(self, message):
        self.x = 600
        self.y = 660
        self.l = tk.Label(text=message, font=("Comic Sans MS", 10), fg="green", bg="white")
        self.l.place(x=self.x, y=self.y)


class Searcher:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, "r") as db:
            self.database = json.load(db)


# data = Searcher(file_path="db.json")
# print(data.database["gmail"]["password"])

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
symbols = "!@#$%^&*()"
numbers = "123456789"
