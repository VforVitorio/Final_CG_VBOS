# modelo.py

from OpenGL.GL import *  # Importa las funciones de OpenGL necesarias para renderizar.
from transformaciones import transformar  # Importa funciones para realizar transformaciones en 3D.
from OpenGL.arrays import vbo  # Importa la funcionalidad de Vertex Buffer Objects.
import numpy as np  # Importa NumPy para manejar eficientemente los arreglos de datos.
import ctypes  # Importa ctypes para manejar punteros y offsets.

class Modelo:
    """Clase para cargar y dibujar un modelo 3D en formato .obj, con soporte para texturas y VBOs."""

    def __init__(self, filename, draw_type=GL_TRIANGLES):
        """
        Constructor que inicializa el modelo 3D cargando la información desde un archivo .obj.

        Args:
            filename (str): Ruta al archivo .obj que contiene el modelo 3D.
            draw_type (GLenum): Tipo de dibujo OpenGL (por defecto GL_TRIANGLES).

        Atributos:
            vertices (list): Lista de coordenadas de vértices del modelo.
            normales (list): Lista de normales para cada vértice.
            coordenadas_textura (list): Lista de coordenadas de textura para cada vértice.
            triangles (list): Lista de triángulos, cada uno con vértices, normales y coordenadas de textura.
            vertex_data (np.ndarray): Arreglo numpy que contiene todos los datos de los vértices.
            vbo (vbo.VBO): Vertex Buffer Object que almacena los datos en la GPU.
            filename (str): Nombre del archivo .obj que contiene el modelo.
            draw_type (GLenum): Tipo de primitiva a utilizar para renderizar (GL_TRIANGLES por defecto).
        """
        self.vertices = []  # Almacena las coordenadas de los vértices del modelo 3D.
        self.normales = []  # Almacena las normales de los vértices para la iluminación.
        self.coordenadas_textura = []  # Almacena las coordenadas de textura para el mapeo de texturas.
        self.triangles = []  # Almacena los triángulos, definidos por índices de vértices, normales y texturas.
        self.filename = filename  # Archivo que contiene el modelo 3D.
        self.draw_type = draw_type  # Tipo de dibujo en OpenGL (por ejemplo, GL_TRIANGLES para triángulos).
        self.cargar_modelo()  # Llama al método para cargar el modelo desde el archivo .obj.
        self.preparar_vbo()  # Prepara el VBO con los datos del modelo.

    def cargar_modelo(self):
        """
        Carga el modelo desde un archivo .obj, extrayendo vértices, normales y coordenadas de textura.

        Lee el archivo línea por línea y clasifica los datos en vértices, normales y coordenadas de textura.
        Luego, asocia estos elementos en triángulos.
        """
        with open(self.filename) as file:
            for line in file:
                # Si la línea define un vértice (v x y z)
                if line.startswith("v "):
                    partes = line[2:].strip().split()
                    x, y, z = map(float, partes)
                    self.vertices.append((x, y, z))

                # Si la línea define una normal de vértice (vn x y z)
                elif line.startswith("vn "):
                    partes = line[3:].strip().split()
                    nx, ny, nz = map(float, partes)
                    self.normales.append((nx, ny, nz))

                # Si la línea define coordenadas de textura (vt u v)
                elif line.startswith("vt "):
                    partes = line[3:].strip().split()
                    u, v = map(float, partes)
                    self.coordenadas_textura.append((u, v))

                # Si la línea define una cara (f v1/t1/n1 v2/t2/n2 v3/t3/n3)
                elif line.startswith("f "):
                    partes = line[2:].strip().split()
                    indices = []
                    normal_indices = []
                    textura_indices = []
                    for parte in partes:
                        vals = parte.split('/')
                        indice_v = int(vals[0]) - 1
                        indice_t = int(vals[1]) - 1
                        indice_n = int(vals[2]) - 1
                        indices.append(indice_v)
                        textura_indices.append(indice_t)
                        normal_indices.append(indice_n)
                    if len(indices) == 3:
                        self.triangles.append((indices, normal_indices, textura_indices))

    def preparar_vbo(self):
        """
        Prepara el Vertex Buffer Object (VBO) para almacenar los datos del modelo en la GPU.

        Combina los datos de vértices, normales y coordenadas de textura en un solo arreglo numpy.
        Luego, crea un VBO con estos datos para un renderizado más eficiente.
        """
        # Prepara los datos de los vértices para el VBO
        self.vertex_data = []
        for (vert_indices, norm_indices, tex_indices) in self.triangles:
            for vi, ni, ti in zip(vert_indices, norm_indices, tex_indices):
                position = self.vertices[vi]
                normal = self.normales[ni]
                texcoord = self.coordenadas_textura[ti]
                self.vertex_data.append((*position, *normal, *texcoord))
        self.vertex_data = np.array(self.vertex_data, dtype=np.float32)

        # Crea el VBO con los datos del modelo
        self.vbo = vbo.VBO(self.vertex_data)

    def dibujar(self, textura_id, t_x=0, t_y=0, t_z=0, angulo=0, eje_x=0, eje_y=0, eje_z=0, sx=1, sy=1, sz=1):
        """
        Dibuja el modelo en la posición especificada, aplicando transformaciones y textura.

        Args:
            textura_id (int): ID de la textura cargada en OpenGL.
            t_x, t_y, t_z (float): Traslación en los ejes X, Y, Z.
            angulo (float): Ángulo de rotación en grados.
            eje_x, eje_y, eje_z (float): Ejes de rotación en X, Y, Z.
            sx, sy, sz (float): Factores de escalado en los ejes X, Y, Z.

        Aplica las transformaciones en orden: traslación, rotación, escalado.
        Luego dibuja el modelo con la textura aplicada.
        """
        # Aplica transformaciones de traslación, rotación y escalado usando la función 'transformar'.
        transformar(t_x, t_y, t_z, angulo, eje_x, eje_y, eje_z, sx, sy, sz, lambda: self._dibujar_objeto(textura_id))

    def _dibujar_objeto(self, textura_id):
        """
        Dibuja el modelo usando VBOs para un renderizado eficiente.

        Args:
            textura_id (int): ID de la textura cargada en OpenGL.

        Habilita el modo de textura, asigna la textura y dibuja el modelo
        utilizando el VBO previamente creado.
        """
        glEnable(GL_NORMALIZE)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textura_id)

        self.vbo.bind()

        # Habilita los arreglos de vértices, normales y coordenadas de textura.
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        stride = 8 * 4  # 8 floats por vértice, 4 bytes por float.

        glVertexPointer(3, GL_FLOAT, stride, ctypes.c_void_p(0))
        glNormalPointer(GL_FLOAT, stride, ctypes.c_void_p(12))  # Offset de 3 floats (12 bytes).
        glTexCoordPointer(2, GL_FLOAT, stride, ctypes.c_void_p(24))  # Offset de 6 floats (24 bytes).

        glDrawArrays(self.draw_type, 0, len(self.vertex_data))

        # Deshabilita los arreglos y desvincula el VBO.
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        self.vbo.unbind()

        glDisable(GL_TEXTURE_2D)
