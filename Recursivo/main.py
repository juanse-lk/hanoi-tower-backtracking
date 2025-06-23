## Pruebas 
import time
import tracemalloc
from ramificacion_y_poda import hanoi_backtracking as ramificacion_y_poda
from solo_poda import hanoi_backtracking as solo_poda
from solo_ramificacion import hanoi_backtracking as solo_ramificacion
from solo_backtracking import hanoi_backtracking as solo_backtracking


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
total_discos = 4
torres_iniciales = {
    "Origen": [Disco(3), Disco(2), Disco(1)],
    "Auxiliar": [],
    "Destino": []
}
# --- Prueba solo backtracking

copia_torres = copiar_torres(torres_iniciales)

soluciones = []
visitados = set()

# ⏱️ Inicio de medición
tracemalloc.start()
inicio = time.time()

solo_backtracking(copia_torres, total_discos, [], soluciones, visitados)

# ⏱️ Fin de medición
fin = time.time()
mem_actual, mem_pico = tracemalloc.get_traced_memory()
tracemalloc.stop()

print("-----------  SOLO BACKTRACKING ------------")
print(f"\n Total de soluciones encontradas: {len(soluciones)}")
print(f"\n🕒 Tiempo de ejecución: {fin - inicio:.4f} segundos")
print(f"📈 Memoria actual usada: {mem_actual / 1024:.2f} KB")
print(f"🚀 Pico de memoria: {mem_pico / 1024:.2f} KB")

# --- Prueba solo ramificacion

# copia_torres = copiar_torres(torres_iniciales)

# soluciones = []
# visitados = set()

# # ⏱️ Inicio de medición
# tracemalloc.start()
# inicio = time.time()

# solo_ramificacion(copia_torres, total_discos, [], soluciones, visitados)

# # ⏱️ Fin de medición
# fin = time.time()
# mem_actual, mem_pico = tracemalloc.get_traced_memory()
# tracemalloc.stop()

# print("\n-----------  CON RAMIFICACION ------------")
# print(f"\n Total de soluciones encontradas: {len(soluciones)}")
# print(f"\n🕒 Tiempo de ejecución: {fin - inicio:.4f} segundos")
# print(f"📈 Memoria actual usada: {mem_actual / 1024:.2f} KB")
# print(f"🚀 Pico de memoria: {mem_pico / 1024:.2f} KB")


# # --- Prueba solo poda
# copia_torres = copiar_torres(torres_iniciales)

# soluciones = []
# visitados = set()

# # ⏱️ Inicio de medición
# tracemalloc.start()
# inicio = time.time()

# solo_poda(copia_torres, total_discos, [], soluciones, visitados, [None])

# # ⏱️ Fin de medición
# fin = time.time()
# mem_actual, mem_pico = tracemalloc.get_traced_memory()
# tracemalloc.stop()

# print("\n-----------  CON PODA ------------")
# print(f"\n Total de soluciones encontradas: {len(soluciones)}")
# print(f"\n🕒 Tiempo de ejecución: {fin - inicio:.4f} segundos")
# print(f"📈 Memoria actual usada: {mem_actual / 1024:.2f} KB")
# print(f"🚀 Pico de memoria: {mem_pico / 1024:.2f} KB")


# # --- Prueba ramificacion y poda
# copia_torres = copiar_torres(torres_iniciales)

# soluciones = []
# visitados = set()

# # ⏱️ Inicio de medición
# tracemalloc.start()
# inicio = time.time()

# ramificacion_y_poda(copia_torres, total_discos, [], soluciones, visitados, [None])

# # ⏱️ Fin de medición
# fin = time.time()
# mem_actual, mem_pico = tracemalloc.get_traced_memory()
# tracemalloc.stop()


# print("\n-----------  CON RAMIFICACION Y PODA ------------")
# print(f"\n Total de soluciones encontradas: {len(soluciones)}")
# print(f"\n🕒 Tiempo de ejecución: {fin - inicio:.4f} segundos")
# print(f"📈 Memoria actual usada: {mem_actual / 1024:.2f} KB")
# print(f"🚀 Pico de memoria: {mem_pico / 1024:.2f} KB")



# # soluciones.sort(key=len, reverse=True)
# # # Mostrar soluciones
# # for i, solucion in enumerate(soluciones, 1):
# #     print(f"\n🔹 Solución {i} ({len(solucion)} movimientos):")
# #     for mov in solucion:
# #         print(f"{mov[0]} → {mov[1]} | Disco {mov[2]}")

# # print(f"\n Total de soluciones encontradas: {len(soluciones)}")