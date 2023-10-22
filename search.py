import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
from encryption import AES256Decryptor
import base64
import pyperclip

master_password = None


def search(callback):


    global master_password
    FONT = ("Comic Sans MS", 14)
    file_path = os.path.expandvars(r'C:\Users\%username%\AppData\Local\mypasswd\db.json')
    master_password = callback
    passwd = None

    def search_json():
        global master_password
        keyword = search_entry.get()
        global passwd
        with open(file_path, 'r') as file:
            data = json.load(file)

            if keyword in data:
                password_entry.configure(show='•')
                decryption = AES256Decryptor(passphrase=master_password)
                user_decryption = decryption.decrypt_text(ciphertext=base64.b64decode(data[keyword]["user"]))
                password_decryption = decryption.decrypt_text(ciphertext=base64.b64decode(data[keyword]["password"]))
                user_entry.configure(state='normal')
                password_entry.configure(state='normal')
                passwd = password_decryption
                user_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)

                user_entry.insert(tk.END, user_decryption)
                password_entry.insert(tk.END, password_decryption)

                user_entry.configure(state='readonly')
                password_entry.configure(state='readonly')
            else:
                messagebox.showerror(message="Password not found!")
                user_entry.configure(state='normal')
                password_entry.configure(state='normal')
                user_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
                user_entry.configure(state='readonly')
                password_entry.configure(state='readonly')

    def show_keys():
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                keys = list(data.keys())

                keys_window = tk.Toplevel(root)
                keys_window.title("Available Passwords")
                keys_window.geometry("300x200")

                keys_frame = ttk.Frame(keys_window, padding=0)
                keys_frame.pack(fill='both', expand=True)

                keys_listbox = tk.Listbox(keys_frame, font=FONT)
                keys_listbox.pack(side='left', fill='both', expand=True)

                keys_scrollbar = ttk.Scrollbar(keys_frame, command=keys_listbox.yview)
                keys_scrollbar.pack(side='right', fill='y')

                keys_listbox.config(yscrollcommand=keys_scrollbar.set)

                for key in keys:
                    keys_listbox.insert(tk.END, key)

                values_text = tk.Text(keys_window, state='disabled')
                values_text.pack(fill='both', expand=True)
        except FileNotFoundError:
            messagebox.showerror(message="No data found!")
            root.destroy()
            root.quit()

    def copy():
        global passwd
        pyperclip.copy(passwd)

    def view():
        global passwd
        password_entry.configure(state='normal')
        password_entry.delete(0, tk.END)
        password_entry.insert(tk.END, passwd)
        password_entry.configure(show='')
        password_entry.configure(state='readonly')

    def delete():
        global passwd
        keyword = search_entry.get()
        with open(file_path, 'r') as file:
            data = json.load(file)
            if keyword in data:
                confirm = messagebox.askyesno("Delete Password!", f"Do you want to delete the entry for {keyword}?")
                if confirm:
                    del data[keyword]
                    with open(file_path, 'w') as file:
                        json.dump(data, file, indent=4)
                    user_entry.configure(state='normal')
                    password_entry.configure(state='normal')
                    user_entry.delete(0, tk.END)
                    password_entry.delete(0, tk.END)
                    user_entry.configure(state='readonly')
                    password_entry.configure(state='readonly')
                    passwd = None

    root = tk.Tk()
    root.title("Search Passwords")
    root.geometry("500x200")
    root.resizable(False, False)

    padding_frame = ttk.Frame(root)
    padding_frame.pack()

    search_label = ttk.Label(padding_frame, text="Search Password:", font=FONT)
    search_label.grid(row=0, column=0, padx=5, pady=5)

    search_entry = ttk.Entry(padding_frame)
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    user_label = ttk.Label(padding_frame, text="User:", font=FONT)
    user_label.grid(row=1, column=0, padx=5, pady=5)

    user_entry = ttk.Entry(padding_frame, state='readonly')
    user_entry.grid(row=1, column=1, padx=5, pady=5)

    password_label = ttk.Label(padding_frame, text="Password:", font=FONT)
    password_label.grid(row=2, column=0, padx=5, pady=5)

    password_entry = ttk.Entry(padding_frame, state='readonly', show='•')
    password_entry.grid(row=2, column=1, padx=5, pady=5)

    style = ttk.Style()
    style.configure("Search.TButton",
                    background="pink",
                    foreground="black",
                    font=("Comic Sans MS", 12, "bold"),
                    relief="flat",
                    borderwidth=2,
                    width=6,
                    padding=4)

    search_button = ttk.Button(padding_frame, text="Search", command=search_json, style="Search.TButton")
    search_button.grid(row=3, column=0, padx=5, pady=5)

    show_button = ttk.Button(padding_frame, text="Show", command=show_keys, style="Search.TButton")
    show_button.grid(row=3, column=1, padx=5, pady=5)

    cp_style = ttk.Style()
    cp_style.configure("cp.TButton",
                       background="pink",
                       foreground="black",
                       font=("Comic Sans MS", 8),
                       relief="flat",
                       borderwidth=2,
                       width=4,
                       padding=2)

    cp = ttk.Button(padding_frame, text="Copy", command=copy, style="cp.TButton")
    cp.grid(row=2, column=2, padx=5, pady=5)
    reveal = ttk.Button(padding_frame, text="View", command=view, style="cp.TButton")
    reveal.grid(row=2, column=3, padx=5, pady=5)
    delete_button = ttk.Button(padding_frame, text="Delete", command=delete, style="Search.TButton")
    delete_button.grid(row=3, column=2, padx=5, pady=5)


    root.mainloop()
