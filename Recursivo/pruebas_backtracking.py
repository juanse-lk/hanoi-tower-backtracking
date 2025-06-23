## Pruebas 
import time
import tracemalloc
from solo_backtracking import hanoi_backtracking as solo_backtracking
from backtracking_sin_repeticion import hanoi_backtracking as backtracking_sin_repeticion
from backtracking_sin_visitados import hanoi_backtracking as backtracking_sin_visitados
from backtracking_unica_solucion import hanoi_backtracking as backtracking_unica_solucion

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
    "Origen": [Disco(2), Disco(1)],
    "Auxiliar": [],
    "Destino": []
}
total_discos = len(torres_iniciales["Origen"])

#--- Prueba solo backtracking


# # Estrategia 1
# copia_torres = copiar_torres(torres_iniciales)

# soluciones = []
# visitados = set()

# # ⏱️ Inicio de medición
# tracemalloc.start()
# inicio = time.time()

# solo_backtracking(copia_torres, total_discos, [], soluciones, visitados)

# # ⏱️ Fin de medición
# fin = time.time()
# mem_actual, mem_pico = tracemalloc.get_traced_memory()
# tracemalloc.stop()

# print("-----------  Estrategia 1 ------------")

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


# # Estrategia 1.2

# copia_torres = copiar_torres(torres_iniciales)

# soluciones = []
# visitados = set()

# # ⏱️ Inicio de medición
# tracemalloc.start()
# inicio = time.time()

# backtracking_sin_repeticion(copia_torres, total_discos, [], soluciones, visitados)

# # ⏱️ Fin de medición
# fin = time.time()
# mem_actual, mem_pico = tracemalloc.get_traced_memory()
# tracemalloc.stop()

# print("\n-----------  Estrategia 1.2 ------------")


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

# # Estrategia 1.3

# copia_torres = copiar_torres(torres_iniciales)

# soluciones = []
# visitados = set()

# # ⏱️ Inicio de medición
# tracemalloc.start()
# inicio = time.time()

# backtracking_unica_solucion(copia_torres, total_discos, [], soluciones, visitados)

# # ⏱️ Fin de medición
# fin = time.time()
# mem_actual, mem_pico = tracemalloc.get_traced_memory()
# tracemalloc.stop()

# print("\n-----------  Estrategia 1.3 ------------")

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


# Estrategia 2

copia_torres = copiar_torres(torres_iniciales)
max_movimientos = (2 ** total_discos) + 50

soluciones = []
visitados = set()

# ⏱️ Inicio de medición
tracemalloc.start()
inicio = time.time()

backtracking_sin_visitados(torres_iniciales, total_discos, [], soluciones, max_movimientos)

# ⏱️ Fin de medición
fin = time.time()
mem_actual, mem_pico = tracemalloc.get_traced_memory()
tracemalloc.stop()

print("\n-----------  Estrategia 2 ------------")


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