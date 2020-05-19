import requests

from webapp.config import WEATHER_API_KEY, WEATHER_DEFAULT_CITY
from flask import current_app

def weather_by_city(city_name):
    weather_url = 'http://api.worldweatheronline.com/premium/v1/weather.ashx'
    params = {
        "key": current_app.config['WEATHER_API_KEY'],
        "q": current_app.config['WEATHER_DEFAULT_CITY'],
        "format": "json",
        "num_of_days": 5,
        "lang": "ru"
    }
    try:
        res = requests.get(weather_url, params=params)
        res.raise_for_status()
        weather = res.json()
        if 'data' in weather:
            if 'current_condition' in weather['data']:
                try:
                    return weather['data']['current_condition'][0]
                except (IndexError, TypeError):
                    return False
    except (requests.RequestException, ValueError):
        print('Network error')
        return False
    return False

if __name__ == '__main__':
    w = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    print(w)
