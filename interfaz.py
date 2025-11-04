# ---------------------------------------------------------------------
# interfaz_plantas.py
# ---------------------------------------------------------------------
# Interfaz gráfica del simulador de crecimiento de plantas.
# Usa Tkinter y Matplotlib, y llama a la lógica desde logica_plantas.py
# Soporta múltiples simulaciones guardadas.
# ---------------------------------------------------------------------

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

# --- Importaciones de la lógica y guardado ---
from logica import calcular_crecimiento, VALORES_IDEALES, MUERTE
from guardado_json import guardar_simulacion, cargar_simulaciones, reiniciar_guardado


class SimuladorPlantas:
    def __init__(self, root):
        self.root = root
        self.root.title("🌿 Simulador de Crecimiento de Plantas 🌿")
        self.root.geometry("1300x850")
        self.root.resizable(False, False)
        self.root.configure(bg="#fff9e6")
        self.pantalla_inicio()

    # -------------------------------------------------------
    # Pantalla de inicio
    # -------------------------------------------------------
    def pantalla_inicio(self):
        self.frame_inicio = ttk.Frame(self.root, padding=20)
        self.frame_inicio.pack(expand=True, fill="both")
        self.frame_inicio.configure(style="Custom.TFrame")

        titulo = ttk.Label(
            self.frame_inicio,
            text="🌱 Simulador de Crecimiento de Plantas 🌱",
            font=("Times New Roman", 22, "bold"),
            anchor="center",
            background="#fff9e6"
        )
        titulo.pack(pady=20)

        descripcion = (
            "Este programa permite observar cómo distintas condiciones ambientales\n"
            "(agua, luz solar y temperatura) afectan el crecimiento de una planta de tomate.\n\n"
            "Cada barra del gráfico representa una planta. Podés modificar sus condiciones\n"
            "y observar si crece (la barra sube) o muere (la barra baja o desaparece).\n\n"
            "💧 Agua: en mililitros (ml)\n"
            "☀️ Luz: en horas de exposición directa (h)\n"
            "🌡️ Temperatura: en grados Celsius (°C)"
        )
        ttk.Label(
            self.frame_inicio,
            text=descripcion,
            justify="center",
            wraplength=1200,
            font=("Times New Roman", 14),
            background="#fff9e6"
        ).pack(pady=15)

        ttk.Button(
            self.frame_inicio,
            text="➡️ Iniciar nueva simulación",
            command=self.iniciar_nueva_simulacion,
            style="TButton"
        ).pack(pady=10)

        ttk.Button(
            self.frame_inicio,
            text="📂 Ver simulaciones guardadas",
            command=self.mostrar_guardados,
            style="TButton"
        ).pack(pady=10)

    # -------------------------------------------------------
    # Nueva simulación
    # -------------------------------------------------------
    def iniciar_nueva_simulacion(self):
        self.frame_inicio.destroy()
        self.crear_simulador(reiniciar=True)

    # -------------------------------------------------------
    # Crear simulador (interfaz principal)
    # -------------------------------------------------------
    def crear_simulador(self, reiniciar=False, datos=None):
        if reiniciar or datos is None:
            datos = reiniciar_guardado() or {"alturas":[3,3,3,3],"muertas":[False]*4,"condiciones":[{"agua":80,"luz":8,"temp":22}]*4}

        self.alturas = datos.get("alturas", [3, 3, 3, 3])
        self.muertas = datos.get("muertas", [False, False, False, False])
        self.condiciones = datos.get("condiciones", [{"agua":80,"luz":8,"temp":22} for _ in range(4)])

        # --- Gráfico ---
        self.fig, self.ax = plt.subplots(figsize=(7, 5))
        colores = ["#4CAF50", "#CDDC39", "#00BCD4", "#FFEB3B"]
        self.barras = self.ax.bar(
            ["Planta 1", "Planta 2", "Planta 3", "Planta 4"],
            self.alturas,
            color=colores
        )
        self.ax.set_ylim(0, max(20, max(self.alturas)+2))
        self.ax.set_ylabel("Altura (cm)")
        self.ax.set_title("Crecimiento de plantas de tomate")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().place(x=40, y=30)

        # --- Panel de controles ---
        self.control_frame = tk.Frame(self.root, bg="#fff9e6")
        self.control_frame.place(x=750, y=30)

        tk.Label(
            self.control_frame,
            text="⚙️ Ajustá los factores abióticos de cada planta",
            wraplength=300,
            bg="#fff9e6",
            font=("Times New Roman", 14)
        ).grid(row=0, column=0, columnspan=2, pady=5)

        ideal_text = (
            f"Ideales:\n"
            f"💧 Agua: {VALORES_IDEALES['agua'][0]}–{VALORES_IDEALES['agua'][1]} ml ± 50ml\n"
            f"☀️ Luz: {VALORES_IDEALES['luz'][0]}–{VALORES_IDEALES['luz'][1]} h ± 2h\n"
            f"🌡️ Temp: {VALORES_IDEALES['temp'][0]}–{VALORES_IDEALES['temp'][1]} °C ± 2°C"
        )
        tk.Label(
            self.control_frame,
            text=ideal_text,
            justify="left",
            fg="green",
            bg="#fff9e6",
            font=("Times New Roman", 12)
        ).grid(row=1, column=0, pady=5)

        crecimiento_text = (
            "🌿 Crecimiento estimado:\n"
            "+6 cm → Condiciones ideales\n"
            "+3 cm → Dentro de tolerancia\n"
            "+1 cm → Cercanas a tolerancia"
        )
        tk.Label(
            self.control_frame,
            text=crecimiento_text,
            justify="left",
            bg="#fff9e6",
            font=("Times New Roman", 12),
            relief="solid",
            bd=1,
            padx=5,
            pady=5
        ).grid(row=1, column=1, padx=10, pady=5)

        # --- Entradas para cada planta ---
        self.entradas = []
        for i in range(4):
            frame = tk.LabelFrame(self.control_frame, text=f"Planta {i+1}", bg="#fff9e6",
                                  font=("Times New Roman", 12, "bold"))
            frame.grid(row=i+2, column=0, columnspan=2, pady=5, sticky="ew")

            agua = tk.Entry(frame, width=6, font=("Times New Roman", 12))
            luz = tk.Entry(frame, width=6, font=("Times New Roman", 12))
            temp = tk.Entry(frame, width=6, font=("Times New Roman", 12))
            agua.insert(0, str(self.condiciones[i]["agua"]))
            luz.insert(0, str(self.condiciones[i]["luz"]))
            temp.insert(0, str(self.condiciones[i]["temp"]))

            tk.Label(frame, text="Agua (ml):", bg="#fff9e6", font=("Times New Roman", 12)).grid(row=0, column=0, padx=2)
            agua.grid(row=0, column=1, padx=2)
            tk.Label(frame, text="Luz (h):", bg="#fff9e6", font=("Times New Roman", 12)).grid(row=0, column=2, padx=2)
            luz.grid(row=0, column=3, padx=2)
            tk.Label(frame, text="Temp (°C):", bg="#fff9e6", font=("Times New Roman", 12)).grid(row=0, column=4, padx=2)
            temp.grid(row=0, column=5, padx=2)

            self.entradas.append((agua, luz, temp))

            tk.Button(
                frame,
                text="Simular esta planta",
                font=("Times New Roman", 12),
                command=lambda i=i: self.simular_una(i)
            ).grid(row=1, column=0, columnspan=6, pady=4)

        # --- Botones principales ---
        tk.Button(
            self.control_frame,
            text="🔄 Simular todas",
            font=("Times New Roman", 13),
            command=self.simular_todas
        ).grid(row=10, column=0, pady=10, columnspan=2)

        tk.Button(
            self.control_frame,
            text="💾 Guardar simulación",
            font=("Times New Roman", 13),
            command=self.guardar_progreso
        ).grid(row=11, column=0, pady=5, columnspan=2)

        tk.Button(
            self.control_frame,
            text="🔁 Reiniciar simulación actual",
            font=("Times New Roman", 13),
            command=self.reiniciar_simulacion
        ).grid(row=12, column=0, pady=5, columnspan=2)

        tk.Button(
            self.root,
            text="🏠 Volver al inicio",
            font=("Times New Roman", 12),
            command=self.volver_inicio,
            bg="#f0f0f0"
        ).place(x=1180, y=10)

    # -------------------------------------------------------
    # Simulación de una planta
    # -------------------------------------------------------
    def simular_una(self, i):
        if self.muertas[i]:
            messagebox.showinfo("Aviso", f"La Planta {i+1} ya está muerta 💀.")
            return

        try:
            agua = float(self.entradas[i][0].get())
            luz = float(self.entradas[i][1].get())
            temp = float(self.entradas[i][2].get())
        except ValueError:
            messagebox.showerror("Error", "Ingresá solo números válidos.")
            return

        resultado = calcular_crecimiento(agua, luz, temp)

        if resultado == MUERTE:
            self.alturas[i] = 0
            self.muertas[i] = True
            self.condiciones[i] = {"agua":agua, "luz":luz, "temp":temp}
            messagebox.showwarning("Planta muerta 💀", f"La Planta {i+1} murió por condiciones extremas.")
        else:
            self.alturas[i] = max(0, self.alturas[i] + resultado)
            self.condiciones[i] = {"agua":agua, "luz":luz, "temp":temp}
            if self.alturas[i] <= 0:
                self.muertas[i] = True
                messagebox.showwarning("Planta muerta 💀", f"La Planta {i+1} no resistió las condiciones y murió.")
            else:
                signo = "+" if resultado >= 0 else ""
                messagebox.showinfo("Simulación", f"Planta {i+1}: cambio {signo}{resultado} cm → altura {self.alturas[i]:.1f} cm.")

        self.actualizar_grafico()

    def simular_todas(self):
        for i in range(4):
            self.simular_una(i)

    def actualizar_grafico(self):
        for rect, h in zip(self.barras, self.alturas):
            rect.set_height(h)
        self.ax.set_ylim(0, max(20, max(self.alturas) + 2))
        self.canvas.draw()

    # -------------------------------------------------------
    # Guardar progreso
    # -------------------------------------------------------
    def guardar_progreso(self):
        datos = {"alturas": self.alturas, "muertas": self.muertas, "condiciones": self.condiciones}
        guardar_simulacion(datos)
        messagebox.showinfo("Guardado exitoso", "💾 Simulación guardada correctamente.")

    # -------------------------------------------------------
    # Reiniciar simulación actual (cambia colores aleatorios)
    # -------------------------------------------------------
    def reiniciar_simulacion(self):
        self.alturas = [3,3,3,3]
        self.muertas = [False]*4
        self.condiciones = [{"agua":80,"luz":8,"temp":22} for _ in range(4)]
        
        # Cambiar colores aleatoriamente solo al reiniciar
        colores = ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(4)]
        for rect, color in zip(self.barras, colores):
            rect.set_color(color)
        
        for i, (agua, luz, temp) in enumerate(self.entradas):
            agua.delete(0, tk.END)
            agua.insert(0, "80")
            luz.delete(0, tk.END)
            luz.insert(0, "8")
            temp.delete(0, tk.END)
            temp.insert(0, "22")
        
        self.actualizar_grafico()

    # -------------------------------------------------------
    # Volver al inicio
    # -------------------------------------------------------
    def volver_inicio(self):
        self.control_frame.destroy()
        self.canvas.get_tk_widget().destroy()
        self.pantalla_inicio()

    # -------------------------------------------------------
    # Cargar guardados
    # -------------------------------------------------------
    def mostrar_guardados(self):
        simulaciones = cargar_simulaciones()
        if not simulaciones:
            messagebox.showinfo("Simulaciones guardadas", "No hay simulaciones guardadas.")
            return

        # Abrir una ventana por cada simulación guardada
        for idx, datos in enumerate(simulaciones, start=1):
            ventana = tk.Toplevel(self.root)
            ventana.title(f"Simulación guardada #{idx}")
            ventana.geometry("1300x750")
            ventana.configure(bg="#fff9e6")

            # Número de orden visible
            tk.Label(ventana, text=f"Simulación #{idx}", font=("Times New Roman", 16, "bold"), bg="#fff9e6").pack(pady=5)

            # --- Gráfico ---
            fig, ax = plt.subplots(figsize=(7,5))
            barras = ax.bar(
                ["Planta 1","Planta 2","Planta 3","Planta 4"],
                datos["alturas"],
                color=["#4CAF50", "#CDDC39", "#00BCD4", "#FFEB3B"]
            )
            ax.set_ylim(0, max(20, max(datos["alturas"])+2))
            ax.set_ylabel("Altura (cm)")
            ax.set_title("Crecimiento de plantas de tomate")
            canvas = FigureCanvasTkAgg(fig, master=ventana)
            canvas.get_tk_widget().pack(pady=20)

            # --- Datos en 4 columnas ---
            data_frame = tk.Frame(ventana, bg="#fff9e6")
            data_frame.pack(pady=10)

            for col in range(4):
                col_frame = tk.Frame(data_frame, bg="#fff9e6", relief="groove", bd=1, padx=10, pady=5)
                col_frame.grid(row=0, column=col, padx=10)

                altura = datos["alturas"][col]
                muerta = datos["muertas"][col]
                condiciones = datos.get("condiciones", [{}]*4)[col]
                estado = "💀 Muerta" if muerta else f"{altura:.1f} cm"
                agua = condiciones.get("agua", "N/A")
                luz = condiciones.get("luz", "N/A")
                temp = condiciones.get("temp", "N/A")

                tk.Label(col_frame, text=f"Planta {col+1}", font=("Times New Roman", 12, "bold"), bg="#fff9e6").pack()
                tk.Label(col_frame, text=f"Altura: {estado}", font=("Times New Roman", 12), bg="#fff9e6").pack()
                tk.Label(col_frame, text=f"Agua: {agua} ml", font=("Times New Roman", 12), bg="#fff9e6").pack()
                tk.Label(col_frame, text=f"Luz: {luz} h", font=("Times New Roman", 12), bg="#fff9e6").pack()
                tk.Label(col_frame, text=f"Temp: {temp} °C", font=("Times New Roman", 12), bg="#fff9e6").pack()


# -------------------------------------------------------
# Función para iniciar la interfaz
# -------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorPlantas(root)
    root.mainloop()