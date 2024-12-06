# configuracion.py
'''
Es este fichero se definen las constantes que establecen la configuración general de la aplicación
'''

# Definición de colores
COLOR_ROJO = (1.0, 0.0, 0.0)     # Color rojo primario
COLOR_VERDE = (0.0, 1.0, 0.0)     # Color verde primario
COLOR_AZUL = (0.0, 0.0, 1.0)     # Color azul primario
COLOR_AMARILLO = (1.0, 1.0, 0.0)     # Color amarillo
COLOR_NARANJA = (1.0, 0.5, 0.0)     # Color naranja
COLOR_BLANCO = (1.0, 1.0, 1.0)     # Color blanco
COLOR_NEGRO = (0.0, 0.0, 0.0)     # Color negro

# Configuración de la ventana gráfica
SCREEN_WIDTH = 1280                           # Anchura de la ventana gráfica
SCREEN_HEIGHT = 720                           # Altura de la ventana gráfica
# Relación de aspecto de la ventana gráfica
SCREEN_ASPECT_RATIO = SCREEN_WIDTH / SCREEN_HEIGHT

# Configuración de la proyección
# (Field Of View) Campo o ángulo de vision desde el centro de la cámara.
FOV = 45
NEAR_PLANE = 0.1   # Distancia del plano más cercano a la cámara.
FAR_PLANE = 50    # Distancia del plano más lejano a la cámara.

# Configuración del bucle de renderizado
FPS = 60
MILLISECONDS_PER_SECOND = 1000.0    # Número de milisegundos en un segundo.

# Configuración de la interacción del usuario
BOTON_IZQUIERDO_RATON = 1     # ID del botón izquierdo del ratón.
# Sensibilidad a la rotación cuando se utiliza el ratón.
SENSIBILIDAD_ROTACION = 0.2
SENSIBILIDAD_ZOOM = 0.3   # Sensibilidad al zoom cuando se usa el ratón.
# Distancia máxima de la cámara al origen cuando se hace zoom.
RADIO_MAX = 15.0
# Distancia mínima de la cámara al origen cuando se hace zoom.
RADIO_MIN = 1.0
# Ajustar a 1 o -1 para invertir el sentido de los controles cuando se rota la escena.
INVERTIR_CONTROLES = -1
# Velocidad de rotación cuando se usa el teclado, en grados por segundo.
VELOCIDAD_ROTACION = 135
# Velocidad de zoom cuando se usa el teclado, en unidades por segundo.
VELOCIDAD_ZOOM = 10

# Configuración de los ejes
# Longitud de los segmentos de recta que representan los ejes
LONGITUD_EJE = 4
EJE_X_MIN = -LONGITUD_EJE    # Coordenada mínima del eje X
EJE_X_MAX = LONGITUD_EJE    # Coordenada máxima del eje X
EJE_Y_MIN = -LONGITUD_EJE    # Coordenada mínima del eje Y
EJE_Y_MAX = LONGITUD_EJE    # Coordenada máxima del eje Y
EJE_Z_MIN = -LONGITUD_EJE    # Coordenada mínima del eje Z
EJE_Z_MAX = LONGITUD_EJE    # Coordenada máxima del eje Z
COLOR_EJE_X = COLOR_ROJO      # Color del eje X
COLOR_EJE_Y = COLOR_VERDE     # Color del eje Y
COLOR_EJE_Z = COLOR_AZUL      # Color del eje Z
EJE_FLECHA_BASE = 0.1             # Radio de la base de la flecha
EJE_FLECHA_PUNTA = 0.0             # Radio de la punta de la flecha
EJE_FLECHA_LONGITUD = 0.5             # Longitud de la flecha
# Número de subdivisiones en el eje Z de la flecha
EJE_FLECHA_REBANADAS = 10
EJE_FLECHA_PILAS = 10              # Nümero de subdivisiones en el eje Y de la flecha

# Configuración de la rejilla
REJILLA_COLOR = COLOR_BLANCO    # Color de las líneas de la rejilla
# Tamaño de la rejilla en cada eje (positivo y negativo)
REJILLA_TAMANO = 5
REJILLA_PASO = 1               # Tamaño de cada celda de la rejilla
