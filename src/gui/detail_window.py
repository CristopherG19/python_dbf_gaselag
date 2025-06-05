import os
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import logging
from src.models.config import date_fields, logical_fields, detail_window, df_full, loading

def close_detail_window():
    global detail_window
    if detail_window:
        detail_window.destroy()
        detail_window = None

def save_and_close(tree, detail_entries, selected_item):
    global detail_window, df_full
    if detail_window and df_full is not None:
        item = tree.index(selected_item)
        values = []
        for col, entry in zip(tree['columns'], detail_entries):
            if col in date_fields:
                values.append(entry.get())
            elif col in logical_fields:
                values.append(entry.get())
            else:
                values.append(entry.get().strip())
        tree.item(selected_item, values=values)
        df_full.iloc[item] = values
        logging.info(f"Registro {item + 1} actualizado: {values}")
        close_detail_window()

def show_details(event, tree, df_full, current_file):
    global detail_window, loading
    if loading or detail_window is not None or not tree.selection():
        return
    
    selected_item = tree.selection()[0]
    item = tree.item(selected_item)
    values = item['values']
    columns = tree['columns']
    
    detail_window = tk.Toplevel()
    detail_window.title(f"Editor registro - {os.path.basename(current_file)}")
    detail_window.geometry("450x600")
    detail_window.resizable(False, False)
    
    detail_window.protocol("WM_DELETE_WINDOW", close_detail_window)
    
    frame = ttk.Frame(detail_window)
    frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    canvas = tk.Canvas(frame)
    scrollbar = ttk.Scrollbar(frame, orient='vertical', command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')
    canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
    
    detail_entries = []
    
    for i, (col, val) in enumerate(zip(columns, values)):
        ttk.Label(scrollable_frame, text=f"{col}:", font=('Arial', 10, 'bold'), 
             anchor='e', width=15).grid(row=i, column=0, sticky='e', pady=2)
    
        if col in date_fields:
            entry = DateEntry(scrollable_frame, width=27, font=('Arial', 10), date_pattern='dd/mm/yyyy')
            if val and val.strip():
                try:
                    date_obj = datetime.strptime(val, '%d/%m/%Y')
                    entry.set_date(date_obj)
                except ValueError as e:
                        logging.warning(f"Error al parsear fecha en {col}: {val}, {str(e)}")
                        entry.set_date(datetime.now())
            else:
                entry.set_date(datetime.now())
            entry.grid(row=i, column=1, sticky='w', padx=5)
        elif col in logical_fields:
            var = tk.BooleanVar(value=val if isinstance(val, bool) else False)
            entry = ttk.Checkbutton(scrollable_frame, variable=var)
            entry.grid(row=i, column=1, sticky='w', padx=5)
            entry.get = var.get
        else:
            # MASIVO caerá aquí y se mostrará como Entry
            entry = ttk.Entry(scrollable_frame, width=30, font=('Arial', 10))
            entry.insert(0, str(val).strip())
            entry.grid(row=i, column=1, sticky='w', padx=5)
    
        detail_entries.append(entry)
    
    btn_frame = ttk.Frame(scrollable_frame)
    btn_frame.grid(row=len(columns), column=0, columnspan=2, pady=10)
    
    ttk.Button(btn_frame, text="OK", 
              command=lambda: save_and_close(tree, detail_entries, selected_item)).pack(side='left', padx=5)
    ttk.Button(btn_frame, text="Cancel", command=close_detail_window).pack(side='left', padx=5)