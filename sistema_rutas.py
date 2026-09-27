"""
Sistema Inteligente basado en Reglas Logicas
Proyecto: Mejor ruta en un sistema de transporte masivo

Idea del proyecto:
- Tenemos una BASE DE CONOCIMIENTO con hechos: que estaciones existen,
  a que linea pertenece cada una, y cuanto se demora entre estaciones.
- Tenemos REGLAS logicas tipo SI-ENTONCES que el programa aplica para
  saber cuando hay que hacer un transbordo (cambiar de linea).
- Con esas reglas se arma un "mapa" (grafo) de conexiones y se usa el
  algoritmo de Dijkstra para encontrar la ruta mas rapida entre el
  punto A y el punto B.

Autor(es): (escribir aqui los nombres del equipo)
"""

import heapq

# ---------------------------------------------------------
# 1) BASE DE CONOCIMIENTO (HECHOS)
# ---------------------------------------------------------
# Cada linea del sistema de transporte tiene una lista de estaciones
# en orden. Esto representa el hecho: "la estacion X esta en la linea Y".

LINEAS = {
    "Linea_Caracas": ["Portal_Norte", "Calle_100", "Calle_85", "Heroes", "Av_Jimenez"],
    "Linea_NQS": ["Portal_80", "Ricaurte", "Av_Jimenez", "Restrepo"],
    "Linea_Suba": ["Portal_Suba", "Suba_Calle_100", "Calle_85"],
}

# Hecho: tiempo en minutos entre estaciones consecutivas.
# Si un tramo no esta en la lista, se asume un tiempo por defecto.
TIEMPO_POR_DEFECTO = 3

TIEMPOS = {
    ("Portal_Norte", "Calle_100"): 5,
    ("Calle_100", "Calle_85"): 3,
    ("Calle_85", "Heroes"): 4,
    ("Heroes", "Av_Jimenez"): 4,
    ("Portal_80", "Ricaurte"): 6,
    ("Ricaurte", "Av_Jimenez"): 4,
    ("Av_Jimenez", "Restrepo"): 3,
    ("Portal_Suba", "Suba_Calle_100"): 7,
    ("Suba_Calle_100", "Calle_85"): 5,
}

# Hecho: cuantos minutos "cuesta" hacer un transbordo (cambiar de linea)
PENALIZACION_TRANSBORDO = 4


def obtener_tiempo(estacion_a, estacion_b):
    """Busca el tiempo del tramo sin importar el orden en que se escriba."""
    if (estacion_a, estacion_b) in TIEMPOS:
        return TIEMPOS[(estacion_a, estacion_b)]
    if (estacion_b, estacion_a) in TIEMPOS:
        return TIEMPOS[(estacion_b, estacion_a)]
    return TIEMPO_POR_DEFECTO


def lineas_de_la_estacion(estacion):
    """Devuelve en que lineas aparece una estacion."""
    resultado = []
    for nombre_linea, estaciones in LINEAS.items():
        if estacion in estaciones:
            resultado.append(nombre_linea)
    return resultado


# ---------------------------------------------------------
# 2) REGLAS LOGICAS (MOTOR DE INFERENCIA)
# ---------------------------------------------------------
# Regla 1: SI una estacion aparece en mas de una linea
#          ENTONCES es una estacion de transbordo.
#
# Regla 2: SI dos estaciones son consecutivas en la misma linea
#          ENTONCES se puede viajar directo entre ellas.
#
# Regla 3: SI hay que cambiar de linea en una estacion de transbordo
#          ENTONCES se suma la penalizacion de transbordo.
#
# Con estas reglas construimos un grafo. Cada nodo del grafo es una
# pareja (estacion, linea) para poder saber en que linea "va" la persona.

def construir_grafo():
    grafo = {}

    def agregar_conexion(nodo_origen, nodo_destino, costo):
        grafo.setdefault(nodo_origen, [])
        grafo[nodo_origen].append((nodo_destino, costo))

    # Regla 2: conexiones directas dentro de cada linea
    for linea, estaciones in LINEAS.items():
        for i in range(len(estaciones) - 1):
            a = estaciones[i]
            b = estaciones[i + 1]
            costo = obtener_tiempo(a, b)
            agregar_conexion((a, linea), (b, linea), costo)
            agregar_conexion((b, linea), (a, linea), costo)

    # Regla 1 + Regla 3: transbordos entre lineas en estaciones compartidas
    todas_las_estaciones = set()
    for estaciones in LINEAS.values():
        todas_las_estaciones.update(estaciones)

    for estacion in todas_las_estaciones:
        lineas_posibles = lineas_de_la_estacion(estacion)
        if len(lineas_posibles) > 1:  # Regla 1: es transbordo
            for i in range(len(lineas_posibles)):
                for j in range(len(lineas_posibles)):
                    if i != j:
                        origen = (estacion, lineas_posibles[i])
                        destino = (estacion, lineas_posibles[j])
                        agregar_conexion(origen, destino, PENALIZACION_TRANSBORDO)

    return grafo


# ---------------------------------------------------------
# 3) BUSQUEDA DE LA MEJOR RUTA (ALGORITMO DE DIJKSTRA)
# ---------------------------------------------------------
# Esta parte usa lo que dejaron listo las reglas (el grafo) para
# encontrar el camino de menor costo total (tiempo + transbordos).

def mejor_ruta(origen, destino):
    grafo = construir_grafo()

    # Nodos de partida: la estacion de origen en cada linea a la que pertenece
    distancias = {}
    padres = {}
    cola = []

    for linea in lineas_de_la_estacion(origen):
        nodo_inicial = (origen, linea)
        distancias[nodo_inicial] = 0
        heapq.heappush(cola, (0, nodo_inicial))

    nodo_final = None

    while cola:
        costo_actual, nodo = heapq.heappop(cola)

        estacion_actual, _linea_actual = nodo
        if estacion_actual == destino:
            nodo_final = nodo
            break

        for vecino, costo_tramo in grafo.get(nodo, []):
            nuevo_costo = costo_actual + costo_tramo
            if vecino not in distancias or nuevo_costo < distancias[vecino]:
                distancias[vecino] = nuevo_costo
                padres[vecino] = nodo
                heapq.heappush(cola, (nuevo_costo, vecino))

    if nodo_final is None:
        return None  # No se encontro ruta

    # Reconstruir el camino desde el final hasta el origen
    camino = [nodo_final]
    while camino[-1] in padres:
        camino.append(padres[camino[-1]])
    camino.reverse()

    return camino, distancias[nodo_final]


def mostrar_ruta(origen, destino):
    resultado = mejor_ruta(origen, destino)

    if resultado is None:
        print(f"No se encontro una ruta entre '{origen}' y '{destino}'.")
        return

    camino, costo_total = resultado

    print("\n--- MEJOR RUTA ENCONTRADA ---")
    linea_anterior = None
    for estacion, linea in camino:
        if linea_anterior is not None and linea != linea_anterior:
            print(f"  >> Transbordo en '{estacion}': cambia a la {linea}")
        print(f"  - {estacion} ({linea})")
        linea_anterior = linea

    print(f"\nTiempo total estimado: {costo_total} minutos")
    print("-----------------------------\n")


# ---------------------------------------------------------
# 4) PROGRAMA PRINCIPAL
# ---------------------------------------------------------

def main():
    print("Estaciones disponibles:")
    todas = set()
    for estaciones in LINEAS.values():
        todas.update(estaciones)
    for estacion in sorted(todas):
        print(f"  - {estacion}")

    origen = input("\nIngrese la estacion de origen (punto A): ").strip()
    destino = input("Ingrese la estacion de destino (punto B): ").strip()

    if origen not in todas or destino not in todas:
        print("Una de las estaciones ingresadas no existe. Revise el nombre e intente de nuevo.")
        return

    mostrar_ruta(origen, destino)


if __name__ == "__main__":
    main()
