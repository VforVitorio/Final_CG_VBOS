def convertir_a_cuarto_esfera(obj_entrada, obj_salida):
    vertices = []
    caras = []
    nuevos_vertices = []
    nuevas_texturas = []
    nuevas_normales = []
    nuevas_caras = []

    # Leer archivo original
    with open(obj_entrada, 'r') as f:
        for linea in f:
            if linea.startswith('v '):
                x, y, z = map(float, linea.strip().split()[1:])
                # Solo mantener vértices del cuadrante frontal derecho
                if x >= 0 and z >= 0:  # Modificado para un verdadero cuarto
                    nuevos_vertices.append(f"v {x} {y} {z}\n")
                    # Calcular coordenadas UV
                    u = x / (2.0 * 3.14159)  # Ajustado para mejor mapeo
                    v = 0.5 + (y / 3.14159)
                    nuevas_texturas.append(f"vt {u:.6f} {v:.6f}\n")
                    # Calcular normal
                    magnitud = (x*x + y*y + z*z)**0.5
                    if magnitud > 0:
                        nx, ny, nz = x/magnitud, y/magnitud, z/magnitud
                        nuevas_normales.append(
                            f"vn {nx:.6f} {ny:.6f} {nz:.6f}\n")
                vertices.append((x, y, z))
            elif linea.startswith('f '):
                caras.append(linea)

    # Filtrar vértices válidos
    vertices_validos = set()
    for i, (x, y, z) in enumerate(vertices, 1):
        if x >= 0 and z >= 0:  # Misma condición que arriba
            vertices_validos.add(i)

    # Crear caras
    for cara in caras:
        indices = [int(v.split('/')[0]) for v in cara.strip().split()[1:]]
        if all(i in vertices_validos for i in indices):
            nuevos_nums = [
                str(len([x for x in vertices_validos if x <= i])) for i in indices]
            nueva_cara = "f"
            for idx in nuevos_nums:
                nueva_cara += f" {idx}/{idx}/{idx}"
            nueva_cara += "\n"
            nuevas_caras.append(nueva_cara)

    # Guardar archivo
    with open(obj_salida, 'w') as f:
        f.write("# Cuarto de esfera con texturas y normales\n")
        f.writelines(nuevos_vertices)
        f.writelines(nuevas_texturas)
        f.writelines(nuevas_normales)
        f.writelines(nuevas_caras)


# Uso
convertir_a_cuarto_esfera('modelos/esfera.obj', 'modelos/cuarto_esfera.obj')
