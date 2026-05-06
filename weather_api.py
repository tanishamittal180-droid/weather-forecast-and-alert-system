import requests

def get_coordinates(city):
    # Using Open-Meteo Geocoding API (no API key needed)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    response = requests.get(url)
    data = response.json()

    if "results" not in data:
        raise ValueError("City not found")

    result = data["results"][0]
    return result["latitude"], result["longitude"]


def get_weather(city):
    lat, lon = get_coordinates(city)

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,precipitation_probability"

    response = requests.get(url)
    data = response.json()

    return data