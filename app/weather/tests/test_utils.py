import pytest
from app.weather.utils import get_weather_data
import requests

def test_get_weather_data_success(mocker):
    # Arrange
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'latitude': 52.52,
        'longitude': 13.41,
        'hourly': {
            'temperature_2m': [25, 26, 27] 
        },
        'timezone': 'Europe/Berlin'
    }
    mocker.patch('requests.get', return_value=mock_response)

    expected_temperature = [25, 26, 27]
    expected_timezone = 'Europe/Berlin'

    # Act
    result = get_weather_data(52.52, 13.41)

    # Assert
    assert result['hourly']['temperature_2m'] == expected_temperature
    assert result['timezone'] == expected_timezone

