TORRES = ["Origen", "Auxiliar", "Destino"]

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
    return tuple(tuple(d.tamanio for d in torres[nombre]) for nombre in TORRES)

def hanoi_backtracking(torres, total_discos, movimientos, soluciones, visitados):
    estado_actual = estado_serializado(torres)
    if estado_actual in visitados:
        return

    visitados.add(estado_actual)

    if len(torres["Destino"]) == total_discos:
        soluciones.append(list(movimientos))
        visitados.remove(estado_actual)
        return

    for origen in TORRES:
        if not torres[origen]:
            continue

        disco = torres[origen][-1]

        for destino in TORRES:
            if (origen == destino or
                not disco.puede_moverse() or
                (torres[destino] and torres[destino][-1].tamanio < disco.tamanio) or
                (movimientos and disco.tamanio == movimientos[-1][2])):
                continue

            torres[origen].pop()
            torres[destino].append(disco)
            disco.mover()

            movimientos.append((origen, destino, disco.tamanio))

            hanoi_backtracking(torres, total_discos, movimientos, soluciones, visitados)

            movimientos.pop()
            torres[destino].pop()
            disco.deshacer_movimiento()
            torres[origen].append(disco)

    visitados.remove(estado_actual)


if __name__ == "__main__":
    total_discos = 2
    torres_iniciales = {
        "Origen": [Disco(2), Disco(1)],
        "Auxiliar": [],
        "Destino": []
    }

    soluciones = []
    visitados = set()

    hanoi_backtracking(torres_iniciales, total_discos, [], soluciones, visitados)

    print("-----------  SOLO BACKTRACKING ------------")
    print(f"\nTotal de soluciones encontradas: {len(soluciones)}")

    soluciones.sort(key=len, reverse=True)
    print("\n🔍 Resumen de soluciones:")
    for i, solucion in enumerate(soluciones, 1):
        print(f"🔹 Solución {i}: {len(solucion)} movimientos")
