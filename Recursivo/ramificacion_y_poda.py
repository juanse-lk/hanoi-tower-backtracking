# prueba de Ramificacion ordenando como mejor camino el que tenga mas fichas colocadas en orden en la torre destino

def estado_serializado(torres):
    estado = []
    for nombre in ["Origen", "Auxiliar", "Destino"]:
        if nombre != "Origen":
            estado.append(0)  # Separador entre torres
        for d in torres[nombre]:
            estado.append(d.tamanio)
    return tuple(estado)


def ordenar_por_euristica(torres, movimientos_posibles):
    movimientos_posibles.sort(key=lambda mov: estimar_beneficio_movimiento(torres, mov), reverse=True)


def estimar_beneficio_movimiento(torres, movimiento):
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


def hanoi_backtracking(torres, total_discos, movimientos, soluciones, visitados, mejor_solucion_len):
    estado_actual = estado_serializado(torres)
    if estado_actual in visitados:
        return
    visitados.add(estado_actual)

    if mejor_solucion_len[0] is not None and len(movimientos) >= mejor_solucion_len[0]:
        return

    if len(torres["Destino"]) == total_discos:
        soluciones.append(list(movimientos))
        # Actualizamos mejor solución
        if mejor_solucion_len[0] is None or len(movimientos) < mejor_solucion_len[0]:
            mejor_solucion_len[0] = len(movimientos)
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
            visitados.copy(),
            mejor_solucion_len
        )

        movimientos.pop()
        torres[destino].pop()
        disco.deshacer_movimiento()
        torres[origen].append(disco)
