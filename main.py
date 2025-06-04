import logging
import os
from src.utils.logger import setup_logging
from src.gui.main_window import show_data_in_grid
from src.data.dbf_reader import load_dbf_data

if __name__ == "__main__":
    setup_logging()  # Configurar logging
    logging.info("Iniciando la aplicación")
    initial_file = None  # Especificar un archivo inicial si es necesario
    
    if initial_file and os.path.exists(initial_file):
        df = load_dbf_data(initial_file)
        show_data_in_grid(df)
    else:
        show_data_in_grid()