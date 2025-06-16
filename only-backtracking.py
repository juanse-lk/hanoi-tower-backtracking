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


def hanoi_backtracking(torres, movimientos, soluciones, visitados):
    estado_actual = estado_serializado(torres)

    if estado_actual in visitados:
        return
    visitados.add(estado_actual)

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
                movimientos,
                soluciones,
                visitados.copy()  # copiar visitados para mantener independencia por camino
            )

            # Deshacer movimiento
            movimientos.pop()
            torres[destino].pop()
            disco.deshacer_movimiento()
            torres[origen].append(disco)


# -------------------- EJECUCIÓN ------------------------

total_discos = 3
torres_iniciales = {
    "Origen": [DiscoFragil(3, 1), DiscoFragil(2,2), DiscoFragil(1,4)],
    "Auxiliar": [],
    "Destino": []
}

soluciones = []
visitados = set()

hanoi_backtracking(copiar_torres(torres_iniciales), [], soluciones, visitados)

soluciones.sort(key=len, reverse=True)
# Mostrar soluciones
for i, solucion in enumerate(soluciones, 1):
    print(f"\n🔹 Solución {i} ({len(solucion)} movimientos):")
    for mov in solucion:
        print(f"{mov[0]} → {mov[1]} | Disco {mov[2]}")

print(f"\n Total de soluciones encontradas: {len(soluciones)}")
