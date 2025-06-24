import heapq
import itertools
import time

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
    for nombre in ["Origen", "Auxiliar", "Destino"]:
        if nombre != "Origen":
            estado.append(0)  # Separador al principio de cada torre
        for d in torres[nombre]:
            estado.append(d.tamanio)
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


def heuristica_prioridad_discos_pequenos(torres):
    """
    Heurística del enunciado: Chequea cuántos discos están ordenados en la torre de destino.
    
    Una heurística común prioriza mover los discos más pequeños primero porque:
    * Permite liberar los discos más grandes
    * Crea espacio para mover discos intermedios
    * Sigue la estrategia óptima natural del problema
    
    En el caso de éste algoritmo, un valor más bajo indica un estado más cercano a la solución

    * En el Branch and Bound, los nodos con valores heurísticos más bajos se exploran primero (porque se ordenan en orden descendente pero luego se usa pop())
    * Esto prioriza estados donde más discos están correctamente colocados en el destino
    * Priorización implícita: Aunque el nombre sugiere priorizar discos pequeños, la heurística realmente mide el progreso hacia la solución completa. 
        La priorización de discos pequeños ocurre indirectamente porque mover discos pequeños es necesario para colocar correctamente los más grandes.
    """
    destino = torres["Destino"]
    correcto = 0
    for i, disco in enumerate(reversed(destino)):
        if disco.tamanio == i + 1:
            correcto += 1
        else:
            break
    return total_discos - correcto


def hanoi_branch_and_bound_sin_visitados(torres_iniciales):
    total_discos = len(torres_iniciales['Origen'])
    nodos_vivos = []
    nodo_raiz = (heuristica_prioridad_discos_pequenos(torres_iniciales), copiar_torres(torres_iniciales), [])
    nodos_vivos.append(nodo_raiz)

    mejor_solucion = None
    max_movimientos = 2 ** total_discos

    while nodos_vivos:
        # Ramificación: ordenar por heurística + profundidad
        nodos_vivos.sort(key=lambda nodo: nodo[0], reverse=True)
        costo_estimado, torres, movimientos = nodos_vivos.pop()

        # Poda: si ya es más largo que el mejor, descartamos
        if len(movimientos) >= max_movimientos:
            continue

        # Es solución?
        if len(torres["Destino"]) == total_discos:
            mejor_solucion = movimientos
            max_movimientos = len(movimientos)
            continue

        for origen, destino, disco in generar_movimientos_posibles(torres):

            if movimientos and movimientos[-1][2] == disco.tamanio: # si estoy moviendo el mismo disco dos veces podo
                continue

            if not disco.puede_moverse():
                continue

            nuevas_torres = copiar_torres(torres) # Crear la copia del estado actual
            disco_en_nuevas_torres = nuevas_torres[origen].pop()
            nuevas_torres[destino].append(disco_en_nuevas_torres)
            disco_en_nuevas_torres.mover()

            nuevos_movs = movimientos + [(origen, destino, disco_en_nuevas_torres.tamanio)]
            nuevo_costo = len(nuevos_movs) + heuristica_prioridad_discos_pequenos(nuevas_torres)
            nodos_vivos.append((nuevo_costo, nuevas_torres, nuevos_movs))

    return mejor_solucion


def hanoi_branch_and_bound_estados_visitados(torres_iniciales):
    total_discos = len(torres_iniciales['Origen'])
    nodos_vivos = []
    estado_ini = estado_serializado(torres_iniciales)
    nodo_raiz = (heuristica_prioridad_discos_pequenos(torres_iniciales), copiar_torres(torres_iniciales), [], set([estado_ini]))
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
            nuevo_costo = len(nuevos_movs) + heuristica_prioridad_discos_pequenos(nuevas_torres)

            
            nodos_vivos.append((nuevo_costo, nuevas_torres, nuevos_movs, nuevo_visitados))

    return mejor_solucion

def hanoi_backtracking_solucion_unica(torres, total_discos, movimientos, soluciones, visitados):
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

    # Verificar si el estado actual ya fue visitado o si ya se encontró una solución
    if soluciones or estado_actual in visitados:
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
            # No mover si el disco no puede moverse
            # No mover a una torre que ya tiene un disco más grande en la parte superior
            # Evitar mover el mismo disco en dos turnos seguidos
            if (
            origen == destino or
            not disco.puede_moverse() or
            (torres[destino] and torres[destino][-1].tamanio < disco.tamanio) or
            (movimientos and disco.tamanio == movimientos[-1][2])
            ):
                continue

            # Mover disco
            torres[origen].pop()
            torres[destino].append(disco)
            disco.mover()

            # Registrar el movimiento
            movimientos.append((origen, destino, disco.tamanio))

            hanoi_backtracking_solucion_unica(
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


# 🔽 Ejemplo de uso:
total_discos = 5
if __name__ == "__main__":
    """
    # Crear torres con 3 discos en "Origen"
    torres = {
        "Origen": [Disco(5), Disco(4),Disco(3), Disco(2), DiscoFragil(1,100)],
        "Auxiliar": [],
        "Destino": [],
    }
    
    solucion = hanoi_branch_and_bound_sin_visitados(torres)

    print("Mejor solución encontrada SIN VISITADOS:")
    for i, mov in enumerate(solucion, 1):
        print(f"{i}. Mover disco {mov[2]} de {mov[0]} a {mov[1]}")
    """
    
    import time
    import tracemalloc
    # Crear torres con 3 discos en "Origen"
    torres_iniciales = {
        "Origen": [Disco(5),Disco(4),Disco(3),Disco(2), DiscoFragil(1,64)],
        "Auxiliar": [],
        "Destino": [],
    }
    
    """
    # ⏱️ Inicio de medición
    tracemalloc.start()
    inicio = time.time()

    solucion = hanoi_branch_and_bound_estados_visitados(torres_iniciales)

    # print("Mejor solución encontrada:")
    # for i, mov in enumerate(solucion, 1):
    #     print(f"{i}. Mover disco {mov[2]} de {mov[0]} a {mov[1]}")
    # ⏱️ Fin de medición
    fin = time.time()
    mem_actual, mem_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()


    print(f"\n🕒 Tiempo de ejecución ESTADOS VISITADOS: {fin - inicio:.4f} segundos")
    print(f"📈 Memoria actual usada ESTADOS VISITADOS: {mem_actual / 1024:.2f} KB")
    print(f"🚀 Pico de memoria ESTADOS VISITADOS: {mem_pico / 1024:.2f} KB")
    """
    
    soluciones = []
    visitados = set()

    hanoi_backtracking_solucion_unica(torres_iniciales, total_discos, [], soluciones, visitados)
    
    print("-----------  SOLO BACKTRACKING ------------")
    print(f"\n Total de soluciones encontradas: {len(soluciones)}")
    soluciones.sort(key=len, reverse=True)
    # Mostrar soluciones
    for i, solucion in enumerate(soluciones, 1):
         print(f"\n🔹 Solución {i} ({len(solucion)} movimientos):")
         for mov in solucion:
             print(f"{mov[0]} → {mov[1]} | Disco {mov[2]}")
    # Mostrar cantidad de movimientos de cada solución
    print("\n🔍 Resumen de soluciones:")
    for i, solucion in enumerate(soluciones, 1):
        print(f"🔹 Solución {i}: {len(solucion)} movimientos")

    print(f"\n Total de soluciones encontradas: {len(soluciones)}")