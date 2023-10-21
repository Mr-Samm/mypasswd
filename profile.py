import os
import ctypes
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from encryption import *
import base64

master_pass = ""


def create_master_password():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("First Time Setup",
                        "This is your first time using mypasswd password manager. Please create a master password.")
    password_window = tk.Toplevel(root)
    password_window.title("Create Master Password")
    password_window.configure(bg="#F0F0F0")

    font = ("Comic Sans MS", 14)

    password_label = tk.Label(password_window, text="Password:", bg="#F0F0F0", font=font)
    password_label.pack(pady=10)

    password_entry = tk.Entry(password_window, show="*", font=font)
    password_entry.pack(pady=5)

    confirm_label = tk.Label(password_window, text="Confirm Password:", bg="#F0F0F0", font=font)
    confirm_label.pack(pady=10)

    confirm_entry = tk.Entry(password_window, show="*", font=font)
    confirm_entry.pack(pady=5)

    def check_password():
        global master_pass
        password = password_entry.get()
        confirm_password = confirm_entry.get()

        if not password or not confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
        elif password == confirm_password:
            messagebox.showinfo("Success", "Master password created successfully.")
            messagebox.showinfo("Success", "Please reopen your password manager Enjoy :).")
            password_window.destroy()
            password_window.quit()
            master_pass = confirm_password

        else:
            messagebox.showerror("Error", "Passwords do not match.")

    style = tk.ttk.Style()
    style.configure("Cute.TButton",
                    background="pink",
                    foreground="black",
                    font=("Comic Sans MS", 12, "bold"),
                    relief="flat",
                    borderwidth=2,
                    width=6,
                    padding=4)

    save_button = ttk.Button(password_window, text="Save", command=check_password, style="Cute.TButton")
    save_button.pack(pady=20)

    window_width = 300
    window_height = 270
    screen_width = password_window.winfo_screenwidth()
    screen_height = password_window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    password_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    password_window.mainloop()


def create_profile():
    global master_pass
    folder_path = os.path.expandvars(r'C:\Users\%username%\AppData\Local\mypasswd')
    msp = os.path.expandvars(r'C:\Users\%username%\AppData\Local\mypasswd\msp.txt')

    if os.path.exists(folder_path):
        print("folder exist")
        return

    try:
        os.makedirs(folder_path, exist_ok=True)
        ctypes.windll.kernel32.SetFileAttributesW(folder_path, 2)
        create_master_password()
        encryption = AES256Encryptor(passphrase=master_pass)
        encryption_text = encryption.encrypt_text(text=master_pass)
        encode_encryption = base64.b64encode(encryption_text).decode()
        with open(msp, "w") as master_p:
            master_p.write(encode_encryption)
        ctypes.windll.kernel32.SetFileAttributesW(msp, 2)

        return
    except OSError as e:
        with open("error.txt", "w") as error:
            error.write("failed to create profile please try again or check your system privileges")



