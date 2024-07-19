# test_utils.py
import pytest
import requests
import responses
from weather.utils import get_weather_data

# Используем pytest.mark.parametrize для проверки различных сценариев
@pytest.mark.parametrize(
    "lat, lon, mock_response, expected",
    [
        (40.7128, -74.0060, {'temperature_2m': [22]}, {'temperature_2m': [22]}),  # Пример успешного ответа
        (34.0522, -118.2437, {'temperature_2m': [25]}, {'temperature_2m': [25]}), # Другой успешный ответ
    ]
)
@responses.activate
def test_get_weather_data(lat, lon, mock_response, expected):
    # Мокаем ответ от API
    url = "https://api.open-meteo.com/v1/forecast"
    responses.add(
        responses.GET,
        url,
        json=mock_response,
        status=200
    )
    
    # Вызываем функцию
    result = get_weather_data(lat, lon)
    
    # Проверяем результат
    assert result == expected

@pytest.mark.parametrize(
    "lat, lon, status_code, mock_response",
    [
        (40.7128, -74.0060, 500, {'error': 'Server error'}),  # Пример ответа с ошибкой сервера
        (34.0522, -118.2437, 404, {'error': 'Not found'})    # Пример ответа с ошибкой 404
    ]
)
@responses.activate
def test_get_weather_data_errors(lat, lon, status_code, mock_response):
    # Мокаем ответ от API
    url = "https://api.open-meteo.com/v1/forecast"
    responses.add(
        responses.GET,
        url,
        json=mock_response,
        status=status_code
    )
    
    # Проверяем, что функция корректно обрабатывает ошибки
    with pytest.raises(requests.exceptions.HTTPError):
        get_weather_data(lat, lon)


from unittest.mock import Mock
from weather.utils import get_city_coordinates

# Тест успешного получения координат
def test_get_city_coordinates_success(mocker):
    # Создаем мок объекта location
    mock_location = Mock()
    mock_location.latitude = 40.7128
    mock_location.longitude = -74.0060

    # Мокаем метод geocode
    mock_geolocator = mocker.patch('geopy.geocoders.Nominatim.geocode', return_value=mock_location)
    
    # Вызываем тестируемую функцию
    lat, lon = get_city_coordinates("New York")

    # Проверяем результат
    assert lat == 40.7128
    assert lon == -74.0060
    mock_geolocator.assert_called_once_with("New York")

# Тест неуспешного получения координат
def test_get_city_coordinates_failure(mocker):
    # Мокаем метод geocode, чтобы возвращать None
    mocker.patch('geopy.geocoders.Nominatim.geocode', return_value=None)
    
    # Вызываем тестируемую функцию
    lat, lon = get_city_coordinates("Unknown City")
    
    # Проверяем результат
    assert lat is None
    assert lon is None

# Тестирование обработки исключений
def test_get_city_coordinates_exception(mocker):
    # Мокаем метод geocode, чтобы выбрасывать исключение
    mocker.patch('geopy.geocoders.Nominatim.geocode', side_effect=Exception("Geocoding error"))
    
    # Вызываем тестируемую функцию и проверяем, что она корректно обрабатывает исключение
    lat, lon = get_city_coordinates("City With Exception")
    
    # Проверяем результат
    assert lat is None
    assert lon is None
