# 🌿 Simulador de Crecimiento de Plantas 

El Simulador de Crecimiento de Plantas es una aplicación interactiva desarrollada en Python con fines educativos. Permite observar cómo distintas condiciones ambientales —agua, luz y temperatura— afectan el crecimiento de plantas de tomate, representadas gráficamente mediante barras.

El programa busca favorecer la comprensión de los factores abióticos que influyen en los seres vivos, promoviendo la experimentación y la observación de resultados de manera visual e intuitiva. Desde el punto de vista didáctico, esta herramienta puede integrarse en clases de Biología para explorar las relaciones entre los seres vivos y el ambiente, favorecer el razonamiento hipotético-deductivo al anticipar resultados de una simulación y potenciar la autonomía y la curiosidad científica del estudiante mediante la manipulación de variables.

Como docente de Biología, el objetivo de esta aplicación fue generar un recurso interactivo simple pero significativo que permitiera conectar conceptos teóricos con una experiencia simulada. A través de la interfaz, el estudiante puede visualizar cómo pequeñas variaciones en el agua, la luz o la temperatura afectan el crecimiento de las plantas, observando las consecuencias directas de sus decisiones. El diseño busca integrar la tecnología como medio de exploración científica, y no solo como recurso visual, favoreciendo el pensamiento crítico y la toma de decisiones basadas en evidencia.

## Instalación y ejecución

Para instalar y ejecutar el programa, primero se debe clonar o descargar el repositorio del proyecto.

Clonar o descargar el repositorio del proyecto:
git clone https://github.com/t4t14n4-hub/Proyecto-final-

cd simulador-plantas

Instalar las dependencias necesarias:
pip install -r requirements.txt

### Ejecutar la aplicación:
python ejecutar.py

Se abrirá una ventana con dos opciones:

Iniciar nueva simulación: para comenzar desde cero.

Ver simulaciones guardadas: para explorar resultados previos.

Los datos se guardan automáticamente en la carpeta /data/guardado.json.

## Estructura del proyecto

📁 simulador_plantas/
│
├── ejecutar.py — Archivo principal, inicia la interfaz
├── interfaz.py — Interfaz gráfica con Tkinter + Matplotlib
├── logica.py — Cálculos y condiciones de crecimiento
├── guardado_json.py — Persistencia con archivos JSON
├── data/
│ └── guardado.json — Archivo donde se guardan las simulaciones
├── tests/
│ └── test_logica.py — Pruebas unitarias con pytest
├── requirements.txt — Dependencias del proyecto
└── README.md — Documento descriptivo

## Dependencias

El proyecto utiliza las siguientes librerías, indicadas en el archivo requirements.txt:

python-dateutil==2.8.2

matplotlib==3.8.0

pytest==7.4.0

Explicación:

python-dateutil: manejo flexible de fechas (utilizado indirectamente por Matplotlib).

matplotlib: visualización de los resultados de crecimiento de las plantas.

pytest: ejecución de pruebas unitarias para validar la lógica del programa.

(Tkinter y JSON son módulos estándar de la instalación de Python y no figuran en requirements.txt).

## Justificación de librerías utilizadas

Tkinter: permite crear una interfaz gráfica de escritorio intuitiva y accesible.

Matplotlib: facilita la visualización gráfica del crecimiento de las plantas en forma de barras.

JSON (módulo nativo): usado para guardar y cargar las simulaciones, garantizando persistencia de datos sin necesidad de bases de datos complejas.

Pytest: utilizado para realizar pruebas unitarias simples sobre las funciones lógicas.

El uso combinado de estas librerías permite integrar interfaz, persistencia y visualización, cumpliendo con los principios de modularidad y separación de responsabilidades.

## Resultados de las pruebas unitarias

Se ejecutaron 5 pruebas con `pytest` para verificar el funcionamiento de la lógica de crecimiento y muerte de las plantas.
 
python -m pytest -v

Resultados obtenidos: 
tests/test_logica.py::test_crecimiento_ideal PASSED                                                              [ 20%]
tests/test_logica.py::test_crecimiento_bajo_agua_moderado PASSED                                                 [ 40%]
tests/test_logica.py::test_muerte_por_exceso_de_agua PASSED                                                      [ 60%]
tests/test_logica.py::test_muerte_por_falta_de_luz PASSED                                                        [ 80%]
tests/test_logica.py::test_muerte_por_temperatura_extrema PASSED                                                 [100%]

5 passed in 0.11s 


## Dificultades y aprendizajes

Durante el desarrollo del proyecto se presentaron varios desafíos. Separar correctamente la lógica, la interfaz y la persistencia fue uno de los procesos más complejos y requirió reorganizar el código varias veces hasta lograr que cada módulo cumpliera una función clara y autónoma. Lograr una apariencia visual agradable con Tkinter también fue un reto, ya que demandó experimentar con estilos, tamaños y colores para que la interfaz resultara comprensible y didáctica para los estudiantes. Además, documentar y comentar cada bloque de código facilitó posteriormente el trabajo colaborativo y la corrección de errores.

Esta experiencia permitió comprender que la enseñanza de Biología puede enriquecerse notablemente mediante el uso de simulaciones, siempre que exista una planificación pedagógica que oriente la observación y la reflexión del estudiante. El desarrollo del proyecto fortaleció habilidades de pensamiento lógico, resolución de problemas y diseño modular, todas aplicables al trabajo en el aula.

Proyecto desarrollado con fines educativos por una profesora de Biología y futura profesora de informática, integrando ciencia y programación en el aula.