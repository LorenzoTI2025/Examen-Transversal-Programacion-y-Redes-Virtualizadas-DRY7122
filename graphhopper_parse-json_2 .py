import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "c1b13d09-5fdd-485c-9a5a-7ae20c16439d"

def geocoding(location, key):
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get("hits"):
            lat = data["hits"][0]["point"]["lat"]
            lng = data["hits"][0]["point"]["lng"]
            return lat, lng
    return None, None

def get_route(lat1, lng1, lat2, lng2, vehicle, key):
    url = route_url + urllib.parse.urlencode({
        "point": [f"{lat1},{lng1}", f"{lat2},{lng2}"],
        "vehicle": vehicle,
        "locale": "es",
        "instructions": "true",
        "key": key
    }, doseq=True)

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "paths" in data:
            path = data["paths"][0]
            km = path["distance"] / 1000
            millas = km * 0.621371
            duracion_seg = path["time"] / 1000
            horas = int(duracion_seg // 3600)
            minutos = int((duracion_seg % 3600) // 60)
            segundos = int(duracion_seg % 60)
            instrucciones = path["instructions"]
            return km, millas, horas, minutos, segundos, instrucciones
    return None, None, None, None, None, []

def main():
    print("🗺️  Calculadora de ruta entre ciudades de Chile y Perú")
    print("💡 Escribe 's' en cualquier momento para salir\n")

    while True:
        origen = input("Ingrese la ciudad de origen (ej. Santiago): ").strip()
        if origen.lower() == "s":
            break

        destino = input("Ingrese la ciudad de destino (ej. Lima): ").strip()
        if destino.lower() == "s":
            break

        print("Seleccione medio de transporte:")
        print("1. auto (car)")
        print("2. bicicleta (bike)")
        print("3. caminando (foot)")
        vehiculo_input = input("Opción [1-3]: ")
        if vehiculo_input.lower() == "s":
            break

        vehiculos = {"1": "car", "2": "bike", "3": "foot"}
        vehiculo = vehiculos.get(vehiculo_input, "car")  # por defecto car

        lat1, lng1 = geocoding(origen, key)
        lat2, lng2 = geocoding(destino, key)

        if lat1 is None or lat2 is None:
            print("❌ No se pudo geocodificar alguna ciudad. Intente de nuevo.\n")
            continue

        km, millas, h, m, s, instrucciones = get_route(lat1, lng1, lat2, lng2, vehiculo, key)

        if km is None:
            print("❌ No se pudo obtener la ruta. Intente otra combinación.\n")
            continue

        print(f"\n📍 De {origen} a {destino}")
        print(f"🚗 Distancia: {km:.2f} km / {millas:.2f} millas")
        print(f"⏱️  Duración: {h}h {m}m {s}s")
        print(f"\n🧭 Instrucciones del viaje:\n")

        for i, paso in enumerate(instrucciones, 1):
            print(f"{i}. {paso['text']} ({paso['distance']:.0f} m)")

        print("\n✅ Ruta completada.\n")

if __name__ == "__main__":
    main()
