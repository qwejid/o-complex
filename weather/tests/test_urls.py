import pytest
from django.urls import reverse, resolve
from weather.urls import views

@pytest.mark.django_db
def test_index_url():
    path = reverse('index')
    assert resolve(path).view_name == 'index'

@pytest.mark.django_db
def test_city_request_count_url():
    path = reverse('city_request_count', kwargs={'city': 'New York'})
    assert resolve(path).view_name == 'city_request_count'

@pytest.mark.django_db
def test_index_view(client):
    response = client.get(reverse('index'))
    assert response.status_code == 200
   

@pytest.mark.django_db
def test_city_request_count_view(client):
    response = client.get(reverse('city_request_count', kwargs={'city': 'New York'}))
    assert response.status_code == 200  
