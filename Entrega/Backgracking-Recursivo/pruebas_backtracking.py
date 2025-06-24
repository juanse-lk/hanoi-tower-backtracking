import time
import tracemalloc
from e1_backtracking_estados_visitados import hanoi_backtracking as estrategia_1
from e2_backtracking_sin_repeticion import hanoi_backtracking as estrategia_2
from e3_backtracking_solucion_unica import hanoi_backtracking as estrategia_3
from e4_backtracking_limite_movimientos import hanoi_backtracking as estrategia_4
from e5_backtracking_nueva_serializacion import hanoi_backtracking as estrategia_5

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


def imprimir_resultados(estrategia_num, soluciones, tiempo, mem_actual, mem_pico):
    print(f"\n-----------  Estrategia {estrategia_num} ------------")

    if len(soluciones) == 0:
        print("\n❌ No se encontraron soluciones.")
    else:
        soluciones.sort(key=len, reverse=True)
        print(f"\n✅ Solución más larga con {len(soluciones[0])} movimientos:")

        soluciones.sort(key=len, reverse=False)
        print(f"\n✅ Solución más corta con {len(soluciones[0])} movimientos:")

    print(f"\n🕒 Tiempo de ejecución: {tiempo:.4f} segundos")
    print(f"📈 Memoria actual usada: {mem_actual / 1024:.2f} KB")
    print(f"🚀 Pico de memoria: {mem_pico / 1024:.2f} KB")
    print(f"\n Total de soluciones encontradas: {len(soluciones)}")


### PRUEBAS
# Creo los discos y torres
torres_iniciales = {
    "Origen": [Disco(2), Disco(1)],
    "Auxiliar": [],
    "Destino": []
}
total_discos = len(torres_iniciales["Origen"])


# Estrategia 1
copia_torres = copiar_torres(torres_iniciales)
soluciones = []
visitados = set()

tracemalloc.start()
inicio = time.time()

estrategia_1(copia_torres, total_discos, [], soluciones, visitados)

fin = time.time()
mem_actual, mem_pico = tracemalloc.get_traced_memory()
tracemalloc.stop()

imprimir_resultados(1, soluciones, fin - inicio, mem_actual, mem_pico)


# Estrategia 2
copia_torres = copiar_torres(torres_iniciales)
soluciones = []
visitados = set()

tracemalloc.start()
inicio = time.time()

estrategia_2(copia_torres, total_discos, [], soluciones, visitados)

fin = time.time()
mem_actual, mem_pico = tracemalloc.get_traced_memory()
tracemalloc.stop()

imprimir_resultados(2, soluciones, fin - inicio, mem_actual, mem_pico)


# Estrategia 3
copia_torres = copiar_torres(torres_iniciales)
soluciones = []
visitados = set()

tracemalloc.start()
inicio = time.time()

estrategia_3(copia_torres, total_discos, [], soluciones, visitados)

fin = time.time()
mem_actual, mem_pico = tracemalloc.get_traced_memory()
tracemalloc.stop()

imprimir_resultados(3, soluciones, fin - inicio, mem_actual, mem_pico)


# # Estrategia 4
# copia_torres = copiar_torres(torres_iniciales)
# max_movimientos = (2 ** total_discos) * 2
# soluciones = []
# visitados = set()

# tracemalloc.start()
# inicio = time.time()

# estrategia_4(copia_torres, total_discos, [], soluciones, max_movimientos)

# fin = time.time()
# mem_actual, mem_pico = tracemalloc.get_traced_memory()
# tracemalloc.stop()

# imprimir_resultados(4, soluciones, fin - inicio, mem_actual, mem_pico)


# Estrategia 5
copia_torres = copiar_torres(torres_iniciales)
soluciones = []
visitados = set()

tracemalloc.start()
inicio = time.time()

estrategia_5(copia_torres, total_discos, [], soluciones, visitados)

fin = time.time()
mem_actual, mem_pico = tracemalloc.get_traced_memory()
tracemalloc.stop()

imprimir_resultados(5, soluciones, fin - inicio, mem_actual, mem_pico)
