import random
from core import *
from tkinter import messagebox
import pyperclip
from encryption import AES256Encryptor
import json
import base64
from profile import create_profile
import os
from auth import authenticate
from search import search

folder_path = os.path.expandvars(r'C:\Users\%username%\AppData\Local\mypasswd')
file_path = os.path.expandvars(r'C:\Users\%username%\AppData\Local\mypasswd\db.json')
if not os.path.exists(folder_path):
    create_profile()
    exit()
else:
    pass

authenticated_password = None


def callback(password):
    global authenticated_password
    authenticated_password = password


def add_b():
    encryption = AES256Encryptor(passphrase=authenticated_password)
    encrypted_user = encryption.encrypt_text(text=user.user_en.get())
    encrypted_password = encryption.encrypt_text(text=password.pass_en.get())

    data = {
        url.url_en.get(): {
            "user": base64.b64encode(encrypted_user).decode(),
            "password": base64.b64encode(encrypted_password).decode(),
        }
    }

    if not url.url_en.get():
        messagebox.showwarning(title="Empty fields!", message="Please make sure to write URL")
    elif not user.user_en.get():
        messagebox.showwarning(title="Empty fields!", message="Please make sure to write USER/EMAIL")
    elif not password.pass_en.get():
        messagebox.showwarning(title="Empty fields!", message="Please make sure to write PASSWORD")

    else:
        ask = messagebox.askyesno(title="Save Login?",
                                  message=f"Would you like to save: {url.url_en.get()}\nUser/Email:  {user.user_en.get()}\nPassword: {password.pass_en.get()}\n")
        if ask:
            def disappear():
                msg.l.destroy()

            try:
                with open(file_path, "r") as database:
                    json_data = json.load(database)
            except FileNotFoundError:
                with open(file_path, "w") as database:
                    json.dump(data, database, indent=4)
                    msg = Message(message="Login saved successfully")
                    url.url_en.delete(0, tk.END)
                    user.user_en.delete(0, tk.END)
                    password.pass_en.delete(0, tk.END)
                window.after(4000, disappear)
            except json.decoder.JSONDecodeError:
                json_data = {}
                with open(file_path, "w") as database:
                    json.dump(data, database, indent=4)
                    msg = Message(message="Login saved successfully")
                    url.url_en.delete(0, tk.END)
                    user.user_en.delete(0, tk.END)
                    password.pass_en.delete(0, tk.END)
                window.after(4000, disappear)
            else:
                if url.url_en.get() in json_data:
                    messagebox.showerror(message=f"{url.url_en.get()} is already in the database")
                else:
                    json_data.update(data)
                    with open(file_path, "w") as database:
                        json.dump(json_data, database, indent=4)
                        msg = Message(message="Login saved successfully")
                        url.url_en.delete(0, tk.END)
                        user.user_en.delete(0, tk.END)
                        password.pass_en.delete(0, tk.END)
                        window.after(4000, disappear)
        else:
            pass


def pass_generate():
    password.pass_en.delete(0, tk.END)
    passwd = ""
    passwd_result = ""
    for x in range(5):
        passwd += (random.choice(letters))
        passwd += (random.choice(symbols))
        passwd += (random.choice(numbers))
    for y in passwd:
        passwd_result += random.choice(str(passwd))

    password.pass_en.insert(tk.END, passwd_result)


def copy():
    if not password.pass_en.get():
        copied = tk.Label(text="Empty!", font=("Comic Sans MS", 10), fg="red")
        copied.place(x=715, y=635)

        def disappear():
            copied.destroy()

        window.after(4000, disappear)
    else:
        pyperclip.copy(password.pass_en.get())
        copied = tk.Label(text="Copied!", font=("Comic Sans MS", 10))
        copied.place(x=715, y=635)

        def disappear():
            copied.destroy()

        window.after(4000, disappear)


def search_A():
    global authenticated_password
    search(authenticated_password)


authenticate(callback)
window = tk.Tk()
window.minsize(width=1000, height=800)
window.title("Mypasswd")
window.config(bg="white")
window.resizable(False, False)
logo = tk.PhotoImage(file="logo.png")
lb_logo = tk.Label(image=logo, borderwidth=0, bg="white")
lb_logo.pack()
url = URL()
user = User()
password = Password()
cp = Button(x=700, y=597, text="Copy", command=copy)
generate = Button(x=800, y=597, text="Generate", command=pass_generate, )
add = Button(x=400, y=650, text="Add", command=add_b)
search_b = Button(x=500, y=650, command=search_A, text="Search")

window.mainloop()
