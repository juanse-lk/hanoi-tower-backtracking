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
    Heurística: Chequea cuántos discos están ordenados en la torre de destino.
    
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
    """
    Qué hace: Igual que el anterior, pero no evita repetir estados, lo cual puede hacer que explore más de lo necesario.

    Complejidad temporal: Más alta que el branch and bound con visitados, pero aún mejor que un backtracking puro.

    En palabras: Rápido en muchos casos, pero puede perder tiempo repitiendo caminos ya vistos.
    """
    total_discos = len(torres_iniciales['Origen'])
    nodos_vivos = []
    #genera una tupla con 3 valores: el número que devuelve la función de heuristica, una copia del diccionario de las torres y un array de movimientos vacios
    nodo_raiz = (heuristica_prioridad_discos_pequenos(torres_iniciales), copiar_torres(torres_iniciales), [])
    nodos_vivos.append(nodo_raiz)

    mejor_solucion = None
    max_movimientos = 2 ** total_discos# 2 elevado a la cantidad de discos, es un corte que hicimos para evitar loopear infinitamente

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
    """
    Qué hace: Usa una heurística para priorizar los caminos que parecen mejores y evita repetir estados.

    Complejidad temporal: Más baja que el backtracking. Depende de qué tan buena sea la heurística y de cuántos caminos se podan.

    En palabras: Mucho más inteligente, porque elige primero los caminos prometedores y descarta muchos otros innecesarios.
    """
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
    Qué hace: Igual que el anterior, pero se detiene apenas encuentra una solución válida.

    Complejidad temporal: Sigue siendo alta, pero más eficiente que el anterior si la primera solución se encuentra rápido.

    En palabras: Puede ser más rápido que el anterior porque no busca todas las soluciones, solo una.
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

def hanoi_backtracking_estados_visitados(torres, total_discos, movimientos, soluciones, visitados):
    """
    Qué hace: Explora todas las formas posibles de resolver el problema, evitando repetir estados ya visitados.

    Complejidad temporal: Muy alta, porque prueba casi todas las combinaciones posibles, aunque evita algunas repeticiones.

    En palabras: Tarda muchísimo tiempo porque explora casi todos los caminos posibles, pero se ahorra algo de tiempo al no repetir configuraciones que ya probó.
    """
    estado_actual = estado_serializado(torres)

    # Verificar si el estado actual ya fue visitado
    if estado_actual in visitados:
        return
    # Marcar el estado actual como visitado
    visitados.add(estado_actual)

    # Verificar si se ha alcanzado la solución
    # vemos cuantos discos hay en la torre destino y verifica si es igual al total de discos
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

            # Mover disco
            torres[origen].pop()
            torres[destino].append(disco)
            disco.mover()# solamente incrementa los movimientos del disco( solo es útil para DiscoFragil)

            # Registrar el movimiento
            movimientos.append((origen, destino, disco.tamanio))

            hanoi_backtracking_estados_visitados(
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
total_discos = 3
if __name__ == "__main__":
    import time
    import tracemalloc

    torres_iniciales = {
        "Origen": [Disco(3),Disco(2), DiscoFragil(1,64)],
        "Auxiliar": [],
        "Destino": [],
    }

    soluciones = []
    visitados = set()
    print("\n----------- BACKTRACKING estados visitados ------------")
    inicio = time.time()
    hanoi_backtracking_estados_visitados(torres_iniciales, total_discos, [], soluciones, visitados)
    fin = time.time()
    movimientos_bt_visitados = [len(sol) for sol in soluciones]
    print(f"Total de soluciones encontradas: {len(soluciones)}")
    soluciones.sort(key=len, reverse=True)
    # Mostrar soluciones
    for i, solucion in enumerate(soluciones, 1):
         print(f"\n🔹 Solución {i} ({len(solucion)} movimientos):")
         for mov in solucion:
             print(f"{mov[0]} → {mov[1]} | Disco {mov[2]}")
    print(f"\n🕒 Tiempo de ejecución VISITADOS: {fin - inicio:.4f} segundos")
    if movimientos_bt_visitados:
        print(f"\n🔢 Soluciones: {len(movimientos_bt_visitados)} | Mínimos movimientos: {min(movimientos_bt_visitados)} | Promedio: {sum(movimientos_bt_visitados)/len(movimientos_bt_visitados):.2f}")
    print("🧮 Complejidad esperada: O(2^n)")
    print("----------- fin BACKTRACKING estados visitados ------------")



    soluciones = []
    visitados = set()
    print("\n----------- BACKTRACKING solución única ------------")
    inicio = time.time()
    hanoi_backtracking_solucion_unica(torres_iniciales, total_discos, [], soluciones, visitados)
    fin = time.time()
    movimientos_bt_unica = [len(sol) for sol in soluciones]
    print(f"Total de soluciones encontradas: {len(soluciones)}")
    soluciones.sort(key=len, reverse=True)
    # Mostrar soluciones
    for i, solucion in enumerate(soluciones, 1):
         print(f"\n🔹 Solución {i} ({len(solucion)} movimientos):")
         for mov in solucion:
             print(f"{mov[0]} → {mov[1]} | Disco {mov[2]}")
    print(f"\n🕒 Tiempo de ejecución VISITADOS: {fin - inicio:.4f} segundos")
    if movimientos_bt_unica:
        print(f"\n🔢 Soluciones: {len(movimientos_bt_unica)} | Mínimos movimientos: {min(movimientos_bt_unica)} | Promedio: {sum(movimientos_bt_unica)/len(movimientos_bt_unica):.2f}")
    print("🧮 Complejidad esperada: O(2^n)")
    print("----------- fin BACKTRACKING solución única ------------")
    
    

    print("\n----------- BRANCH & BOUND visitados ------------")
    # ⏱️ Inicio de medición
    #tracemalloc.start()
    inicio = time.time()
    solucion = hanoi_branch_and_bound_estados_visitados(torres_iniciales)
    # ⏱️ Fin de medición
    fin = time.time()
    #mem_actual, mem_pico = tracemalloc.get_traced_memory()
    #tracemalloc.stop()
    print("Mejor solución encontrada VISITADOS:")
    for i, mov in enumerate(solucion, 1):
        print(f"{i}. Mover disco {mov[2]} de {mov[0]} a {mov[1]}")
    print(f"\n🕒 Tiempo de ejecución VISITADOS: {fin - inicio:.4f} segundos")
    #print(f"📈 Memoria actual usada VISITADOS: {mem_actual / 1024:.2f} KB")
    #print(f"🚀 Pico de memoria VISITADOS: {mem_pico / 1024:.2f} KB")
    print(f"\n🔢 Total de movimientos: {len(solucion)}")
    print("🧮 Complejidad esperada: O(b^d) donde b = branching factor y d = profundidad")
    print("----------- fin BRANCH & BOUND visitados ------------")



    print("\n----------- BRANCH & BOUND sin visitados ------------")
    inicio = time.time()
    solucion = hanoi_branch_and_bound_sin_visitados(torres_iniciales)
    fin = time.time()
    print("Mejor solución encontrada SIN VISITADOS:")
    for i, mov in enumerate(solucion, 1):
        print(f"{i}. Mover disco {mov[2]} de {mov[0]} a {mov[1]}")
    print(f"\n🕒 Tiempo de ejecución SIN VISITADOS: {fin - inicio:.4f} segundos")
    print(f"\n🔢 Total de movimientos: {len(solucion)}")
    print("🧮 Complejidad esperada: O(b^d) sin poda de estados repetidos")
    print("----------- fin BRANCH & BOUND sin visitados ------------")
    