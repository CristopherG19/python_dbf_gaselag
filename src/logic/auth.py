from src.data.user_manager import validate_user
from tkinter import messagebox

def authenticate(username, password):
    """Authenticate a user and return True if successful."""
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return False
    if validate_user(username, password):
        return True
    messagebox.showerror("Error", "Invalid username or password.")
    return False