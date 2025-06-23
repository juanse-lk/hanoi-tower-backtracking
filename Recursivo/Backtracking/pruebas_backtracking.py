import time
import tracemalloc
from e1_backtracking_estados_visitados import hanoi_backtracking as estrategia_1
from e2_backtracking_sin_repeticion import hanoi_backtracking as estrategia_2
from e3_backtracking_solucion_unica import hanoi_backtracking as estrategia_3
from e4_backtracking_limite_movimientos import hanoi_backtracking as estrategia_4
from e5_backtracking_optimizado import hanoi_backtracking as estrategia_5

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


### PRUEBAS
# Creo los discos y torres
torres_iniciales = {
    "Origen": [Disco(3), Disco(2), Disco(1)],
    "Auxiliar": [],
    "Destino": []
}
total_discos = len(torres_iniciales["Origen"])

#--- Prueba solo backtracking

# # Estrategia 1
# # Backtracking con estados visitados

# copia_torres = copiar_torres(torres_iniciales)

# soluciones = []
# visitados = set()

# # ⏱️ Inicio de medición
# tracemalloc.start()
# inicio = time.time()

# estrategia_1(copia_torres, total_discos, [], soluciones, visitados)

# # ⏱️ Fin de medición
# fin = time.time()
# mem_actual, mem_pico = tracemalloc.get_traced_memory()
# tracemalloc.stop()

# print("-----------  Estrategia 1 ------------")

# # Ordenar de mayor a menor 
# soluciones.sort(key=len, reverse=True)

# print(f"\n✅ Solución más larga con {len(soluciones[0])} movimientos:")

# # Ordenar de menor a mayor
# soluciones.sort(key=len, reverse=False)

# print(f"\n✅ Solución más corta con {len(soluciones[0])} movimientos:")


# print(f"\n🕒 Tiempo de ejecución: {fin - inicio:.4f} segundos")
# print(f"📈 Memoria actual usada: {mem_actual / 1024:.2f} KB")
# print(f"🚀 Pico de memoria: {mem_pico / 1024:.2f} KB")
# print(f"\n Total de soluciones encontradas: {len(soluciones)}")


# # Estrategia 2
# # Backtracking sin repetición de estados visitados

# copia_torres = copiar_torres(torres_iniciales)

# soluciones = []
# visitados = set()

# # ⏱️ Inicio de medición
# tracemalloc.start()
# inicio = time.time()

# estrategia_2(copia_torres, total_discos, [], soluciones, visitados)

# # ⏱️ Fin de medición
# fin = time.time()
# mem_actual, mem_pico = tracemalloc.get_traced_memory()
# tracemalloc.stop()

# print("\n-----------  Estrategia 2 ------------")


# # Ordenar de mayor a menor (o podés hacerlo al revés con reverse=False)
# soluciones.sort(key=len, reverse=True)

# print(f"\n✅ Solución más larga con {len(soluciones[0])} movimientos:")

# # Ordenar de menor a mayor
# soluciones.sort(key=len, reverse=False)

# print(f"\n✅ Solución más corta con {len(soluciones[0])} movimientos:")


# print(f"\n🕒 Tiempo de ejecución: {fin - inicio:.4f} segundos")
# print(f"📈 Memoria actual usada: {mem_actual / 1024:.2f} KB")
# print(f"🚀 Pico de memoria: {mem_pico / 1024:.2f} KB")
# print(f"\n Total de soluciones encontradas: {len(soluciones)}")

# # Estrategia 3
# # Backtracking con una única solución
# # y sin repecitcion de estados visitados

# copia_torres = copiar_torres(torres_iniciales)

# soluciones = []
# visitados = set()

# # ⏱️ Inicio de medición
# tracemalloc.start()
# inicio = time.time()

# estrategia_3(copia_torres, total_discos, [], soluciones, visitados)

# # ⏱️ Fin de medición
# fin = time.time()
# mem_actual, mem_pico = tracemalloc.get_traced_memory()
# tracemalloc.stop()

# print("\n-----------  Estrategia 3 ------------")

# # Ordenar de mayor a menor (o podés hacerlo al revés con reverse=False)
# soluciones.sort(key=len, reverse=True)

# print(f"\n✅ Solución más larga con {len(soluciones[0])} movimientos:")

# # Ordenar de menor a mayor
# soluciones.sort(key=len, reverse=False)

# print(f"\n✅ Solución más corta con {len(soluciones[0])} movimientos:")


# print(f"\n🕒 Tiempo de ejecución: {fin - inicio:.4f} segundos")
# print(f"📈 Memoria actual usada: {mem_actual / 1024:.2f} KB")
# print(f"🚀 Pico de memoria: {mem_pico / 1024:.2f} KB")
# print(f"\n Total de soluciones encontradas: {len(soluciones)}")


# # Estrategia 4
# # Backtracking con límite de movimientos
# # y sin repetición de estados visitados

# copia_torres = copiar_torres(torres_iniciales)
# max_movimientos = (2 ** total_discos) + 50

# soluciones = []
# visitados = set()

# # ⏱️ Inicio de medición
# tracemalloc.start()
# inicio = time.time()

# estrategia_4(torres_iniciales, total_discos, [], soluciones, max_movimientos)

# # ⏱️ Fin de medición
# fin = time.time()
# mem_actual, mem_pico = tracemalloc.get_traced_memory()
# tracemalloc.stop()

# print("\n-----------  Estrategia 4 ------------")


# # Ordenar de mayor a menor (o podés hacerlo al revés con reverse=False)
# soluciones.sort(key=len, reverse=True)

# print(f"\n✅ Solución más larga con {len(soluciones[0])} movimientos")

# # Ordenar de menor a mayor
# soluciones.sort(key=len, reverse=False)

# print(f"\n✅ Solución más corta con {len(soluciones[0])} movimientos")


# print(f"\n🕒 Tiempo de ejecución: {fin - inicio:.4f} segundos")
# print(f"📈 Memoria actual usada: {mem_actual / 1024:.2f} KB")
# print(f"🚀 Pico de memoria: {mem_pico / 1024:.2f} KB")
# print(f"\n Total de soluciones encontradas: {len(soluciones)}")


# Estrategia 5
# Optimización de la serializacion

copia_torres = copiar_torres(torres_iniciales)

soluciones = []
visitados = set()

# ⏱️ Inicio de medición
tracemalloc.start()
inicio = time.time()

estrategia_5(torres_iniciales, total_discos, [], soluciones, visitados)

# ⏱️ Fin de medición
fin = time.time()
mem_actual, mem_pico = tracemalloc.get_traced_memory()
tracemalloc.stop()

print("\n-----------  Estrategia 5 ------------")


# Ordenar de mayor a menor (o podés hacerlo al revés con reverse=False)
soluciones.sort(key=len, reverse=True)

print(f"\n✅ Solución más larga con {len(soluciones[0])} movimientos")

# Ordenar de menor a mayor
soluciones.sort(key=len, reverse=False)

print(f"\n✅ Solución más corta con {len(soluciones[0])} movimientos")


print(f"\n🕒 Tiempo de ejecución: {fin - inicio:.4f} segundos")
print(f"📈 Memoria actual usada: {mem_actual / 1024:.2f} KB")
print(f"🚀 Pico de memoria: {mem_pico / 1024:.2f} KB")
print(f"\n Total de soluciones encontradas: {len(soluciones)}")