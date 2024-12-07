# main.py

from modelo_vbos import Modelo
from utilidades import *
from usuario import *
from camara import Camara
from configuracion import *
from luces import configurar_luces
# Importa cargar_textura para gestionar texturas
from texturas import cargar_textura
from clase_fisicas_pendulo import PendulumPhysics
import math

# Inicialización de la cámara y el modelo 3D
camara = Camara()
POSICIONES_DONUTS_X = [-2, -1, 0.0, 1, 2]
POSICIONES_DONUTS_Z = [-1.5, 1.5]


# Inicialización de la escena


def inicializar_escena():
    """Inicializa la ventana gráfica con Pygame y configura los ajustes de OpenGL para la escena 3D.

    Returns:
        screen: Objeto de la ventana gráfica creada por Pygame.
    """
    pygame.init()
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('GRUPO 06')

    # Configuración de OpenGL
    glClearColor(0, 0, 0, 1)  # Fondo negro
    glEnable(GL_DEPTH_TEST)  # Activa el z-buffer para la profundidad
    glShadeModel(GL_SMOOTH)  # Activa el sombreado suave
    glMatrixMode(GL_PROJECTION)  # Selecciona la matriz de proyección
    # Configura la proyección en perspectiva
    gluPerspective(FOV, SCREEN_ASPECT_RATIO, NEAR_PLANE, FAR_PLANE)
    glMatrixMode(GL_MODELVIEW)  # Selecciona la matriz de modelo-vista
    glLoadIdentity()  # Restablece la matriz a la identidad
    # Inicializa la iluminación
    configurar_luces()
    # Activa la luz 1 (GL_LIGHT0)
    glEnable(GL_LIGHT0)
    # Activa la luz 2
    glEnable(GL_LIGHT1)

    # Activa la iluminación en general
    glEnable(GL_LIGHTING)
    return screen


# Configuración e inicialización del entorno
screen = inicializar_escena()  # Crea la ventana y configura el contexto OpenGL
physics = PendulumPhysics()
# Modelos

# Creación de la instancia de cada modelo con su obj correspondiente


cubo = Modelo("modelos/cubo.obj")
cono = Modelo("modelos/cono.obj")
cilindro = Modelo("modelos/cilindro.obj")
donut = Modelo("modelos/donut.obj")
esfera = Modelo("modelos/esfera.obj")  # Definir esfera correctamente
cuarto_esfera = Modelo("modelos/cuarto_esfera.obj")


# Texturas
# Se cargan las texturas a partir de su png correspondiente
textura_cubo = cargar_textura("texturas/madera.png")
textura_cilindro = cargar_textura("texturas/metal.png")
textura_donut = cargar_textura("texturas/metal_2.png")
textura_esfera = cargar_textura("texturas/metal_esfera.png")
textura_hilo = cargar_textura("texturas/hilo_metalico.png")

# Se inicializa el reloj de pygame
clock = pygame.time.Clock()
ejecutando = True

# Renderiza la escena


def renderizar(ball_positions=None):
    """
    Renderiza la escena completa con las bolas del péndulo de Newton.

    Parámetros:
        - ball_positions: Lista de posiciones de las bolas del péndulo. Cada posición es una tupla (x, y, z).

    Acciones:
        - Configura la cámara.
        - Dibuja la base cúbica.
        - Dibuja la estructura del péndulo (cilindros y uniones).
        - Dibuja las bolas del péndulo y sus hilos.
    """

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glRotatef(camara.roll, 0, 0, 1)
    cam_x, cam_y, cam_z = camara.obtener_posicion()
    gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 1, 0)

    glDisable(GL_LIGHTING)
    # dibujar_elementos_auxiliares(ejes=True, rejilla=True)
    glEnable(GL_LIGHTING)

    # Dibuja el cubo (base)
    cubo.dibujar(textura_id=textura_cubo, t_x=0.0, t_y=0.2, t_z=0.0,
                 angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                 sx=10.0, sy=0.4, sz=4.0)

    # Dibuja la estructura (cilindros y uniones)
    dibujar_estructura()

    # Dibuja las bolas del péndulo y sus conexiones
    if ball_positions:
        for i, pos in enumerate(ball_positions):

            # Dibujar hilos diagonales
            dibujar_hilo(cilindro, pos[0], 3.5, 0, pos, False)

            # Dibujar la esfera principal (abajo)
            esfera.dibujar(
                textura_id=textura_esfera,
                t_x=pos[0],
                t_y=pos[1],
                t_z=pos[2],
                angulo=0.0,
                eje_x=1.0,
                eje_y=0.0,
                eje_z=0.0,
                sx=1.0,
                sy=1.0,
                sz=1.0
            )


def dibujar_estructura():
    """
    Dibuja la estructura del péndulo, que consiste en:
        - Cilindros verticales en las esquinas.
        - Cilindros horizontales que conectan las columnas.
        - Esferas en las uniones.
        - Donuts decorativos en los cilindros horizontales.
    """
    # Cilindros verticales en las esquinas
    for x in [-4.5, 4.5]:
        for z in [-1.5, 1.5]:
            # Dibuja los cilindros verticales
            cilindro.dibujar(textura_id=textura_cilindro, t_x=x, t_y=1.8, t_z=z,
                             angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                             sx=0.25, sy=3.5, sz=0.25)

    # Cilindros horizontales
    for z in [-1.5, 1.5]:
        cilindro.dibujar(textura_id=textura_cilindro, t_x=0.0, t_y=3.5, t_z=z,
                         angulo=90.0, eje_x=0.0, eje_y=0.0, eje_z=1.0,
                         sx=0.25, sy=9.0, sz=0.25)

    # Esferas de unión en las esquinas
    for x in [-4.49, 4.49]:
        for z in [-1.5, 1.5]:
            if x > 0:  # Derecha
                cuarto_esfera.dibujar(textura_id=textura_cilindro, t_x=x, t_y=3.48, t_z=z,
                                      angulo=-90.0, eje_x=1.0, eje_y=0.0, eje_z=0.0,
                                      sx=0.3, sy=0.3, sz=0.3)
            else:  # Izquierda
                cuarto_esfera.dibujar(textura_id=textura_cilindro, t_x=x, t_y=3.48, t_z=z,
                                      angulo=180.0, eje_x=0.0, eje_y=1.0, eje_z=1.0,
                                      sx=0.3, sy=0.3, sz=0.3)
    for x in POSICIONES_DONUTS_X:
        for z in POSICIONES_DONUTS_Z:
            donut.dibujar(
                textura_id=textura_donut,
                t_x=x,
                t_y=3.5,
                t_z=z,
                angulo=90.0 if z > 0 else -90.0,  # Ajusta el ángulo según la posición
                eje_x=0.0,
                eje_y=0.0,
                eje_z=1.0,
                sx=0.22,
                sy=0.22,
                sz=0.12
            )


def dibujar_hilo(modelo, t_x, t_y, t_z, punto_destino, es_trasero=False):
    """
    Dibuja un hilo diagonal entre un punto origen y un punto destino utilizando un modelo dado, con una textura específica y una orientación basada en la dirección del hilo.

    Parámetros:
    - modelo: Objeto que se usará para dibujar el hilo (generalmente un cilindro).
    - t_x, t_y, t_z (float): Coordenadas del punto de origen del hilo.
    - punto_destino (tuple[float, float, float]): Coordenadas del punto final del hilo.
    - es_trasero (bool): Indica si el hilo es parte trasera del modelo. No se usa actualmente.

    El hilo se dibuja con una textura predeterminada, ajustando su longitud y orientación con base en las posiciones de origen y destino.
    """
    dx = punto_destino[0] - t_x
    dy = punto_destino[1] - t_y  # Ya no restamos offset
    dz = punto_destino[2] - t_z
    longitud = math.sqrt(dx*dx + dy*dy + dz*dz)

    # Calculamos el ángulo de rotación basado en la dirección del hilo
    angulo_y = math.degrees(math.atan2(dx, dy))  # Cambia el cálculo del ángulo
    # Nuevo cálculo para orientación
    angulo_z = math.degrees(math.atan2(dz, math.sqrt(dx*dx + dy*dy)))

    # Punto medio para la posición del hilo
    medio_x = (t_x + punto_destino[0]) / 2
    medio_y = (t_y + punto_destino[1]) / 2
    medio_z = (t_z + punto_destino[2]) / 2

    glPushMatrix()
    glTranslatef(medio_x, medio_y, medio_z)
    glRotatef(angulo_y, 0, 0, 1)
    glRotatef(angulo_z, 0, 1, 0)

    modelo.dibujar(
        textura_id=textura_hilo,
        t_x=0, t_y=0, t_z=0,
        angulo=0.0,
        eje_x=1.0, eje_y=0.0, eje_z=0.0,
        sx=0.01,
        sy=longitud/2,
        sz=0.01
    )
    glPopMatrix()


def dibujar_esfera_union(modelo, x, y, z, es_trasero=False):
    """
    Dibuja una media esfera en el extremo de un hilo, simulando una unión o conexión con un modelo de textura específica.

    Parámetros:
    - modelo: Objeto que se usará para dibujar la media esfera.
    - x, y, z (float): Coordenadas donde se ubicará la media esfera.
    - es_trasero (bool): Indica si la esfera está ubicada en la parte trasera del modelo. No se usa actualmente.

    La media esfera se orienta con la parte plana mirando hacia arriba y se ajusta para alinear correctamente con el hilo al que está unida.
    """

    esfera.dibujar(
        textura_id=textura_donut,
        t_x=x,
        t_y=y - 0.3,  # Ajustamos altura para que coincida con los hilos
        t_z=z,
        angulo=180.0,  # Rotación para que la parte plana mire hacia arriba
        eje_x=1.0,
        eje_y=0.0,
        eje_z=0.0,
        sx=0.08,      # Ancho de la media esfera
        # Altura de la media esfera (más pequeña para que parezca partida)
        sy=0.04,
        sz=0.08       # Profundidad igual al ancho para mantener proporción
    )


# Bucle principal de la aplicación
while ejecutando:
    delta_time = clock.tick(FPS) / MILLISECONDS_PER_SECOND
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.MOUSEWHEEL):
            procesar_eventos_raton(evento, camara)
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                physics.prepare_ball_launch()
            elif evento.key == pygame.K_r:
                physics.cleanup()
                physics = PendulumPhysics()

    consultar_estado_teclado(camara, delta_time)
    physics.step()
    ball_positions = physics.get_ball_positions()

    renderizar(ball_positions)
    camara.actualizar_camara()
    configurar_luces()

    # Solo un flip al final
    pygame.display.flip()

physics.cleanup()
pygame.quit()
