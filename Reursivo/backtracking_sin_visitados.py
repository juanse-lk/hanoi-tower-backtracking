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


def hanoi_backtracking(torres, total_discos, movimientos, soluciones, max_movimientos_permitidos):
    if soluciones:
        return
    
    if len(movimientos) > max_movimientos_permitidos:
        return  # Corte por exceso de movimientos

    if len(torres["Destino"]) == total_discos:
        soluciones.append(list(movimientos))
        return

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

            # Mover disco
            torres[origen].pop()
            torres[destino].append(disco)
            disco.mover()
            movimientos.append((origen, destino, disco.tamanio))

            hanoi_backtracking(
                torres,
                total_discos,
                movimientos,
                soluciones,
                max_movimientos_permitidos
            )

            # Deshacer movimiento
            movimientos.pop()
            torres[destino].pop()
            disco.deshacer_movimiento()
            torres[origen].append(disco)


if __name__ == "__main__":
    total_discos = 6
    max_movimientos = (2 ** total_discos) + 50
    torres_iniciales = {
        "Origen": [Disco(6),Disco(5),Disco(4), Disco(3), DiscoFragil(2,max_movimientos), DiscoFragil(1,max_movimientos)],
        "Auxiliar": [],
        "Destino": []
    }
    # --- Prueba solo backtracking

    soluciones = []
    visitados = set()
    
    hanoi_backtracking(torres_iniciales, total_discos, [], soluciones, max_movimientos)

    print("-----------  SOLO BACKTRACKING ------------")
    print(f"\n Total de soluciones encontradas: {len(soluciones)}")


    
soluciones.sort(key=len, reverse=True)
# Mostrar soluciones
# for i, solucion in enumerate(soluciones, 1):
#     print(f"\n🔹 Solución {i} ({len(solucion)} movimientos):")
for mov in soluciones[-1]:
    print(f"{mov[0]} → {mov[1]} | Disco {mov[2]}")

print(f"\n Total de soluciones encontradas: {len(soluciones)}")