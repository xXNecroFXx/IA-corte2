"""
base_conocimiento.py
---------------------
Aqui van los HECHOS del sistema experto: que estaciones existen,
a que linea pertenece cada una, y cuanto tiempo hay entre ellas.

Estos son los datos que el motor de reglas y el buscador de rutas
van a usar. Si quieres usar datos reales de tu ciudad, solo tienes
que modificar los diccionarios de aqui abajo.
"""

# Hecho: cada linea tiene una lista de estaciones en orden.
LINEAS = {
    "Linea_Caracas": ["Portal_Norte", "Calle_100", "Calle_85", "Heroes", "Av_Jimenez"],
    "Linea_NQS": ["Portal_80", "Ricaurte", "Av_Jimenez", "Restrepo"],
    "Linea_Suba": ["Portal_Suba", "Suba_Calle_100", "Calle_85"],
}

# Hecho: tiempo en minutos entre estaciones consecutivas.
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

# Hecho: tiempo por defecto si un tramo no esta en el diccionario TIEMPOS.
TIEMPO_POR_DEFECTO = 3

# Hecho: cuantos minutos "cuesta" hacer un transbordo (cambiar de linea).
PENALIZACION_TRANSBORDO = 4
