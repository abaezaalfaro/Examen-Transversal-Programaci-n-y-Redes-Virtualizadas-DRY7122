import requests
import json
import sys
import os

# 🔑 Token de Mapbox
MAPBOX_TOKEN = 'pk.eyJ1IjoiYXJpZWxiYWV6YSIsImEiOiJjbTlhbmR5azkwN253MnlvZXl5a2drY2RnIn0.JrwIzUeJ048hG6kUJF75tg'

# Cargar archivo ciudades.json
ruta_json = os.path.join(os.path.dirname(__file__), 'ciudades.json')
with open(ruta_json, 'r', encoding='utf-8') as f:
    ciudades = json.load(f)

def formatear_duracion(segundos):
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segundos = int(segundos % 60)
    return f"{horas}h {minutos}m {segundos}s"

def calcular_combustible(distancia_km, consumo_km_litro):
    return distancia_km / consumo_km_litro

def obtener_datos(origen, destino):
    try:
        coord_origen = ciudades[origen]
        coord_destino = ciudades[destino]
        coords = f"{coord_origen[0]},{coord_origen[1]};{coord_destino[0]},{coord_destino[1]}"

        url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{coords}"
        params = {
            'geometries': 'geojson',
            'steps': 'true',
            'access_token': MAPBOX_TOKEN,
            'language': 'es'
        }

        response = requests.get(url, params=params)
        data = response.json()

        if 'routes' not in data or not data['routes']:
            print("No se pudo obtener una ruta válida.")
            return None, None, None

        ruta = data['routes'][0]
        distancia_km = ruta['distance'] / 1000
        duracion_s = ruta['duration']
        pasos = ruta['legs'][0]['steps']

        return distancia_km, duracion_s, pasos

    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return None, None, None

def mostrar_narrativa(pasos):
    print("\nNarrativa del viaje:")
    for paso in pasos:
        print(f"- {paso['maneuver']['instruction']}")

def elegir_transporte():
    opciones = {
        '1': ('auto', 12),
        '2': ('moto', 25)
    }
    print("\nTipos de transporte disponibles:")
    print("1. En auto")
    print("2. En moto")
    print("S. Salir")
    eleccion = input("Elige el número de transporte: ").strip().lower()
    if eleccion == 's':
        print("Saliendo del programa. ¡Buen viaje!")
        sys.exit()
    return opciones.get(eleccion, ('auto', 12))  # Default: auto

def main():
    while True:
        print("\n--- Calculadora de viaje (Mapbox) ---")
        print("Ciudades disponibles:", ", ".join(ciudades.keys()))

        origen = input("Ciudad de origen (o 's' para salir): ").strip().lower()
        if origen == 's':
            print("Saliendo del programa. ¡Buen viaje!")
            sys.exit()

        destino = input("Ciudad de destino (o 's' para salir): ").strip().lower()
        if destino == 's':
            print("Saliendo del programa. ¡Buen viaje!")
            sys.exit()

        if origen not in ciudades or destino not in ciudades:
            print("Una o ambas ciudades no están en la lista.")
            continue

        transporte_mostrar, consumo = elegir_transporte()
        distancia, duracion, pasos = obtener_datos(origen, destino)

        if distancia:
            print(f"\nTipo de transporte: {transporte_mostrar.capitalize()}")
            print(f"Distancia: {distancia:.2f} km")
            print(f"Duración estimada: {formatear_duracion(duracion)}")

            combustible = calcular_combustible(distancia, consumo)
            print(f"Consumo estimado: {combustible:.2f} litros (basado en {consumo} km/l)")

            mostrar_narrativa(pasos)

if __name__ == "__main__":
    main()
