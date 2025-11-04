# ---------------------------------------------------------------------
# logica_plantas.py
# ---------------------------------------------------------------------
# Contiene la lógica del simulador:
# - Cálculo del crecimiento de plantas
# - Manejo de condiciones extremas
# - Inicialización y reinicio de simulaciones
# - Interacción con archivo JSON para guardar y cargar progresos
# ---------------------------------------------------------------------

# --- Valores ideales para plantas de tomate ---
VALORES_IDEALES = {
    "agua": (70, 90),   # Rango en ml
    "luz": (6, 10),     # Rango en horas de exposición
    "temp": (18, 28)    # Rango en °C
}

# Constante que indica que la planta muere
MUERTE = -999  

# ---------------------------------------------------------------------
# Función principal de cálculo de crecimiento
# ---------------------------------------------------------------------
def calcular_crecimiento(agua, luz, temp):
    """
    Calcula el cambio en altura de la planta según los valores de
    agua, luz y temperatura ingresados.

    Reglas de crecimiento:
    - Condiciones ideales → +6 cm
    - Dentro de tolerancia extendida → +3 cm
    - Fuera de tolerancia pero cercanas → +1 cm
    - Condiciones extremas → MUERTE (-999)

    Se toma el factor más restrictivo como limitante del crecimiento.
    """

    # Extraemos los rangos ideales
    a_min, a_max = VALORES_IDEALES["agua"]
    l_min, l_max = VALORES_IDEALES["luz"]
    t_min, t_max = VALORES_IDEALES["temp"]

    # --- Función auxiliar para evaluar la contribución de cada factor ---
    def evaluar_factor(valor, minimo, maximo, tol_extendida, tol_cercana):
        """
        Determina cuánto contribuye un factor al crecimiento.
        Args:
            valor: valor ingresado del factor (agua, luz, temp)
            minimo, maximo: rango ideal
            tol_extendida: tolerancia extendida (crecimiento +3)
            tol_cercana: tolerancia cercana (crecimiento +1)
        Returns:
            Entero: 6, 3, 1 o MUERTE
        """
        if minimo <= valor <= maximo:
            return 6        # Condición ideal
        elif (minimo - tol_extendida) <= valor < minimo or maximo < valor <= (maximo + tol_extendida):
            return 3        # Dentro de tolerancia extendida
        elif (minimo - tol_extendida - tol_cercana) <= valor < (minimo - tol_extendida) or \
             (maximo + tol_extendida) < valor <= (maximo + tol_extendida + tol_cercana):
            return 1        # Fuera pero cercano
        else:
            return MUERTE    # Condición extrema → planta muere

    # Evaluamos cada factor
    crecimiento_agua = evaluar_factor(agua, a_min, a_max, tol_extendida=50, tol_cercana=10)
    crecimiento_luz = evaluar_factor(luz, l_min, l_max, tol_extendida=2, tol_cercana=2)
    crecimiento_temp = evaluar_factor(temp, t_min, t_max, tol_extendida=2, tol_cercana=2)

    # Si algún factor indica MUERTE, la planta muere
    if MUERTE in [crecimiento_agua, crecimiento_luz, crecimiento_temp]:
        return MUERTE

    # Retornamos el valor más restrictivo como limitante
    return min(crecimiento_agua, crecimiento_luz, crecimiento_temp)


# ---------------------------------------------------------------------
# Funciones para manejar datos de la simulación
# ---------------------------------------------------------------------
from guardado_json import guardar_simulacion, cargar_simulaciones, reiniciar_guardado

def valores_iniciales():
    """
    Devuelve los valores iniciales de la simulación actual:
    - Altura inicial de cada planta: 3 cm
    - Estado de cada planta: viva (False = no muerta)
    """
    return {"alturas": [3, 3, 3, 3], "muertas": [False, False, False, False]}

def reiniciar_simulacion_actual():
    """
    Devuelve los valores iniciales de la simulación actual.
    No toca los datos guardados previamente.
    """
    return valores_iniciales()

def inicializar_datos():
    """
    Carga datos guardados desde JSON.
    Si no hay datos guardados, devuelve valores iniciales por defecto.
    """
    datos = cargar_simulaciones()
    if datos is None:
        datos = valores_iniciales()
    return datos

def guardar_estado(datos):
    """
    Guarda la simulación actual en el archivo JSON.
    Se llama cuando el usuario decide guardar su progreso.
    """
    guardar_simulacion(datos)








