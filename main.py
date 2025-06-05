import logging
from src.utils.logger import setup_logging
from src.gui.login_window import show_login_window

if __name__ == "__main__":
    setup_logging()
    logging.info("Starting the application")
    show_login_window()