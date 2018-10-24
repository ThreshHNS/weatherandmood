import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ru&appid=af6b64750bf392c94ec8ff16e6b2d41a'

    cities = City.objects.all()

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    data_weather = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city,
            'country' : r['sys']['country'],
            'location' : f"{r['coord']['lon']} , {r['coord']['lat']}",
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        print(city_weather.get('location'))
        data_weather.append(city_weather)

    context = {
        'data_weather': data_weather,
        'form': form,
    }
    return render(request, 'weather/weather.html', context)
