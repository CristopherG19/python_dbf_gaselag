def update_selected_row(tree, row_label, total_label, df_full):
    selected_item = tree.selection()
    if selected_item:
        item = tree.index(selected_item)
        loaded_rows = len(tree.get_children())
        total_rows = len(df_full) if df_full is not None else 0
        row_label.config(text=f"Registro {item + 1} de {loaded_rows}")
        total_label.config(text=f"Total registros: {total_rows}")