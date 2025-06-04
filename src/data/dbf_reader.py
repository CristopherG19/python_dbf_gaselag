import pandas as pd
from dbfread import DBF
from datetime import datetime
import logging
from tkinter import messagebox
from src.models.config import date_fields, logical_fields
from src.logic.data_processor import convert_logical

def load_dbf_data(file_path):
    global date_fields, logical_fields
    try:
        table = DBF(file_path, encoding='latin1', raw=True)
        
        date_fields.clear()
        logical_fields.clear()
        date_fields.extend([field.name for field in table.fields if field.type == 'D'])
        logical_fields.extend([field.name for field in table.fields if field.type == 'L'])
        logging.info(f"Campos de fecha detectados: {date_fields}")
        logging.info(f"Campos lógicos detectados: {logical_fields}")
        
        data = []
        for record in table:
            new_record = {}
            for field_name, value in record.items():
                try:
                    if field_name in date_fields and value:
                        if isinstance(value, bytes):
                            date_str = value.decode('latin1').strip()
                            if date_str:
                                date_obj = datetime.strptime(date_str, '%Y%m%d')
                                new_record[field_name] = date_obj.strftime('%d/%m/%Y')
                            else:
                                new_record[field_name] = ""
                        else:
                            new_record[field_name] = value.strftime('%d/%m/%Y') if pd.notnull(value) else ""
                    elif field_name in logical_fields:
                        new_record[field_name] = convert_logical(value)
                    elif isinstance(value, bytes):
                        new_record[field_name] = value.decode('latin1').strip()
                    else:
                        new_record[field_name] = str(value).strip() if value is not None else ""
                except Exception as e:
                    logging.error(f"Error al procesar el campo {field_name} con valor {value}: {str(e)}")
                    new_record[field_name] = ""
            data.append(new_record)
        
        df = pd.DataFrame(data)
        logging.info(f"Datos cargados correctamente desde {file_path}. Dimensiones: {df.shape}")
        logging.info(f"Primeras filas de los campos de fecha:\n{df[date_fields].head()}")
        logging.info(f"Primeras filas de los campos lógicos:\n{df[logical_fields].head()}")
        return df
    except Exception as e:
        logging.error(f"Error al cargar el archivo DBF {file_path}: {str(e)}")
        messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{str(e)}")
        return None