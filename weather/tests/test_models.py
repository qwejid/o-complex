import pytest
from django.db.utils import IntegrityError
from weather.models import CityWeatherRequest
import time

@pytest.fixture
def city_weather_request(db):
    return CityWeatherRequest.objects.create(
        city="New York",
        request_count=5,
        session_key="test_session"
    )

@pytest.mark.django_db
def test_create_city_weather_request(city_weather_request):
    assert CityWeatherRequest.objects.count() == 1
    saved_request = CityWeatherRequest.objects.first()
    assert saved_request.city == "New York"
    assert saved_request.request_count == 5
    assert saved_request.session_key == "test_session"

@pytest.mark.django_db
def test_unique_together_constraint(city_weather_request):
    with pytest.raises(IntegrityError):
        CityWeatherRequest.objects.create(
            city="New York",
            request_count=10,
            session_key="test_session"
        )

@pytest.mark.django_db
def test_str_method(city_weather_request):
    assert str(city_weather_request) == "New York - 5 requests"

@pytest.mark.django_db
def test_auto_now_last_search_date(db):
    request = CityWeatherRequest.objects.create(
        city="Los Angeles",
        request_count=3,
        session_key="another_session"
    )
    assert request.last_search_date is not None
    previous_date = request.last_search_date
    time.sleep(1)
    request.request_count = 4
    request.save()
    assert request.last_search_date > previous_date
