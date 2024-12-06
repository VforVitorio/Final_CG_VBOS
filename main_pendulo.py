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
# Nuevas importaciones
import pybullet as p
import pybullet_data
import trimesh
import numpy as np
# Inicialización de la cámara y el modelo 3D
camara = Camara()
POSICIONES_DONUTS_X = [-2, -1, 0.0, 1, 2]
POSICIONES_DONUTS_Z = [-1.5, 1.5]


class PendulumPhysics():
    def __init__(self):
        self.physicsClient = p.connect(p.DIRECT)

        # Configuración precisa de física
        p.setGravity(0, -9.81, 0)
        p.setRealTimeSimulation(0)
        p.setTimeStep(1.0 / 240.0)

        self.balls = []
        self.constraints = []
        self.initial_positions = []

        spacing = 1.0
        start_x = -2.0
        ball_radius = 0.5
        initial_height = 1.7
        num_balls = 5

        # Crear bolas y configurarlas
        for i in range(num_balls):
            x = start_x + i * spacing
            position = [x, ball_radius, 0]
            self.initial_positions.append(position)

            # Crear la bola
            ball_collision = p.createCollisionShape(
                p.GEOM_SPHERE, radius=ball_radius)
            ball = p.createMultiBody(
                baseMass=0.5,
                baseCollisionShapeIndex=ball_collision,
                basePosition=position
            )
            p.changeDynamics(
                ball, -1,
                restitution=1.0,  # Colisiones elásticas ideales
                lateralFriction=0.0,  # Sin fricción lateral
                spinningFriction=0.0,
                rollingFriction=0.0
            )

            # Crear el punto de anclaje y constraint
            anchor = p.createMultiBody(
                baseMass=0,
                baseCollisionShapeIndex=p.createCollisionShape(
                    p.GEOM_SPHERE, radius=0.01),
                basePosition=[x, initial_height, 0]
            )
            constraint = p.createConstraint(
                anchor, -1,
                ball, -1,
                p.JOINT_POINT2POINT,
                [0, 0, 0],
                [0, ball_radius, 0],
                [0, -(initial_height - ball_radius), 0]
            )
            self.balls.append(ball)
            self.constraints.append(constraint)

    def prepare_ball_launch(self):
        """Impulsa la primera bola"""
        if self.balls:
            # Posición inicial ligeramente desplazada
            initial_pos = self.initial_positions[0]
            launch_pos = [initial_pos[0] - 0.2, initial_pos[1], initial_pos[2]]

            # Configurar la bola inicial para el impacto
            p.resetBasePositionAndOrientation(
                self.balls[0], launch_pos, [0, 0, 0, 1])
            p.resetBaseVelocity(self.balls[0], [0, 0, 0], [0, 0, 0])

            # Aplicar fuerza para el impulso inicial
            p.applyExternalForce(
                self.balls[0], -1,
                forceObj=[5.0, 0, 0],  # Fuerza en dirección positiva X
                posObj=launch_pos,
                flags=p.WORLD_FRAME
            )

    def step(self):
        """Simula la física y asegura colisiones realistas"""
        p.stepSimulation()

        # Ajustar velocidades tras colisiones
        velocities = [p.getBaseVelocity(ball)[0] for ball in self.balls]
        for i in range(len(velocities) - 1):
            v1 = np.linalg.norm(velocities[i])
            v2 = np.linalg.norm(velocities[i + 1])

            # Transferir velocidad si la bola está casi inmóvil
            if v1 > 0.1 and v2 < 0.1:
                p.resetBaseVelocity(
                    self.balls[i + 1], linearVelocity=velocities[i])

    def get_ball_positions(self):
        return [p.getBasePositionAndOrientation(ball)[0] for ball in self.balls]

    def cleanup(self):
        p.disconnect()

# Inicialización de la escena


def inicializar_escena():
    """Inicializa la ventana gráfica con Pygame y configura los ajustes de OpenGL para la escena 3D.

    Returns:
        screen: Objeto de la ventana gráfica creada por Pygame.
    """
    pygame.init()
    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption('VEGA SOBRAL VICTOR')

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


def renderizar(ball_positions=None):
    """Renderiza la escena completa con las bolas del péndulo"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glRotatef(camara.roll, 0, 0, 1)
    cam_x, cam_y, cam_z = camara.obtener_posicion()
    gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 1, 0)

    glDisable(GL_LIGHTING)
    dibujar_elementos_auxiliares(ejes=True, rejilla=True)
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
    """Dibuja los cilindros verticales y horizontales con sus uniones"""
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
    """Dibuja un hilo diagonal desde un punto origen a un punto destino"""
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
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                physics.prepare_ball_launch()

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
