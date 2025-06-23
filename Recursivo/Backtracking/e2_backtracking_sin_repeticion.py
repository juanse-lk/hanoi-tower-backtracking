class Disco:
    def __init__(self, tamanio):
        self.tamanio = tamanio

    def puede_moverse(self):
        return True

    def mover(self):
        pass

    def deshacer_movimiento(self):
        pass


class DiscoFragil(Disco):
    def __init__(self, tamanio, max_movimientos):
        super().__init__(tamanio)
        self.max_movimientos = max_movimientos
        self.movimientos_realizados = 0

    def puede_moverse(self):
        return self.movimientos_realizados < self.max_movimientos

    def mover(self):
        self.movimientos_realizados += 1

    def deshacer_movimiento(self):
        self.movimientos_realizados -= 1


def estado_serializado(torres):
    """
    Guarda en una tupla el estado actual de las torres.

    Args:
        torres (dict): Diccionario con las torres como claves y listas de discos como valores. 

    Returns:
        tuple: Estado serializado de las torres usando un 0 como separador entre torres.
    """
    estado = []
    for nombre in ["Origen", "Auxiliar", "Destino"]:
        if nombre != "Origen":
            estado.append(0)  # Separador entre torres
        for d in torres[nombre]:
            estado.append(d.tamanio)
    return tuple(estado)


def hanoi_backtracking(torres, total_discos, movimientos, soluciones, visitados):
    """
    Resuelve el problema de la Torre de Hanoi utilizando backtracking, almacenando todas las soluciones posibles.
    
    Args:
        torres (dict): Diccionario con las torres como claves y listas de discos como valores.
        total_discos (int): Número total de discos a mover.
        movimientos (list): Lista de movimientos realizados hasta el momento, cada uno como una tupla (origen, destino, tamaño).
        soluciones (list): Lista donde se almacenan todas las soluciones encontradas, cada una como una lista de movimientos.
        visitados (set): Conjunto de estados serializados ya visitados para evitar ciclos y repeticiones.
    Returns:
        None: Las soluciones se almacenan en el parámetro 'soluciones' pasado por referencia.
    """
    estado_actual = estado_serializado(torres)

    # Verificar si el estado actual ya fue visitado
    if estado_actual in visitados:
        return
    # Marcar el estado actual como visitado
    visitados.add(estado_actual)

    # Verificar si se ha alcanzado la solución
    if len(torres["Destino"]) == total_discos:
        soluciones.append(list(movimientos))
        visitados.remove(estado_actual)
        return

    # Intentar mover discos entre torres
    for origen in torres:
        # Si la torre de origen está vacía, no hay disco para mover
        if not torres[origen]:
            continue
        # Tomar el disco superior de la torre de origen
        disco = torres[origen][-1]
        # Intentar mover el disco a cada torre de destino
        for destino in torres:
            # No mover el disco a la misma torre de origen
            if origen == destino:
                continue
            # No mover a una torre que ya tiene un disco más grande en la parte superior
            if torres[destino] and torres[destino][-1].tamanio < disco.tamanio:
                continue
            # No mover si el disco no puede moverse
            if not disco.puede_moverse():
                continue
            # Evitar mover el mismo disco en dos turnos seguidos
            if movimientos and disco.tamanio == movimientos[-1][2]:
                continue 


            # Mover disco
            torres[origen].pop()
            torres[destino].append(disco)
            disco.mover()

            # Registrar el movimiento
            movimientos.append((origen, destino, disco.tamanio))

            hanoi_backtracking(
                torres,
                total_discos,
                movimientos,
                soluciones,
                visitados
            )

            # Deshacer movimiento
            movimientos.pop()
            torres[destino].pop()
            disco.deshacer_movimiento()
            torres[origen].append(disco)
    # Desmarcar el estado actual como visitado
    visitados.remove(estado_actual)


if __name__ == "__main__":
    total_discos = 2
    torres_iniciales = {
        "Origen": [Disco(2), Disco(1)],
        "Auxiliar": [],
        "Destino": []
    }
    # --- Prueba solo backtracking

    soluciones = []
    visitados = set()

    hanoi_backtracking(torres_iniciales, total_discos, [], soluciones, visitados)
    
    print("-----------  SOLO BACKTRACKING ------------")
    print(f"\n Total de soluciones encontradas: {len(soluciones)}")


        
    soluciones.sort(key=len, reverse=True)
    # # Mostrar soluciones
    # for i, solucion in enumerate(soluciones, 1):
    #     print(f"\n🔹 Solución {i} ({len(solucion)} movimientos):")
    #     for mov in solucion:
    #         print(f"{mov[0]} → {mov[1]} | Disco {mov[2]}")
    # Mostrar cantidad de movimientos de cada solución
    print("\n🔍 Resumen de soluciones:")
    for i, solucion in enumerate(soluciones, 1):
        print(f"🔹 Solución {i}: {len(solucion)} movimientos")

    print(f"\n Total de soluciones encontradas: {len(soluciones)}")