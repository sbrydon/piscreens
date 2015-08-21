import requests
import feedparser


class Weather(object):
    def __init__(self, data):
        self.location = data['name']
        self.description = data['weather'][0]['description']
        self.temp = data['main']['temp']
        self.humidity = data['main']['humidity']
        self.wind_speed = data['wind']['speed']


class Headline(object):
    def __init__(self, data):
        self.title = data['title']
        self.summary = data['summary']


class WeatherService(object):
    def __init__(self, api_key, lat, lon):
        self.api_key = api_key
        self.lat = lat
        self.lon = lon

    # TODO: Exception handling!
    def get_current_weather(self):
        url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {
            'APPID': self.api_key,
            'lat': self.lat,
            'lon': self.lon,
            'units': 'metric'
        }

        response = requests.get(url, params=params)
        return Weather(response.json())


class NewsService(object):
    # TODO: Exception handling!
    def get_current_headlines(self):
        url = 'http://feeds.bbci.co.uk/news/rss.xml'

        response = requests.get(url)
        parsed = feedparser.parse(response.content)
        return [Headline(item) for item in parsed['entries'][:10]]
