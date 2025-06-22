class Disco:
    def __init__(self, tamanio):
        self.tamanio = tamanio

    def puede_moverse(self):
        return True

    def mover(self):
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


def estado_serializado(torres):
    """
    Guarda el estado actual de las torres en una tupla.
    
    Cada torre ("Origen", "Auxiliar", "Destino") se recorre en orden. 
    Se agrega un separador (0) antes de cada torre excepto la primera.
    Luego, se agregan los tamaños de los discos de cada torre.

    Args:
        torres (dict): Diccionario con las torres como claves y lista de discos como valores.

    Returns:
        tuple: Representación del estado de las torres.
    """
    estado = []
    for torre in ["Origen", "Auxiliar", "Destino"]:
        if torre != "Origen":
            estado.append(0)  # Separador entre torres
        for disco in torres[torre]:
            estado.append(disco.tamanio)
    return tuple(estado)

def copiar_torres(torres):
    """
    Crea una copia de las torres y sus discos.

    Args:
        torres (dict): Un diccionario donde las claves representan las torres y los valores son listas de objetos Disco o DiscoFragil.

    Returns:
        nuevas_torres (dict): Un nuevo diccionario con copias independientes de las listas de discos.

    Nota:
        - Si un disco es de tipo DiscoFragil, también se copia el número de movimientos realizados.
    """
    nuevas_torres = {}
    for clave, pila in torres.items(): 
        nueva_pila = []
        for disco in pila: 
            if isinstance(disco, DiscoFragil):
                nuevo_disco = DiscoFragil(disco.tamanio, disco.max_movimientos)
                nuevo_disco.movimientos_realizados = disco.movimientos_realizados
            else:
                nuevo_disco = Disco(disco.tamanio)
            nueva_pila.append(nuevo_disco)
        nuevas_torres[clave] = nueva_pila
    return nuevas_torres

def generar_movimientos_posibles(torres):
    """
    Genera una lista de movimientos posibles para los discos en las torres de Hanoi.

    Recorre todas las torres y para cada disco en la cima de una torre, verifica si puede moverse a otra torre
    siguiendo las reglas del juego (no se puede colocar un disco grande sobre uno más pequeño y solo se puede mover
    el disco superior de cada torre). Devuelve una lista de tuplas que representan los movimientos válidos.

    Args:
        torres (dict): Un diccionario donde las claves son los nombres de las torres y los valores son listas de discos,
                       siendo el último elemento de la lista el disco en la cima.

    Returns:
        list: Una lista de tuplas (origen, destino, disco) que representan los movimientos posibles.
    """
    movimientos = []
    for origen in torres:
        if not torres[origen]:
            continue
        disco = torres[origen][-1]
        if not disco.puede_moverse():
            continue
        for destino in torres:
            if origen == destino:
                continue
            if torres[destino] and torres[destino][-1].tamanio < disco.tamanio:
                continue
            movimientos.append((origen, destino, disco))
    return movimientos

def hanoi_iterativo(torres_iniciales, total_discos):
    """
    Resuelve el problema de la Torre de Hanoi de forma iterativa usando backtracking.
    Solo se puede mover un disco a la vez y no se puede colocar un disco grande sobre uno más pequeño.
    Args:
        torres_iniciales (dict): Un diccionario que representa el estado inicial de las torres. 
        Cada clave es el nombre de una torre (por ejemplo, "Origen", "Auxiliar", "Destino"),
        y cada valor es una lista de objetos disco.
        total_discos (int): El número total de discos a mover.
    Returns:
        list: Una lista de soluciones, donde cada solución es una lista de movimientos. 
        Cada movimiento se representa como una tupla (origen, destino, tamaño),
        indicando la torre de origen, la torre de destino y el tamaño del disco movido.
    """
    soluciones = []
    nodos_vivos = [] 

    estado_inicial = copiar_torres(torres_iniciales)
    nodos_vivos.append((estado_inicial, [], set([estado_serializado(estado_inicial)])))

    while nodos_vivos:
        torres, movimientos, visitados_en_rama = nodos_vivos.pop()

        if len(torres["Destino"]) == total_discos:
            soluciones.append(movimientos)
            continue

        for origen, destino, disco in generar_movimientos_posibles(torres):
            nuevas_torres = copiar_torres(torres)
            nuevas_torres[origen].pop()
            nuevas_torres[destino].append(disco)
            disco.mover()

            nuevo_movimiento = (origen, destino, disco.tamanio)
            historial_movimeintos = movimientos + [nuevo_movimiento]
            nuevo_estado = estado_serializado(nuevas_torres)

            if nuevo_estado in visitados_en_rama:
                continue

            nueva_rama_visitados = visitados_en_rama.copy()
            nueva_rama_visitados.add(nuevo_estado)
            nodos_vivos.append((nuevas_torres, historial_movimeintos, nueva_rama_visitados))

    return soluciones

# -------------------- EJECUCIÓN ------------------------
total_discos = 3
torres_iniciales = {
    "Origen": [Disco(3), Disco(2), Disco(1)],
    "Auxiliar": [],
    "Destino": []
}

soluciones = hanoi_iterativo(torres_iniciales, total_discos)

soluciones.sort(key=len, reverse=True)

for i, solucion in enumerate(soluciones, 1):
    print(f"\n🔹 Solución {i} ({len(solucion)} movimientos):")
    for mov in solucion:
        print(f"{mov[0]} → {mov[1]} | Disco {mov[2]}")

print(f"\n Total de soluciones encontradas: {len(soluciones)}")
