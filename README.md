# Péndulo de Newton 3D

Este proyecto implementa una **simulación interactiva en 3D** del péndulo de Newton utilizando **Python**, **OpenGL**, y **PyBullet** para la física.

## Descripción

- 🔹 **Simulación 3D interactiva del péndulo de Newton**.
- 🔹 **Sistema de física realista** usando PyBullet y Trimesh.
- 🔹 **Renderizado 3D** con OpenGL y texturas.
- 🔹 **Cámara interactiva** con controles de rotación y zoom.
- 🔹 **Iluminación dinámica** con múltiples fuentes de luz.

---

## 🛠️ **Características principales**

| Característica           | Detalle                                                                 |
| ------------------------ | ----------------------------------------------------------------------- |
| **Modelado 3D**          | Texturas y VBOs para mejorar rendimiento                                |
| **Física realista**      | Sistema de colisiones y animaciones suaves                              |
| **Cámara interactiva**   | Control con ratón y teclado                                             |
| **Iluminación dinámica** | Configurable con dos luces, siguiendo el modelo de iluminación de Phong |

---

## 🎮 **Controles**

| Acción               | Control                      |
| -------------------- | ---------------------------- |
| **Rotar cámara**     | Ratón (botón izquierdo)      |
| **Zoom**             | Rueda del ratón              |
| **Lanzar bola**      | `Espacio`                    |
| **Reiniciar**        | `R`                          |
| **Control de luces** | `1`, `2`, `3`                |
| **Mover cámara**     | `W`, `A`, `S`, `D`, `Q`, `E` |

---

## 📂 **Estructura del proyecto**

| Archivo           | Descripción                                            |
| ----------------- | ------------------------------------------------------ |
| `main_pendulo.py` | Programa con física y lógica del péndulo               |
| `modelo_vbos.py`  | Programa principal con renderizado del modelo con VBOs |
| `camara.py`       | Configuración de cámara interactiva                    |
| `luces.py`        | Configuración de iluminación                           |
| `texturas.py`     | Carga y gestión de texturas                            |
| `utilidades.py`   | Funciones auxiliares                                   |
| `usuario.py`      | Manejo de entrada de usuario                           |

**Nota:** Los modelos 3D y texturas se encuentran en las carpetas `modelos` y `texturas` respectivamente.

---

## 📦 **Requisitos**

El proyecto utiliza las siguientes librerías:

- `numpy` para cálculos matemáticos
- `pygame` para gestión de ventanas y eventos
- `PyOpenGL` para renderizado 3D
- `pybullet` para simulación física

---

## 🚀 **Instalación y Ejecución**

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/pendulo-newton-3d.git
   ```
2. **Instala las dependencias:**

```bash
pip install -r requirements.txt
```

3. **Ejecuta el proyecto:**

   - **Simulación con física:**

     ```bash
     python main_pendulo.py
     ```

   - **Renderizado estático:**

   ```bash
   python main.py
   ```
