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

def hanoi_iterativo(torres_iniciales, total_discos):
    soluciones = []
    nodos_vivos = [] 

    estado_inicial = copiar_torres(torres_iniciales)
    nodos_vivos.append((estado_inicial, [], set([estado_serializado(estado_inicial)])))

    while nodos_vivos:
        torres, movimientos, visitados_en_rama = nodos_vivos.pop()

        if len(torres["Destino"]) == total_discos:
            soluciones.append(movimientos)
            continue

        for origen, destino, disco in generar_movimientos_posibles(torres):
            nuevas_torres = copiar_torres(torres)
            nuevas_torres[origen].pop()
            nuevas_torres[destino].append(disco)
            disco.mover()

            nuevo_movimiento = (origen, destino, disco.tamanio)
            historial_movimeintos = movimientos + [nuevo_movimiento]
            nuevo_estado = estado_serializado(nuevas_torres)

            if nuevo_estado in visitados_en_rama:
                continue

            nueva_rama_visitados = visitados_en_rama.copy()
            nueva_rama_visitados.add(nuevo_estado)
            nodos_vivos.append((nuevas_torres, historial_movimeintos, nueva_rama_visitados))

    return soluciones

# -------------------- EJECUCIÓN ------------------------
total_discos = 3
torres_iniciales = {
    "Origen": [Disco(3), Disco(2), Disco(1)],
    "Auxiliar": [],
    "Destino": []
}

soluciones = hanoi_iterativo(torres_iniciales, total_discos)

soluciones.sort(key=len, reverse=True)

for i, solucion in enumerate(soluciones, 1):
    print(f"\n🔹 Solución {i} ({len(solucion)} movimientos):")
    for mov in solucion:
        print(f"{mov[0]} → {mov[1]} | Disco {mov[2]}")

print(f"\n Total de soluciones encontradas: {len(soluciones)}")
