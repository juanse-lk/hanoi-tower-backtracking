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
    estado = []
    for torre in ["Origen", "Auxiliar", "Destino"]:
        if torre != "Origen":
            estado.append(0)  # Separador
        for disco in torres[torre]:
            estado.append(disco.tamanio)
    return tuple(estado)


def copiar_torres(torres):
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


def heuristica(torres):
    """
    Heurística ponderada combinada:
    - Para cada disco de tamaño i:
      weight = 2**(i-1)
    - Distancia del poste:
      Origen   -> factor 2
      Auxiliar -> factor 1
      Destino  -> factor 0
    Retorna la suma de weight * factor para todos los discos.
    """
    factor_map = {'Origen': 2, 'Auxiliar': 1, 'Destino': 0}
    h = 0
    for torre_nombre, pila in torres.items():
        factor = factor_map.get(torre_nombre, 0)
        for disco in pila:
            # peso exponencial según el tamaño del disco
            peso = 2 ** (disco.tamanio - 1)
            h += peso * factor
    return h


def hanoi_branch_and_bound(torres_iniciales):
    total_discos = len(torres_iniciales['Origen'])
    nodos_vivos = []
    estado_ini = estado_serializado(torres_iniciales)
    nodo_raiz = (heuristica(torres_iniciales, total_discos), copiar_torres(torres_iniciales), [], set([estado_ini]))
    nodos_vivos.append(nodo_raiz)

    mejor_solucion = None
    mejor_costo = float('inf')

    while nodos_vivos:
        # Ramificación: ordenar por heurística + profundidad
        nodos_vivos.sort(key=lambda nodo: nodo[0], reverse=True)
        costo_estimado, torres, movimientos, visitados = nodos_vivos.pop()

        # Poda: si ya es más largo que el mejor, descartamos
        if len(movimientos) >= mejor_costo:
            continue

        # ¿Es solución?
        if len(torres["Destino"]) == total_discos:
            mejor_solucion = movimientos
            mejor_costo = len(movimientos)
            continue

        for origen, destino, disco in generar_movimientos_posibles(torres):

            if movimientos and movimientos[-1][2] == disco.tamanio: # si estoy moviendo el mismo disco dos veces podo
                continue
            
            if not disco.puede_moverse():
                continue

            nuevas_torres = copiar_torres(torres)
            disco_en_nuevas_torres = nuevas_torres[origen].pop()
            nuevas_torres[destino].append(disco_en_nuevas_torres)
            disco_en_nuevas_torres.mover()

            nuevo_estado = estado_serializado(nuevas_torres)
            if nuevo_estado in visitados:
                continue

            nuevo_visitados = visitados.copy()
            nuevo_visitados.add(nuevo_estado)
            nuevos_movs = movimientos + [(origen, destino, disco_en_nuevas_torres.tamanio)]
            nuevo_costo = len(nuevos_movs) + heuristica(nuevas_torres, total_discos)

            
            nodos_vivos.append((nuevo_costo, nuevas_torres, nuevos_movs, nuevo_visitados))

    return mejor_solucion


# 🔽 Ejemplo de uso:

if __name__ == "__main__":

    import time
    import tracemalloc
    # Crear torres con 3 discos en "Origen"
    torres = {
        "Origen": [Disco(5),Disco(4),Disco(3),Disco(2), DiscoFragil(1,64)],
        "Auxiliar": [],
        "Destino": [],
    }
    # ⏱️ Inicio de medición
    tracemalloc.start()
    inicio = time.time()

    solucion = hanoi_branch_and_bound(torres)

    # print("Mejor solución encontrada:")
    # for i, mov in enumerate(solucion, 1):
    #     print(f"{i}. Mover disco {mov[2]} de {mov[0]} a {mov[1]}")
    # ⏱️ Fin de medición
    fin = time.time()
    mem_actual, mem_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()


    print(f"\n🕒 Tiempo de ejecución: {fin - inicio:.4f} segundos")
    print(f"📈 Memoria actual usada: {mem_actual / 1024:.2f} KB")
    print(f"🚀 Pico de memoria: {mem_pico / 1024:.2f} KB")
