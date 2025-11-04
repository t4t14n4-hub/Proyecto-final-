# ------------------------------------------------------------
# tests/test_logica.py
# ------------------------------------------------------------
# Pruebas unitarias para verificar el funcionamiento de la lógica
# del simulador de crecimiento de plantas.
# Estas pruebas evalúan distintos escenarios de agua, luz y temperatura
# para asegurar que la función de crecimiento responda correctamente.
# ------------------------------------------------------------

import pytest
from logica import calcular_crecimiento, MUERTE, VALORES_IDEALES

# --- 1. Crecimiento ideal ---
def test_crecimiento_ideal():
    """Si las condiciones son ideales, el crecimiento debe ser positivo."""
    ideal = VALORES_IDEALES
    agua = (ideal["agua"][0] + ideal["agua"][1]) / 2
    luz = (ideal["luz"][0] + ideal["luz"][1]) / 2
    temp = (ideal["temp"][0] + ideal["temp"][1]) / 2
    crecimiento = calcular_crecimiento(agua, luz, temp)
    assert crecimiento > 0

# --- 2. Déficit moderado de agua ---
def test_crecimiento_bajo_agua_moderado():
    """Si el agua está un poco por debajo del rango ideal, el crecimiento debe ser menor pero no nulo."""
    ideal = VALORES_IDEALES
    agua = ideal["agua"][0] - 40
    luz = (ideal["luz"][0] + ideal["luz"][1]) / 2
    temp = (ideal["temp"][0] + ideal["temp"][1]) / 2
    crecimiento = calcular_crecimiento(agua, luz, temp)
    assert crecimiento >= -1

# --- 3. Exceso extremo de agua (muerte) ---
def test_muerte_por_exceso_de_agua():
    """Si el agua excede el límite de tolerancia, la planta muere."""
    ideal = VALORES_IDEALES
    agua = ideal["agua"][1] + 100
    luz = (ideal["luz"][0] + ideal["luz"][1]) / 2
    temp = (ideal["temp"][0] + ideal["temp"][1]) / 2
    crecimiento = calcular_crecimiento(agua, luz, temp)
    assert crecimiento == MUERTE

# --- 4. Falta total de luz ---
def test_muerte_por_falta_de_luz():
    """Si no hay luz, la planta muere."""
    ideal = VALORES_IDEALES
    agua = (ideal["agua"][0] + ideal["agua"][1]) / 2
    luz = 0
    temp = (ideal["temp"][0] + ideal["temp"][1]) / 2
    crecimiento = calcular_crecimiento(agua, luz, temp)
    assert crecimiento == MUERTE

# --- 5. Temperatura fuera de rango tolerable ---
def test_muerte_por_temperatura_extrema():
    """Si la temperatura está muy por debajo o muy por encima del rango ideal, la planta muere."""
    ideal = VALORES_IDEALES
    agua = (ideal["agua"][0] + ideal["agua"][1]) / 2
    luz = (ideal["luz"][0] + ideal["luz"][1]) / 2
    temp = ideal["temp"][1] + 20
    crecimiento = calcular_crecimiento(agua, luz, temp)
    assert crecimiento == MUERTE