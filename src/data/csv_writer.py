import pandas as pd
from tkinter import filedialog, messagebox
import logging
from src.models.config import date_fields, logical_fields

def save_to_file(df_full):
    if df_full is not None:
        try:
            output_file = filedialog.asksaveasfilename(
                title="Guardar como",
                defaultextension=".csv",
                filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
            )
            if output_file:
                df_to_save = df_full.copy()
                for col in date_fields:
                    df_to_save[col] = df_to_save[col].apply(lambda x: x if x else "")
                for col in logical_fields:
                    df_to_save[col] = df_to_save[col].apply(lambda x: "S" if x is True else "N" if x is False else "")
                df_to_save.to_csv(output_file, index=False, encoding='utf-8')
                logging.info(f"Datos guardados en {output_file}")
                messagebox.showinfo("Éxito", f"Datos guardados en:\n{output_file}")
        except Exception as e:
            logging.error(f"Error al guardar el archivo: {str(e)}")
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")