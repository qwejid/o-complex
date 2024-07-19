import pytest
from django.urls import reverse
from django.test import Client
from weather.models import CityWeatherRequest
from unittest.mock import patch

@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_index_get_request(client):
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert 'Введите город' in response.content.decode()

@pytest.mark.django_db
def test_index_post_request_valid_city(client):
    with patch('weather.views.get_city_coordinates') as mock_get_city_coordinates, \
         patch('weather.views.get_weather_data') as mock_get_weather_data:
        
        mock_get_city_coordinates.return_value = (40.7128, -74.0060)
        mock_get_weather_data.return_value = {
            'hourly': {
                'temperature_2m': [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
                'time': ['2024-07-19T00:00', '2024-07-19T01:00', '2024-07-19T02:00', '2024-07-19T03:00', '2024-07-19T04:00', '2024-07-19T05:00', '2024-07-19T06:00', '2024-07-19T07:00', '2024-07-19T08:00', '2024-07-19T09:00']
            }
        }
        
        response = client.post(reverse('index'), {'city': 'New York'})
        assert response.status_code == 200
        assert 'New York' in response.content.decode()
        assert CityWeatherRequest.objects.count() == 1

@pytest.mark.django_db
def test_index_post_request_invalid_city(client):
    with patch('weather.views.get_city_coordinates') as mock_get_city_coordinates:
        mock_get_city_coordinates.return_value = (None, None)
        
        response = client.post(reverse('index'), {'city': 'Invalid City'})
        assert response.status_code == 200
        assert 'City not found' in response.content.decode()

@pytest.mark.django_db
def test_city_request_count(client):
    session_key = 'test_session_key'
    client.cookies['sessionid'] = session_key

    CityWeatherRequest.objects.create(city="New York", request_count=5, session_key=session_key)
    
    response = client.get(reverse('city_request_count', kwargs={'city': 'New York'}))
    assert response.status_code == 200
    assert response.json() == {'city': 'New York', 'count': 5}

@pytest.mark.django_db
def test_history_is_unique_per_session(client):
    client1 = Client()
    client2 = Client()

    client1.cookies['sessionid'] = 'test_session_key_1'
    client2.cookies['sessionid'] = 'test_session_key_2'

    with patch('weather.utils.get_city_coordinates') as mock_get_city_coordinates, \
         patch('weather.utils.get_weather_data') as mock_get_weather_data:
        
        mock_get_city_coordinates.return_value = (40.7128, -74.0060)
        mock_get_weather_data.return_value = {
            'hourly': {
                'temperature_2m': [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
                'time': ['2024-07-19T00:00', '2024-07-19T01:00', '2024-07-19T02:00', '2024-07-19T03:00', '2024-07-19T04:00', '2024-07-19T05:00', '2024-07-19T06:00', '2024-07-19T07:00', '2024-07-19T08:00', '2024-07-19T09:00']
            }
        }
        
        # Client 1 requests data for "New York"
        client1.post(reverse('index'), {'city': 'New York'})
        
        # Client 2 requests data for "Los Angeles"
        client2.post(reverse('index'), {'city': 'Los Angeles'})

    # Verify that client 1's history only contains "New York"
    history_client1 = CityWeatherRequest.objects.filter(session_key='test_session_key_1').order_by('-last_search_date')
    assert history_client1.count() == 1
    assert history_client1.first().city == "New York"

    # Verify that client 2's history only contains "Los Angeles"
    history_client2 = CityWeatherRequest.objects.filter(session_key='test_session_key_2').order_by('-last_search_date')
    assert history_client2.count() == 1
    assert history_client2.first().city == "Los Angeles"