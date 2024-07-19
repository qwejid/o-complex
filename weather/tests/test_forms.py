import pytest
from weather.forms import CityForm

@pytest.mark.django_db
def test_city_form_valid_data():
    form = CityForm(data={'city': 'new york'})
    assert form.is_valid()
    assert form.cleaned_data['city'] == 'New York'

@pytest.mark.django_db
def test_city_form_invalid_data():
    form = CityForm(data={'city': ''})
    assert not form.is_valid()
    assert 'city' in form.errors

@pytest.mark.django_db
def test_city_form_max_length():
    long_city_name = 'a' * 101 
    form = CityForm(data={'city': long_city_name})
    assert not form.is_valid()
    print(form.errors)
    assert 'city' in form.errors