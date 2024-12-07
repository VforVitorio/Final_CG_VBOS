import math
# Nuevas importaciones
import pybullet as p
import numpy as np


class PendulumPhysics():
    """
    Clase para simular la física de un péndulo de Newton usando PyBullet.

    Métodos principales:
        - __init__: Configura el entorno de la simulación, crea las bolas y restricciones.
        - prepare_ball_launch: Prepara la primera bola para ser impulsada.
        - step: Simula un paso de física y ajusta las posiciones y velocidades.
        - get_ball_positions: Obtiene las posiciones actuales de las bolas.
        - cleanup: Finaliza la simulación y desconecta PyBullet.
    """

    def __init__(self):
        """
        Constructor que inicializa la simulación, crea las bolas del péndulo
        y establece las restricciones necesarias.

        Configuraciones:
            - Gravedad: (0, -9.81, 0)
            - Paso de tiempo: 1/480 para mayor precisión.
            - Número de bolas: 5.
            - Altura inicial de las bolas: 1.7.

        Componentes creados:
            - Bolas con diferentes propiedades de fricción y elasticidad.
            - Restricciones tipo punto a punto para simular los hilos del péndulo.
        """
        self.physicsClient = p.connect(p.DIRECT)

        # Configuración precisa de física
        p.setGravity(0, -9.81, 0)
        p.setRealTimeSimulation(0)
        p.setTimeStep(1.0 / 480.0)  # TimeStep más preciso para evitar errores

        self.balls = []
        self.constraints = []
        self.initial_positions = []

        spacing = 1.0
        start_x = -2.0
        ball_radius = 0.5
        initial_height = 1.7  # Altura del punto de anclaje
        num_balls = 5

        # Crear bolas y configurarlas
        for i in range(num_balls):
            x = start_x + i * spacing
            position = [x, initial_height - ball_radius, 0]
            self.initial_positions.append(position)

            # Crear la bola
            ball_collision = p.createCollisionShape(
                p.GEOM_SPHERE, radius=ball_radius)
            ball = p.createMultiBody(
                baseMass=1.0,  # Masa ajustada
                baseCollisionShapeIndex=ball_collision,
                basePosition=position
            )

            # Ajustar las propiedades dinámicas según la posición de la bola
            if 1 <= i <= 3:  # Bolas centrales
                p.changeDynamics(
                    ball, -1,
                    restitution=0.95,  # Elasticidad máxima
                    lateralFriction=0.03,  # Fricción mínima
                    spinningFriction=0.02,
                    rollingFriction=0.02,
                    linearDamping=0.05,
                    angularDamping=0.05
                )
            else:  # Bolas en los extremos
                p.changeDynamics(
                    ball, -1,
                    restitution=0.8,  # Elasticidad menor
                    lateralFriction=0.01,
                    spinningFriction=0.01,
                    rollingFriction=0.01
                )

            # Crear el punto de anclaje y restricción
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
                jointAxis=[0, 0, 0],
                parentFramePosition=[0, 0, 0],
                childFramePosition=[0, -(initial_height - position[1]), 0]
            )

            self.balls.append(ball)
            self.constraints.append(constraint)

    def prepare_ball_launch(self):
        """
        Prepara la primera bola para ser impulsada.

        Acciones:
            - Ajusta la posición inicial de la bola.
            - Aplica una fuerza inicial en la dirección positiva del eje X.
        """
        if self.balls:
            initial_pos = self.initial_positions[0]
            launch_pos = [initial_pos[0] - 0.5, initial_pos[1], initial_pos[2]]

            # Configurar posición inicial de la bola
            p.resetBasePositionAndOrientation(
                self.balls[0], launch_pos, [0, 0, 0, 1])
            p.resetBaseVelocity(self.balls[0], [0, 0, 0], [0, 0, 0])

            # Aplicar fuerza inicial
            p.applyExternalForce(
                self.balls[0], -1,
                forceObj=[2.5, 0, 0],  # Reducir fuerza inicial
                posObj=launch_pos,
                flags=p.WORLD_FRAME
            )

    def step(self):
        """
        Simula un paso de la física del péndulo.

        Acciones:
            - Actualiza la simulación usando stepSimulation().
            - Ajusta la posición en Y de las bolas para mantenerlas cerca de su altura inicial.
            - Transferencia de velocidades entre bolas para simular el impacto.
        """
        p.stepSimulation()

        for i, ball in enumerate(self.balls):
            pos, _ = p.getBasePositionAndOrientation(ball)
            velocity = p.getBaseVelocity(ball)[0]

            # Mantener posición en Y cerca de su altura inicial
            if abs(pos[1] - self.initial_positions[i][1]) > 0.15:  # Permitir más libertad en Y
                corrected_pos = [pos[0], self.initial_positions[i][1], pos[2]]
                p.resetBasePositionAndOrientation(
                    ball, corrected_pos, [0, 0, 0, 1])
                p.resetBaseVelocity(
                    ball, [velocity[0], 0, velocity[2]], [0, 0, 0])

            # Transferencia de velocidad entre bolas
            if i < len(self.balls) - 1:
                v1 = velocity[0]
                v2 = p.getBaseVelocity(self.balls[i + 1])[0][0]
                if abs(v1) > 0.05 and abs(v2) < 0.01:  # Transferencia más suave
                    transfer_velocity = v1 * 0.9  # Transferencia reducida
                    p.resetBaseVelocity(
                        self.balls[i + 1], linearVelocity=[transfer_velocity, 0, 0])

    def get_ball_positions(self):
        """
        Devuelve las posiciones actuales de las bolas.

        Retorna:
            - Lista de tuplas con las posiciones (x, y, z) de las bolas.
        """
        return [p.getBasePositionAndOrientation(ball)[0] for ball in self.balls]

    def cleanup(self):
        """
        Finaliza la simulación y desconecta PyBullet.
        """
        p.disconnect()
