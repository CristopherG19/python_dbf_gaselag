import json
import os
import bcrypt
import logging
from tkinter import messagebox

USERS_FILE = os.path.join("data", "users.json")

def load_users():
    """Load users from the JSON file."""
    try:
        if not os.path.exists(USERS_FILE):
            logging.error(f"User file {USERS_FILE} not found.")
            messagebox.showerror("Error", f"User file {USERS_FILE} not found.")
            return []
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("users", [])
    except Exception as e:
        logging.error(f"Error loading users: {str(e)}")
        messagebox.showerror("Error", f"Failed to load user file:\n{str(e)}")
        return []

def validate_user(username, password):
    """Validate user credentials."""
    users = load_users()
    for user in users:
        if user["username"] == username:
            try:
                if bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
                    logging.info(f"User {username} authenticated successfully.")
                    return True
                else:
                    logging.warning(f"Invalid password for user {username}.")
                    return False
            except Exception as e:
                logging.error(f"Error validating password for {username}: {str(e)}")
                return False
    logging.warning(f"User {username} not found.")
    return False