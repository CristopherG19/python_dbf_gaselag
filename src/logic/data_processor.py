import logging

def convert_logical(value):
    if isinstance(value, bytes):
        try:
            value = value.decode('latin1').strip()
        except UnicodeDecodeError as e:
            logging.error(f"Error al decodificar valor lógico: {value}, {str(e)}")
            return None
    if value == "S":
        return True
    elif value == "N":
        return False
    else:
        logging.warning(f"Valor inesperado en campo lógico: {value}")
        return None