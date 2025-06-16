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


def hanoi_arbol_coloreado(torres, graph_file, nivel=0, nodo_id=[0], padre_id=None, visitados_local=None):
    if visitados_local is None:
        visitados_local = set()

    estado_actual = estado_serializado(torres)
    nodo_actual_id = nodo_id[0]
    nodo_id[0] += 1

    nombre_nodo = f"n{nodo_actual_id}"
    label = str(estado_actual)
    color = "black"

    if len(torres["Destino"]) == total_discos:
        color = "blue"  # Solución encontrada
    elif estado_actual in visitados_local:
        color = "red"    # Estado ya visitado en este camino
    else:
        visitados_local.add(estado_actual)

    graph_file.write(f'    "{nombre_nodo}" [label="{label}", color={color}];\n')
    if padre_id is not None:
        graph_file.write(f'    "{padre_id}" -> "{nombre_nodo}";\n')

    if color == "red" or len(torres["Destino"]) == total_discos:
        return

    puedo_avanzar = False # Solo se usa para graficar las interrupciones con dicos fragiles

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

            # Si llegó hasta acá, se puede hacer al menos un movimiento
            puedo_avanzar = True

            # Mover disco
            torres[origen].pop()
            torres[destino].append(disco)
            disco.mover()
            hanoi_arbol_coloreado(
                torres, graph_file, nivel + 1, nodo_id,
                nombre_nodo, visitados_local.copy()
            )
            # Deshacer
            torres[destino].pop()
            torres[origen].append(disco)
            disco.deshacer_movimiento()

    # Si no se pudo avanzar y no fue por visitado o solución, es por disco frágil bloqueado
    if not puedo_avanzar and color == "black":
        color = "yellow"
        # Reescribimos el nodo con nuevo color
        graph_file.write(f'    "{nombre_nodo}" [label="{label}", color={color}];\n')
# -------------------- EJECUCIÓN ------------------------

total_discos = 3
torres_iniciales = {
    "Origen": [DiscoFragil(3,1),DiscoFragil(2,2), DiscoFragil(1,4)],
    "Auxiliar": [],
    "Destino": []
}

with open("hanoi_arbol_colores.dot", "w", encoding="utf-8") as f:
    f.write("digraph Hanoi {\n")
    f.write("    rankdir=TB;\n")
    f.write("    node [shape=box, fontname=\"Arial\"];\n")
    hanoi_arbol_coloreado(copiar_torres(torres_iniciales), f, 0, [0], None, set())
    f.write("}\n")

print("✅ Archivo 'hanoi_arbol_colores.dot' generado con nodos terminales en rojo.")