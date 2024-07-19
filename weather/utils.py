from geopy.geocoders import Nominatim
import requests
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

def get_weather_data(lat, lon):
    params = {
        'latitude': lat,
        'longitude': lon,
        'forecast_hours': 24,  # Запрашиваем данные на 24 часа вперед
        'hourly': 'temperature_2m',  # Запрашиваем температуру
        'timezone': 'auto'  # Автоматическое определение временной зоны
    }
    url = "https://api.open-meteo.com/v1/forecast"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Это выбросит исключение при ошибках HTTP
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        raise http_err
    except requests.exceptions.RequestException as err:        
        raise SystemExit(err) from err
    

def get_city_coordinates(city):  
    geolocator = Nominatim(user_agent="weather_app")
    try:
        location = geolocator.geocode(city)
        if location:
            return location.latitude, location.longitude
        return None, None
    except (GeocoderTimedOut, GeocoderServiceError) as e:        
        print(f"Error while geocoding city '{city}': {e}")
        return None, None
    except Exception as e:        
        print(f"Unexpected error: {e}")
        return None, None

