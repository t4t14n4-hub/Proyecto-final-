# ---------------------------------------------------------------------
# guardado_json.py
# ---------------------------------------------------------------------
# Módulo para guardar y cargar múltiples simulaciones del simulador
# de plantas en formato JSON.
# Cada simulación se guarda como un diccionario con un número y sus datos.
# ---------------------------------------------------------------------

import json
import os

# Ruta al archivo JSON dentro de la carpeta /data
BASE_DIR = os.path.dirname(__file__)
ARCHIVO_DATOS = os.path.join(BASE_DIR, "data", "guardado.json")

# Valores por defecto de cada planta
VALORES_IDEALES_POR_DEFECTO = {
    "agua": [70, 90],
    "luz": [6, 10],
    "temp": [18, 28]
}

# Estado por defecto de una simulación
SIMULACION_POR_DEFECTO = {
    "numero": 1,
    "alturas": [3, 3, 3, 3],
    "muertas": [False, False, False, False],
    "agua": [80, 80, 80, 80],
    "luz": [8, 8, 8, 8],
    "temp": [22, 22, 22, 22]
}


def cargar_simulaciones():
    """
    Carga todas las simulaciones guardadas.
    Devuelve una lista de simulaciones.
    Si no existe archivo, devuelve lista vacía.
    """
    if not os.path.exists(ARCHIVO_DATOS):
        print("No se encontró archivo guardado. Se usarán valores por defecto.")
        return []

    try:
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as f:
            datos = json.load(f)
            if not isinstance(datos, list):
                return []
            return datos
    except (json.JSONDecodeError, FileNotFoundError):
        print("Error al leer el archivo. Se usarán valores por defecto.")
        return []


def guardar_simulacion(simulacion):
    """
    Guarda una nueva simulación en la lista de simulaciones del archivo JSON.
    Asigna automáticamente un número consecutivo a la simulación.
    """
    simulaciones = cargar_simulaciones()
    simulacion["numero"] = len(simulaciones) + 1
    simulaciones.append(simulacion)

    # Asegurarse de que la carpeta data exista
    carpeta_data = os.path.join(BASE_DIR, "data")
    os.makedirs(carpeta_data, exist_ok=True)

    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as f:
        json.dump(simulaciones, f, indent=4, ensure_ascii=False)


def reiniciar_guardado():
    """
    Elimina todas las simulaciones guardadas.
    """
    if os.path.exists(ARCHIVO_DATOS):
        os.remove(ARCHIVO_DATOS)