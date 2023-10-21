import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from encryption import AES256Decryptor
import base64
import os


def authenticate(callback):
    def on_close():
        exit()


    def check_credentials():
        msp = os.path.expandvars(r'C:\Users\%username%\AppData\Local\mypasswd\msp.txt')
        master_password = password_entry.get()
        with open(msp, "r") as masterpass:
            pass_decode = base64.b64decode(masterpass.read())
            pass_decryption = AES256Decryptor(passphrase=master_password)
            try:
                pass_decryption.decrypt_text(pass_decode)
                callback(master_password)
                root.destroy()
                root.quit()
            except ValueError:
                messagebox.showerror(title="error", message="Wrong Password")

    root = tk.Tk()
    root.title("Authentication")
    root.geometry("300x150")
    root.resizable(False, False)

    padding_frame = ttk.Frame(root, padding=20)
    padding_frame.pack()

    password_label = ttk.Label(padding_frame, text="Master Password:", font=("Comic Sans MS", 12, "bold"))
    password_label.pack()

    password_entry = ttk.Entry(padding_frame, show="•", width=20, font=("arial", 14))
    password_entry.pack()

    style = ttk.Style()
    style.configure("Cute.TButton",
                    background="pink",
                    foreground="black",
                    font=("Comic Sans MS", 12, "bold"),
                    relief="flat",
                    borderwidth=2,
                    width=6,
                    padding=4)

    login_button = ttk.Button(padding_frame, text="Login", command=check_credentials, style="Cute.TButton")
    login_button.pack()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
