import tkinter as tk
from tkinter import ttk
from src.logic.auth import authenticate
from src.gui.main_window import show_data_in_grid
import logging

def show_login_window():
    """Display the login window."""
    login_root = tk.Tk()
    login_root.title("Login - DBF Viewer")
    login_root.geometry("300x200")
    login_root.resizable(False, False)

    frame = ttk.Frame(login_root)
    frame.pack(padx=20, pady=20, fill='both', expand=True)

    ttk.Label(frame, text="Username:", font=('Arial', 10)).grid(row=0, column=0, sticky='e', pady=5)
    username_entry = ttk.Entry(frame, width=20)
    username_entry.grid(row=0, column=1, pady=5)

    ttk.Label(frame, text="Password:", font=('Arial', 10)).grid(row=1, column=0, sticky='e', pady=5)
    password_entry = ttk.Entry(frame, width=20, show="*")
    password_entry.grid(row=1, column=1, pady=5)

    def on_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        if authenticate(username, password):
            login_root.destroy()  # Close login window
            show_data_in_grid()   # Open main window
        else:
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)

    ttk.Button(frame, text="Login", command=on_login).grid(row=2, column=0, columnspan=2, pady=10)

    login_root.mainloop()