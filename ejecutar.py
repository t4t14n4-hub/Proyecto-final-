# ---------------------------------------------------------------------
# ejecutar.py
# ---------------------------------------------------------------------
# Archivo principal del simulador de crecimiento de plantas 🌱
# Se encarga únicamente de iniciar la interfaz gráfica.
# ---------------------------------------------------------------------

from interfaz import SimuladorPlantas
import tkinter as tk

def main():
    root = tk.Tk()
    app = SimuladorPlantas(root)
    root.mainloop()

if __name__ == "__main__":
    main()