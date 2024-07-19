from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/request_count/<str:city>/', views.city_request_count, name='city_request_count'),
]
