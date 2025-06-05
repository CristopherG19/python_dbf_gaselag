# src/gui/main_window.py
import logging
import tkinter as tk
from tkinter import ttk
import os
from src.data.dbf_reader import load_dbf_data
from src.data.csv_writer import save_to_file
from src.logic.column_adjuster import load_rows_progressively
from src.gui.detail_window import show_details
from src.gui.widgets import update_selected_row  # Cambiado aquí
from src.models.config import df_full, current_file

def load_new_file(tree, root, row_label, total_label):
    global df_full, current_file
    from tkinter import filedialog
    file_path = filedialog.askopenfilename(
        title="Selecciona archivo .dbf",
        filetypes=[("Archivos DBF", "*.dbf"), ("Todos los archivos", "*.*")]
    )
    if file_path:
        new_df = load_dbf_data(file_path)
        if new_df is not None:
            for item in tree.get_children():
                tree.delete(item)
            tree["columns"] = list(new_df.columns)
            for col in tree["columns"]:
                tree.heading(col, text=col)
                tree.column(col, width=120, anchor='w', stretch=False)
            df_full = new_df
            current_file = file_path
            root.title(os.path.basename(file_path))
            load_rows_progressively(tree, new_df, row_label=row_label, total_label=total_label)
        else:
            logging.warning(f"No se pudo cargar el archivo {file_path}. No se cargaron datos.")

def show_data_in_grid(df=None):
    global df_full, current_file
    root = tk.Tk()
    root.title("Visualizador de Archivos DBF" if df is None else f"Datos de {os.path.basename(current_file)}")
    root.geometry("1200x700")
    
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    main_frame = ttk.Frame(root)
    main_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    
    tree = ttk.Treeview(main_frame, columns=[] if df is None else list(df.columns), show='headings')
    if df is not None:
        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor='w', stretch=False)
    
    vsb = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')
    
    controls_frame = ttk.Frame(root)
    controls_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
    
    btn_frame = ttk.Frame(controls_frame)
    btn_frame.pack(side='left', fill='x', expand=True)
    
    ttk.Button(btn_frame, text="Cargar Archivo DBF", 
              command=lambda: load_new_file(tree, root, row_label, total_label)).pack(side='left', padx=2)
    ttk.Button(btn_frame, text="Guardar Cambios", 
              command=lambda: save_to_file(df_full)).pack(side='left', padx=2)
    
    info_frame = ttk.Frame(controls_frame)
    info_frame.pack(side='right', fill='x')
    
    total_rows = 0 if df is None else len(df)
    row_label = ttk.Label(info_frame, text=f"Registro 0 de {total_rows}", font=('Arial', 10))
    row_label.pack(side='left', padx=10)
    
    total_label = ttk.Label(info_frame, text=f"Total registros: {total_rows}", font=('Arial', 10))
    total_label.pack(side='left', padx=10)
    
    if df is not None:
        df_full = df
        load_rows_progressively(tree, df, row_label=row_label, total_label=total_label)
    
    tree.bind('<Double-1>', lambda e: show_details(e, tree, df_full, current_file))
    tree.bind('<<TreeviewSelect>>', lambda e: update_selected_row(tree, row_label, total_label, df_full))
    
    root.mainloop()