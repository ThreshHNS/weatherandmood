        for weather in weather_info:
            try:
                wind_deg = int((weather.time / 22.5) + .5)
                arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                       "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
                wind_dir = arr[(wind_deg % 16)]
            except KeyError:
                wind_dir = "No Window"

            city_weather = {
                'city': city.name,
                'country': city.country,
                'location': city.location,
                'temperature': weather.time,
                'night': weather.temperature_night,
                'wind': weather.wind,
                'wind_dir': wind_dir
            }
            data_weather.append(city_weather)
