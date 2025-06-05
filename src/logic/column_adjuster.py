# src/logic/column_adjuster.py
import tkinter as tk
from tkinter import ttk, font
import pandas as pd
import logging
from src.models.config import df_full
from src.gui.widgets import update_selected_row  # Cambiado aquí

def auto_adjust_columns(tree, df):
    logging.info("Adjusting columns based on content...")
    font_name = ttk.Style().lookup('Treeview', 'font')
    font_obj = font.nametofont(font_name) if font_name else font.Font(family='TkDefaultFont', size=10)
    
    if df is None:
        logging.warning("No data provided. Skipping column adjustment.")
        return
    
    for col in tree['columns']:
        header_width = font_obj.measure(col.title())
        sample_size = min(500, len(df))
        content_width = max(df[col].iloc[:sample_size].apply(lambda x: font_obj.measure(str(x)) if pd.notna(x) else 0))
        padding = 20
        col_width = max(header_width, content_width) + padding
        tree.column(col, width=int(col_width))
        logging.info(f"Column '{col}' adjusted to {int(col_width)} pixels")

def load_rows_progressively(tree, df, batch_size=100, row_label=None, total_label=None):
    logging.info("Loading rows progressively...")
    tree.unbind('<<TreeviewSelect>>')
    if df is None:
        logging.warning("No data provided to load_rows_progressively. Skipping.")
        return
    
    total_rows = len(df)
    for start in range(0, total_rows, batch_size):
        end = min(start + batch_size, total_rows)
        for index in range(start, end):
            row = df.iloc[index]
            tree.insert('', tk.END, values=list(row))
        tree.winfo_toplevel().update_idletasks()
    
    loaded_rows = len(tree.get_children())
    row_label.config(text=f"Record 0 of {loaded_rows}")
    total_label.config(text=f"Total records: {total_rows}")
    tree.bind('<<TreeviewSelect>>', lambda e: update_selected_row(tree, row_label, total_label, df))
    logging.info(f"Load completed: {loaded_rows} rows loaded in Treeview")
    auto_adjust_columns(tree, df)  # Pasar df como parámetro