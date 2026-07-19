import tkinter as tk
from tkinter import messagebox
from auth import register_user, login_user
from dashboard import FinanceDashboard

root = tk.Tk()
root.title("Finance Tracker Login")
root.geometry("400x300")

tk.Label(root,text="Username").pack(pady=5)

username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root,text="Password").pack(pady=5)

password_entry = tk.Entry(root,show="*")
password_entry.pack()

def register():

    username = username_entry.get()
    password = password_entry.get()

    if register_user(username,password):
        messagebox.showinfo(
            "Success",
            "Registration Successful"
        )
    else:
        messagebox.showerror(
            "Error",
            "Username Already Exists"
        )
def login():

    username = username_entry.get()
    password = password_entry.get()

    user = login_user(
        username,
        password
    )

    if user:

        user_id = user[0]

        root.destroy()

        dashboard_root = tk.Tk()

        
        FinanceDashboard(
             dashboard_root,
             user_id
        )

        dashboard_root.mainloop()

    else:

        messagebox.showerror(
            "Error",
            "Invalid Credentials"
        )


tk.Button(
    root,
    text="Register",
    command=register
).pack(pady=10)

tk.Button(
    root,
    text="Login",
    command=login
).pack()


root.mainloop()