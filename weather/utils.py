from geopy.geocoders import Nominatim
import requests

def get_weather_data(lat, lon):
    params = {
        'latitude': lat,
        'longitude': lon,
        'forecast_hours': 24,  # Запрашиваем данные на 24 часа вперед
        'hourly': 'temperature_2m',  # Запрашиваем температуру
        'timezone': 'auto'  # Автоматическое определение временной зоны
    }
    url = "https://api.open-meteo.com/v1/forecast"
    response = requests.get(url, params=params)
    return response.json()

def get_city_coordinates(city):
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city)
    if location:
        return location.latitude, location.longitude
    return None, None