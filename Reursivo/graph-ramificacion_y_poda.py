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


def hanoi_arbol_coloreado_ramificacion_y_poda(torres, total_discos, movimientos, soluciones, visitados, mejor_solucion_len, graph_file, nivel=0, padre_id=None, visitados_local=None, contador_nodos=[0]):
    if visitados_local is None:
        visitados_local = set()

    estado_actual = estado_serializado(torres)
    contador_nodos[0] += 1
    # ID único: estado + nivel + contador (pero el label solo muestra el estado)
    nombre_nodo = f"{estado_actual}_n{nivel}_c{contador_nodos[0]}"
    label = str(estado_actual)  # Label solo muestra el estado serializado
    color = "black"

    if estado_actual in visitados:
        color = "red"
        graph_file.write(f'    "{nombre_nodo}" [label="{label}", color={color}];\n')
        if padre_id is not None:
            graph_file.write(f'    "{padre_id}" -> "{nombre_nodo}";\n')
        return
    visitados.add(estado_actual)

    if mejor_solucion_len[0] is not None and len(movimientos) >= mejor_solucion_len[0]:
        color = "red"
        graph_file.write(f'    "{nombre_nodo}" [label="{label}", color={color}];\n')
        if padre_id is not None:
            graph_file.write(f'    "{padre_id}" -> "{nombre_nodo}";\n')
        return

    if len(torres["Destino"]) == total_discos:
        color = "blue"
        soluciones.append(list(movimientos))
        if mejor_solucion_len[0] is None or len(movimientos) < mejor_solucion_len[0]:
            mejor_solucion_len[0] = len(movimientos)
        graph_file.write(f'    "{nombre_nodo}" [label="{label}", color={color}];\n')
        if padre_id is not None:
            graph_file.write(f'    "{padre_id}" -> "{nombre_nodo}";\n')
        return

    movimientos_posibles = generar_movimientos_posibles(torres)
    ordenar_por_euristica(torres, movimientos_posibles)
        
    graph_file.write(f'    "{nombre_nodo}" [label="{label}", color={color}];\n')
    if padre_id is not None:
        graph_file.write(f'    "{padre_id}" -> "{nombre_nodo}";\n')

    for origen, destino, disco in movimientos_posibles:
        torres[origen].pop()
        torres[destino].append(disco)
        disco.mover()
        movimientos.append((origen, destino, disco.tamanio))

        hanoi_arbol_coloreado_ramificacion_y_poda(
            torres,
            total_discos,
            movimientos,
            soluciones,
            visitados.copy(),
            mejor_solucion_len,
            graph_file,
            nivel + 1,
            nombre_nodo,  # Padre ahora tiene ID único (pero el label es limpio)
            visitados_local,
            contador_nodos
        )

        movimientos.pop()
        torres[destino].pop()
        disco.deshacer_movimiento()
        torres[origen].append(disco)



# -------------------- EJECUCIÓN ------------------------

total_discos = 3
torres_iniciales = {
    "Origen": [DiscoFragil(3, 1), DiscoFragil(2, 2), DiscoFragil(1, 4)],
    "Auxiliar": [],
    "Destino": []
}

soluciones = []
visitados = set()

# En la parte de EJECUCIÓN (cambia solo la llamada a la función):
with open("hanoi_arbol_colores_ramificacion_y_poda.dot", "w", encoding="utf-8") as f:
    f.write("digraph Hanoi {\n")
    f.write("    rankdir=TB;\n")
    f.write("    node [shape=box, fontname=\"Arial\"];\n")
    hanoi_arbol_coloreado_ramificacion_y_poda(
        torres=copiar_torres(torres_iniciales), 
        total_discos=total_discos, 
        movimientos=[], 
        soluciones=soluciones, 
        visitados=visitados, 
        mejor_solucion_len=[None], 
        graph_file=f, 
        nivel=0, 
        padre_id=None, 
        visitados_local=set(),
        contador_nodos=[0]  # Contador inicializado aquí
    )
    f.write("}\n")

print("\n✅ Archivo 'hanoi_arbol_colores_ramificacion_y_poda.dot' generado con jerarquía y colores.")
