# main.py

from modelo_vbos import Modelo
from utilidades import *
from usuario import *
from camara import Camara
from configuracion import *
from luces import configurar_luces
# Importa cargar_textura para gestionar texturas
from texturas import cargar_textura
import math
# Inicialización de la cámara y el modelo 3D
camara = Camara()

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

# Modelos
cubo = Modelo("modelos/cubo.obj")
cono = Modelo("modelos/cono.obj")
cilindro = Modelo("modelos/cilindro.obj")
donut = Modelo("modelos/donut.obj")
esfera = Modelo("modelos/esfera.obj")
cuarto_esfera = Modelo("modelos/cuarto_esfera.obj")


# Texturas
textura_cubo = cargar_textura("texturas/madera.png")  # Textura marrón
textura_cilindro = cargar_textura("texturas/metal.png")
textura_donut = cargar_textura("texturas/metal_2.png")
textura_esfera = cargar_textura("texturas/metal_esfera.png")
textura_hilo = cargar_textura("texturas/hilo_metalico.png")


clock = pygame.time.Clock()
ejecutando = True

# Renderiza la escena


def renderizar():
    """Renderiza los elementos de la escena, incluyendo la cámara, elementos auxiliares y el modelo 3D."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glRotatef(camara.roll, 0, 0, 1)
    cam_x, cam_y, cam_z = camara.obtener_posicion()
    gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 1, 0)

    glDisable(GL_LIGHTING)
    dibujar_elementos_auxiliares(ejes=True, rejilla=True)
    glEnable(GL_LIGHTING)

    # Dibuja el cubo
    # Dibuja la base (6.0x2.0x0.2)
    cubo.dibujar(textura_id=textura_cubo, t_x=0.0, t_y=0.2, t_z=0.0,  # t_y=0.1 para ponerlo sobre la rejilla
                 angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                 sx=10.0, sy=0.4, sz=4.0)  # Dimensiones según especificaciones

    # Dibuja los 4 cilindros en las esquinas
    # Cilindros ajustados en altura y centrados en las rejillas

    # Cilindro esquina frontal derecha
    cilindro.dibujar(textura_id=textura_cilindro, t_x=4.5, t_y=1.8, t_z=1.5,
                     angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                     sx=0.25, sy=3.5, sz=0.25)
    # Cilindro esquina frontal izquierda
    cilindro.dibujar(textura_id=textura_cilindro, t_x=-4.5, t_y=1.8, t_z=1.5,
                     angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                     sx=0.25, sy=3.5, sz=0.25)
    # Cilindro esquina trasera derecha
    cilindro.dibujar(textura_id=textura_cilindro, t_x=4.5, t_y=1.8, t_z=-1.5,
                     angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                     sx=0.25, sy=3.5, sz=0.25)
    # Cilindro esquina trasera izquierda
    cilindro.dibujar(textura_id=textura_cilindro, t_x=-4.5, t_y=1.8, t_z=-1.5,
                     angulo=0.0, eje_x=0.0, eje_y=0.0, eje_z=0.0,
                     sx=0.25, sy=3.5, sz=0.25)

    # Cilindros horizontales que unen cilindros traseros y delanteros respectivamente

    # Rotarlos 90 grados en eje z
    # Ajustar escalado para que cubran la distancia entre cilindros verticales
    # Posicionarlos a altura correcta

    # Cilindro horizontal frontal (conecta los cilindros frontales)
    cilindro.dibujar(textura_id=textura_cilindro, t_x=0.0, t_y=3.5, t_z=1.5,
                     angulo=90.0, eje_x=0.0, eje_y=0.0, eje_z=1.0,
                     sx=0.25, sy=9.0, sz=0.25)  # sy=9.0 para cubrir la distancia entre -4.5 y 4.5

    # Cilindro horizontal trasero (conecta los cilindros traseros)
    cilindro.dibujar(textura_id=textura_cilindro, t_x=0.0, t_y=3.5, t_z=-1.5,
                     angulo=90.0, eje_x=0.0, eje_y=0.0, eje_z=1.0,
                     sx=0.25, sy=9.0, sz=0.25)

    # Se añaden esferas pequeñas en los puntos de union
    # Se colocan en las 8 intersecciones (4 frontales y 4 traseras)

    # Cuartos de esfera en las intersecciones de los cilindros horizontales

    # Delantero derecho
    # Delantero derecho
    # Delantero derecho (se mantiene igual)
    # Delantero derecho (se mantiene igual)
    cuarto_esfera.dibujar(textura_id=textura_cilindro, t_x=4.49, t_y=3.48, t_z=1.5,
                          angulo=-90.0, eje_x=1.0, eje_y=0.0, eje_z=0.0,
                          sx=0.3, sy=0.3, sz=0.3)

    # Delantero izquierdo (tumbado y mirando hacia fuera)
    cuarto_esfera.dibujar(textura_id=textura_cilindro, t_x=-4.49, t_y=3.48, t_z=1.5,
                          angulo=180.0, eje_x=0.0, eje_y=1.0, eje_z=1.0,  # Primero girar en Y
                          sx=0.3, sy=0.3, sz=0.3)

    # Trasero derecho (se mantiene igual)
    cuarto_esfera.dibujar(textura_id=textura_cilindro, t_x=4.49, t_y=3.48, t_z=-1.5,
                          angulo=-90.0, eje_x=1.0, eje_y=0.0, eje_z=0.0,
                          sx=0.3, sy=0.3, sz=0.3)

    # Trasero izquierdo (tumbado y mirando hacia fuera)
    cuarto_esfera.dibujar(textura_id=textura_cilindro, t_x=-4.49, t_y=3.48, t_z=-1.5,
                          angulo=180.0, eje_x=0.0, eje_y=1.0, eje_z=1.0,  # Primero girar en Y
                          sx=0.3, sy=0.3, sz=0.3)

    # ===========
    # Dibujo de las anillas
    # ===========
    # 5 donuts en el cilindro frontal
    # 5 donuts en el cilindro frontal
    # Ajustamos las posiciones para que estén más juntas
    # Posiciones más cercanas entre sí
    # Ajustamos las posiciones para separar un poco más las bolas
    posiciones_x = [-2, -1, 0.0, 1, 2]

    for x in posiciones_x:
        # Donuts frontales
        donut.dibujar(textura_id=textura_donut,
                      t_x=x, t_y=3.5, t_z=1.5,
                      angulo=90.0, eje_x=0.0, eje_y=0.0, eje_z=1.0,
                      sx=0.22, sy=0.22, sz=0.12)  # Volvemos al tamaño original
        # El resto se mantiene igual usando las nuevas posiciones
        dibujar_hilo(cilindro, x, 3.5, 1.5, (x, 2.0, 0.0), es_trasero=False)
        dibujar_esfera_union(cilindro, x, 2.0, 0.0, es_trasero=False)
        dibujar_bola_pendulo(esfera, x, 2.0, 0.0, es_trasero=False)
    # Repetimos para los traseros
    for x in posiciones_x:
        donut.dibujar(textura_id=textura_donut,
                      t_x=x, t_y=3.5, t_z=-1.5,
                      angulo=-90.0, eje_x=0.0, eje_y=0.0, eje_z=1.0,
                      sx=0.22, sy=0.22, sz=0.12)
        dibujar_hilo(esfera, x, 3.5, -1.5, (x, 2.0, 0.0), es_trasero=True)
        dibujar_esfera_union(esfera, x, 2.0, 0.0, es_trasero=True)
        dibujar_bola_pendulo(esfera, x, 2.0, 0.0, es_trasero=True)


def dibujar_hilo(modelo, t_x, t_y, t_z, punto_destino, es_trasero=False):
    """Dibuja un hilo desde un punto origen a un punto destino"""
    # Calculamos la longitud
    dx = punto_destino[0] - t_x
    dy = punto_destino[1] - (t_y - 0.2)
    dz = punto_destino[2] - t_z
    longitud = math.sqrt(dx*dx + dy*dy + dz*dz) * 2.5

    # Ajustamos el punto medio para que el extremo coincida con el donut
    medio_x = t_x + dx/4  # Desplazamos 1/4 de la distancia en X
    medio_y = (t_y - 0.2) + dy/2  # Desplazamos 1/4 de la distancia en Y
    medio_z = t_z + dz/2  # Desplazamos 1/4 de la distancia en Z

    # Ángulo de inclinación
    angulo = 40.0 if not es_trasero else -40.0

    modelo.dibujar(
        textura_id=textura_hilo,
        t_x=medio_x,
        t_y=medio_y,
        t_z=medio_z,
        angulo=angulo,
        eje_x=1.0, eje_y=0.0, eje_z=0.0,
        sx=0.01,
        sy=longitud/2,  # Mantenemos la mitad de la longitud
        sz=0.01
    )


def dibujar_esfera_union(modelo, x, y, z, es_trasero=False):
    """Dibuja una media esfera en el extremo de los hilos"""
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


def dibujar_bola_pendulo(modelo, x, y, z, es_trasero=False):
    """Dibuja una bola grande del péndulo de Newton"""
    esfera.dibujar(
        textura_id=textura_esfera,
        t_x=x,
        t_y=y - 0.8,  # Bajamos respecto a la posición de la esfera_union
        t_z=z,
        angulo=0.0,   # Sin rotación, es una esfera completa
        eje_x=1.0,
        eje_y=0.0,
        eje_z=0.0,
        sx=1.0,      # Escala grande para la bola
        sy=1.0,      # Mantener proporciones esféricas
        sz=1.0      # Mantener proporciones esféricas
    )


# Bucle principal de la aplicación
while ejecutando:
    delta_time = clock.tick(FPS) / MILLISECONDS_PER_SECOND
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.MOUSEWHEEL):
            procesar_eventos_raton(evento, camara)

    consultar_estado_teclado(camara, delta_time)
    camara.actualizar_camara()
    configurar_luces()
    renderizar()
    pygame.display.flip()

pygame.quit()
