from django.shortcuts import render
from django.http import JsonResponse
from .models import CityWeatherRequest
from .forms import CityForm
from django.db.models import F
from django.utils.timezone import now
from datetime import datetime
from .utils import get_city_coordinates, get_weather_data


def index(request):
    weather_data = None
    search_history = None
    session_key = request.session.session_key
    if not session_key:
        request.session.save()  # Сохранение сессии, если её ключ не существует
        session_key = request.session.session_key

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']           
            lat, lon = get_city_coordinates(city)
            if lat is not None and lon is not None:
                weather_data = get_weather_data(lat, lon)
                if 'hourly' not in weather_data or 'temperature_2m' not in weather_data['hourly']:
                    weather_data = {'error': 'Неудалось получить данные о погоде'}
                else:
                    temperatures = weather_data['hourly']['temperature_2m']
                    times = weather_data['hourly']['time']
                    times = [datetime.strptime(time, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M') for time in times]

                    hourly_weather = [{'time': time, 'temperature': temp} for time, temp in zip(times[:10], temperatures[:10])] 
                    weather_data = {'hourly_weather': hourly_weather}


                    # Получение или создание записи в истории запросов
                    city_record, created = CityWeatherRequest.objects.get_or_create(
                        city=city,
                        session_key=session_key,
                        defaults={'request_count': 1, 'session_key': session_key}
                    )
                    if not created:
                        # Если запись уже существует, увеличиваем счетчик запросов
                        CityWeatherRequest.objects.filter(city=city, session_key=session_key).update(
                            request_count=F('request_count') + 1,
                            last_search_date=now()
                        )

                    # Сохранение последнего запроса в сессию
                    request.session['last_city'] = city                 
                    
            else:
                weather_data = {'error': 'City not found'}
    else:
        form = CityForm()
    
    # Получение последнего запроса из сессии
    last_city = request.session.get('last_city', None)
    if last_city:
        form = CityForm(initial={'city': last_city})

    search_history = CityWeatherRequest.objects.filter(session_key=session_key).order_by('-last_search_date')[:3]
    context = {
        'form': form,
        'weather_data': weather_data,
        'search_history': search_history,
    }
    return render(request, 'weather/index.html', context=context)


