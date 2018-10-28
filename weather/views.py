import requests
from django.shortcuts import render
from datetime import datetime
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q={}&units=metric&lang=ru&cnt=7&appid=af6b64750bf392c94ec8ff16e6b2d41a'

    cities = City.objects.all()

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()

    form = CityForm()

    data_weather = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        weekday = [datetime.fromtimestamp(int(r['list'][i]['dt'])) for i in range(7)]

        try:
            wind_deg = int((r['list'][0]['deg'] / 22.5) + .5)
            arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                   "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
            wind_dir = arr[(wind_deg % 16)]
        except KeyError:
            wind_dir = "No Window"

        city_weather = {
            'city': city,
            'location' : f"{r['city']['coord']['lon']} , {r['city']['coord']['lat']}",
            'temperature' : [int(r['list'][i]['temp']['day']) for i in range(7)],
            'night': [int(r['list'][i]['temp']['night']) for i in range(7)],
            'humidity': r['list'][0]['humidity'],
            'wind': r['list'][0]['speed'],
            'icon' : [r['list'][i]['weather'][0]['icon'] for i in range(7)], 
            'wind_dir': wind_dir
        }

        data_weather.append(city_weather)
    context = {
        'data_weather' : data_weather,
        'form' : form,
        'weekday' : weekday,
    }
    return render(request, 'weather/index.html', context)

