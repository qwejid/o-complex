from django.test import TestCase
from django.contrib.auth.models import User
from .models import CityWeatherRequest

class WeatherAppTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_search_history(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post('/', {'city': 'London'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(CityWeatherRequest.objects.filter(user=self.user, city='London').exists())
