import os
from datetime import datetime

RUTA_LOGS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "sistema.log")

def _asegurar_carpeta_logs():
    carpeta = os.path.dirname(RUTA_LOGS)
    os.makedirs(carpeta, exist_ok=True)

def registrar_evento(nivel, mensaje):
    _asegurar_carpeta_logs()
    marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{marca_tiempo}] [{nivel.upper()}] {mensaje}\n"
    try:
        with open(RUTA_LOGS, "a", encoding="utf-8") as archivo:
            archivo.write(linea)
    except Exception as e:
        print(f"No se pudo escribir en el log: {e}")

def registrar_info(mensaje):
    registrar_evento("INFO", mensaje)

def registrar_error(mensaje):
    registrar_evento("ERROR", mensaje)