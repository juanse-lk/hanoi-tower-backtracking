import time
import tracemalloc

from e1_byb_heuristica_simple import hanoi_branch_and_bound as estrategia_1
from e2_byb_heuristica_mejorada import hanoi_branch_and_bound as estrategia_2
from e3_byb_sin_visitados import hanoi_branch_and_bound as estrategia_3

# Para probar, descomenta la que corresponda
# estrategia_1 = ...
# estrategia_2 = ...
# estrategia_3 = ...

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


def probar_estrategia(nombre_estrategia, funcion_estrategia, torres_iniciales):
    print(f"\n--- Ejecutando {nombre_estrategia} ---")
    copia_torres = copiar_torres(torres_iniciales)

    tracemalloc.start()
    inicio = time.time()

    solucion = funcion_estrategia(copia_torres)  # Llama con un solo argumento, adaptá si tu función necesita otro

    fin = time.time()
    mem_actual, mem_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if solucion:
        print(f"✅ Solución encontrada con {len(solucion)} movimientos")
        # for i, mov in enumerate(solucion, 1):
        #    print(f"{i}. Mover disco {mov[2]} de {mov[0]} a {mov[1]}")
    else:
        print("❌ No se encontró solución")

    print(f"🕒 Tiempo de ejecución: {fin - inicio:.4f} segundos")
    print(f"📈 Memoria actual usada: {mem_actual / 1024:.2f} KB")
    print(f"🚀 Pico de memoria: {mem_pico / 1024:.2f} KB")


if __name__ == "__main__":
    torres_iniciales = {
        "Origen": [Disco(3), Disco(2), DiscoFragil(1, 100)],
        "Auxiliar": [],
        "Destino": []
    }

    # Ejecutar Estrategia 1
    # probar_estrategia("Estrategia 1 - Heurística Simple", estrategia_1, torres_iniciales)

    # Ejecutar Estrategia 2
    probar_estrategia("Estrategia 2 - Heurística Mejorada", estrategia_2, torres_iniciales)

    # Ejecutar Estrategia 3
    # probar_estrategia("Estrategia 3 - Sin visitados", estrategia_3, torres_iniciales)
