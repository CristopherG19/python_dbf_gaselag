# src/logic/column_adjuster.py
import tkinter as tk
from tkinter import ttk, font
import pandas as pd
import logging
from src.models.config import df_full
from src.gui.widgets import update_selected_row  # Cambiado aquí

def auto_adjust_columns(tree):
    logging.info("Ajustando columnas según contenido...")
    font_name = ttk.Style().lookup('Treeview', 'font')
    font_obj = font.nametofont(font_name) if font_name else font.Font(family='TkDefaultFont', size=10)
    
    for col in tree['columns']:
        header_width = font_obj.measure(col.title())
        sample_size = min(500, len(df_full))
        content_width = max(df_full[col].iloc[:sample_size].apply(lambda x: font_obj.measure(str(x)) if pd.notna(x) else 0))
        padding = 20
        col_width = max(header_width, content_width) + padding
        tree.column(col, width=int(col_width))
        logging.info(f"Columna '{col}' ajustada a {int(col_width)} píxeles")

def load_rows_progressively(tree, df, batch_size=100, row_label=None, total_label=None):
    logging.info("Cargando filas progresivamente...")
    tree.unbind('<<TreeviewSelect>>')
    total_rows = len(df)
    for start in range(0, total_rows, batch_size):
        end = min(start + batch_size, total_rows)
        for index in range(start, end):
            row = df.iloc[index]
            tree.insert('', tk.END, values=list(row))
        tree.winfo_toplevel().update_idletasks()
    
    loaded_rows = len(tree.get_children())
    row_label.config(text=f"Registro 0 de {loaded_rows}")
    total_label.config(text=f"Total registros: {total_rows}")
    tree.bind('<<TreeviewSelect>>', lambda e: update_selected_row(tree, row_label, total_label, df))
    logging.info(f"Carga completada: {loaded_rows} filas cargadas en el Treeview")
    auto_adjust_columns(tree)