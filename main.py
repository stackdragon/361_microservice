from flask import Flask, flash, jsonify, request
from flask_restful import Resource, Api
import requests
import configparser

app = Flask(__name__)
api = Api(app)


class WeatherZip(Resource):
    def get(self):
        zip = request.args.getlist('zip') 
        api_key = get_api_key()
        data = get_weather_results(zip[0], api_key)
        formatted_data = select_data(data)
        return jsonify(formatted_data)

class WeatherCity(Resource):
    def get(self):

        city = request.args.getlist('city') 
        country = request.args.getlist('country') 

        api_key = get_api_key()
        data = get_weather_results_name(city[0], country[0], api_key)
        formatted_data = select_data(data)
        return jsonify(formatted_data)

def select_data(data):
    city = data['name']
    lat = data['coord']['lat']
    long = data['coord']['lon']
    country = data['sys']['country']
    conditions = data['weather'][0]['main']
    temp = data['main']['temp']
    high = data['main']['temp_max']
    low = data['main']['temp_min']
    wind_speed = data['wind']['speed']
    humidity = data['main']['humidity']

    formatted_data = {'City': city, 'Country': country, 'Lat': lat, 'Long': long, 'Temp': temp, 'High_Temp': high, 'Low_Temp': low, 'Conditions': conditions, 'Humidity': humidity, 'Wind_Speed': wind_speed}
    return formatted_data

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

def get_weather_results(zip_code, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?zip={}&units=imperial&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    return r.json()

def get_weather_results_name(city_name, country, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?q={},{}&units=imperial&appid={}".format(city_name, country, api_key)
    r = requests.get(api_url)
    return r.json()

api.add_resource(WeatherZip, '/zip')
api.add_resource(WeatherCity, '/name')

if __name__ == '__main__':
    app.run(debug=True)