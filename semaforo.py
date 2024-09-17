import threading
import time
from threading import Semaphore

# Variables compartidas
buffer = []
buffer_size = 5
counter = 1  # Contador para números secuenciales

# Semáforos contadores
empty = Semaphore(buffer_size)  # Número de espacios vacíos
full = Semaphore(0)  # Número de espacios llenos

# Mutex
mutex = threading.Lock()

def productor():
    global counter
    while True:
        empty.acquire()  # Esperar un espacio vacío
        mutex.acquire()  # Entrada a la sección crítica
        buffer.append(counter)  # Añadir el número secuencial al buffer
        print(f"Productor produjo: {counter}")
        counter += 1  # Incrementar el contador
        mutex.release()  # Salir de la sección crítica
        full.release()  # Incrementar los espacios llenos
        time.sleep(1)  # Simular el tiempo de producción

def consumidor(id):
    while True:
        full.acquire()  # Esperar un espacio lleno
        mutex.acquire()  # Entrada a la sección crítica
        item = buffer.pop(0)  # Consumir un ítem del buffer
        print(f"Consumidor {id} consumió: {item}")
        mutex.release()  # Salir de la sección crítica
        empty.release()  # Incrementar los espacios vacíos
        time.sleep(2)  # Simular el tiempo de consumo

# Inicialización de hilos
productor_thread = threading.Thread(target=productor)
consumidor_threads = [threading.Thread(target=consumidor, args=(i,)) for i in range(3)]

# Ejecución
productor_thread.start()
for thread in consumidor_threads:
    thread.start()
