from django.db import models

class CityWeatherRequest(models.Model):
    city = models.CharField(max_length=100)
    request_count = models.IntegerField(default=0)
    last_search_date = models.DateTimeField(auto_now=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)

    class Meta:
        unique_together = ('city', 'session_key')
    def __str__(self):
        return f"{self.city} - {self.request_count} requests"

