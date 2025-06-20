# prueba de Ramificacion ordenando como mejor camino el que tenga mas fichas colocadas en orden en la torre destino

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
            estado.append(0)  # Separador entre torres
        for d in torres[nombre]:
            estado.append(d.tamanio)
    return tuple(estado)


def ordenar_por_euristica(torres, movimientos_posibles):
    movimientos_posibles.sort(key=lambda mov: obtener_cantidad_discos_ordenados(torres, mov), reverse=True)


def obtener_cantidad_discos_ordenados(torres, movimiento):
    """Simula el movimiento y calcula cuantos discos quedan en la torre destino"""
    origen, destino, disco = movimiento
    torres[origen].pop()
    torres[destino].append(disco)
    ordenados = len(torres["Destino"]) # Discos ordenados en destino
    torres[destino].pop()
    torres[origen].append(disco)
    return ordenados


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


def hanoi_backtracking(torres, total_discos, movimientos, soluciones, visitados):
    estado_actual = estado_serializado(torres)
    if estado_actual in visitados:
        return
    visitados.add(estado_actual)

    if len(torres["Destino"]) == total_discos:
        soluciones.append(list(movimientos))
        return

    movimientos_posibles = generar_movimientos_posibles(torres)

    #Ordeno segun euristica,
    ordenar_por_euristica(torres, movimientos_posibles)
        

    for origen, destino, disco in movimientos_posibles:
        torres[origen].pop()
        torres[destino].append(disco)
        disco.mover()
        movimientos.append((origen, destino, disco.tamanio))

        hanoi_backtracking(
            torres,
            total_discos,
            movimientos,
            soluciones,
            visitados.copy()
        )

        movimientos.pop()
        torres[destino].pop()
        disco.deshacer_movimiento()
        torres[origen].append(disco)

