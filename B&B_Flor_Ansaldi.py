"""
----------------------------------------------------------------------------------------------------------------------------
DUDA EXISTENCIAL:

En el enunciado dice:
 
'''
...Utiliza una heurística que priorice colocar números en 
las celdas más restringidas (las que tienen menos opciones disponibles). 

Tareas: 

1. Branch & Bound: 
    o Modifica la solución de backtracking para incorporar B&B. Utiliza 
        una heurística que priorice colocar los discos mas pequeños.
'''

La duda es...¿ambas expresiones indican lo mismo o pueden existir al mismo tiempo? o más importante ¿son excluyentes?
----------------------------------------------------------------------------------------------------------------------------
"""

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

"""
def estado_serializado(torres):
    estado = []
    for nombre in ["Origen", "Auxiliar", "Destino"]:
        estado.append('|')
        for d in torres[nombre]:
            estado.append(str(d.tamanio))
    return ''.join(estado)
"""

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


def heuristica_prioridad_discos_pequeños(torres):
    destino = torres["Destino"]
    correcto = 0
    for i, disco in enumerate(reversed(destino)):
        if disco.tamanio == i + 1:
            correcto += 1
        else:
            break
    return total_discos - correcto


def hanoi_branch_and_bound(torres_iniciales):
    inicio = time.time()
    heap = []
    visitados = {}
    mejor_solucion = None
    contador = itertools.count()
    nodos_explorados = 0

    estado_inicial = estado_serializado(torres_iniciales)
    heapq.heappush(heap, (0, 0, next(contador), estado_inicial, torres_iniciales, []))

    while heap:
        _, costo, _, estado, torres, camino = heapq.heappop(heap)
        nodos_explorados += 1

        if estado in visitados and visitados[estado] <= costo:
            continue
        visitados[estado] = costo

        if len(torres["Destino"]) == total_discos:
            if mejor_solucion is None or len(camino) < len(mejor_solucion):
                mejor_solucion = list(camino)
            continue

        for origen in torres:
            if not torres[origen]:
                continue
            disco = torres[origen][-1]
            for destino in torres:
                if origen == destino:
                    continue
                if torres[destino] and torres[destino][-1].tamanio < disco.tamanio:
                    continue
                if not disco.puede_moverse():
                    continue

                torres[origen].pop()
                torres[destino].append(disco)
                disco.mover()
                camino.append((origen, destino, disco.tamanio))

                nuevo_estado = estado_serializado(torres)
                nuevo_costo = costo + 1
                heuristica = heuristica_prioridad_discos_pequeños(torres)
                estimado_total = nuevo_costo + heuristica

                if mejor_solucion is None or estimado_total < len(mejor_solucion):
                    heapq.heappush(
                        heap,
                        (estimado_total, nuevo_costo, next(contador), nuevo_estado, copiar_torres(torres), list(camino))
                    )

                camino.pop()
                torres[destino].pop()
                disco.deshacer_movimiento()
                torres[origen].append(disco)

    fin = time.time()
    return mejor_solucion, nodos_explorados, fin - inicio


# Configuración inicial
total_discos = 3
torres_iniciales = {
    "Origen": [DiscoFragil(3, 1), DiscoFragil(2, 4), DiscoFragil(1, 4)],
    "Auxiliar": [],
    "Destino": []
}

# Alternativamente, podrías usar discos frágiles:
"""
torres_iniciales = {
    "Origen": [DiscoFragil(3, 1), DiscoFragil(2, 4), DiscoFragil(1, 4)],
    "Auxiliar": [],
    "Destino": []
}
"""

solucion, nodos, duracion = hanoi_branch_and_bound(copiar_torres(torres_iniciales))

# Mostrar resultados
if solucion:
    print(f"\n🔹 Mejor solución encontrada ({len(solucion)} movimientos):")
    for mov in solucion:
        print(f"{mov[0]} → {mov[1]} | Disco {mov[2]}")
else:
    print("❌ No se encontró una solución válida.")

print(f"\n📊 Estadísticas:")
print(f"🔁 Nodos explorados: {nodos}")
print(f"⏱️ Tiempo de ejecución: {duracion:.4f} segundos")