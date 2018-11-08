# -*- coding: utf-8 -*-
import requests
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import City, Weather
from .forms import CityForm


def index(request):
    
    # Url to OpenWeatherMap API
    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q={}&units=metric&lang=ru&cnt=7&appid=af6b64750bf392c94ec8ff16e6b2d41a'

    # Query to City() for all objects
    cities = City.objects.all()

    # Adding city from user to our datebase
    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            addcity = City()
            addcity.name = form.cleaned_data['name']
            r = requests.get(url.format(form.cleaned_data['name'])).json()
            addcity.country = r['city']['country']
            addcity.location = f"{r['city']['coord']['lat']}, {r['city']['coord']['lon']}"
            addcity.save()
            return HttpResponseRedirect("/")

    else: #request.method == "GET"
        form = CityForm()

    # List with sorted weather
    data_weather = []

    # For each city in all objects of City() model (datebase)
    for city in cities:
        # Query to OpenWeatherMap Api
        r = requests.get(url.format(city)).json()

        # Weekday parser [Mon, Tue etc.]
        weekday = [datetime.fromtimestamp(
            int(r['list'][i]['dt'])) for i in range(7)]

        # For each elemnt in JSON parse date to Weather() model (datebase)
        for item in r['list']:

            # Weekday parser [Mon, Tue etc.]
            weekday = [datetime.fromtimestamp(
            int(r['list'][i]['dt'])) for i in range(7)]

            weather = Weather()

            # Calculating a wind direction with deg of response from OpenWeatherMap
            try:
                wind_deg = int((item['deg'] / 22.5) + .5)
                arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                       "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
                wind_dir = arr[(wind_deg % 16)]
            except KeyError:
                wind_dir = "No Window"

            # Adding weathers to our datebase
            try:
                obj = Weather.objects.get(
                    city=city, time=datetime.fromtimestamp(item['dt']))
            except Weather.DoesNotExist:
                weather.city = city
                weather.time = datetime.fromtimestamp(item['dt'])
                weather.temp = int(item['temp']['day'])
                weather.night = int(item['temp']['night'])
                weather.humidity = item['humidity']
                weather.wind = item['speed']
                weather.direction = wind_dir
                weather.icon = item['weather'][0]['icon'].replace("n", 'd')

                weather.save()

        # Query to database for elements with our current city in for
        weathers = Weather.objects.all().filter(city=city)

        # Sorted dict of weather for each city
        city_weather = {
            'city': city.name,
            'country': city.country,
            'location': city.location,
            'temperature': [weathers[i].temp for i in range(7)],
            'night': [weathers[i].night for i in range(7)],
            'humidity': weathers[0].humidity,
            'wind': weathers[0].wind,
            'icon': [weathers[i].icon for i in range(7)],
            'wind_dir': wind_dir
        }

        # Adding @city_weather to list with sorted weathers
        data_weather.append(city_weather)

    # Argument for rendering with weathers, form to add city and day of the week.
    context = {
        'data_weather': data_weather,
        'form': form,
        'weekday': weekday,
    }
    return render(request, 'weather/index.html', context)
