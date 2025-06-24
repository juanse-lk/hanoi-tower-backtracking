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
    destino = torres["Destino"]
    correcto = 0
    for i, disco in enumerate(reversed(destino)):
        if disco.tamanio == i + 1:
            correcto += 1
        else:
            break
    return total_discos - correcto


def hanoi_branch_and_bound(torres_iniciales):
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


# 🔽 Ejemplo de uso:
total_discos = 5
if __name__ == "__main__":
    # Crear torres con 3 discos en "Origen"
    torres = {
        "Origen": [Disco(5), Disco(4),Disco(3), Disco(2), DiscoFragil(1,100)],
        "Auxiliar": [],
        "Destino": [],
    }

    solucion = hanoi_branch_and_bound(torres)

    print("Mejor solución encontrada:")
    for i, mov in enumerate(solucion, 1):
        print(f"{i}. Mover disco {mov[2]} de {mov[0]} a {mov[1]}")