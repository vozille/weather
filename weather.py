import requests
import json

send_url = 'http://freegeoip.net/json'
request = requests.get(send_url)
json_data = json.loads(request.text)
lat = json_data['latitude']
lon = json_data['longitude']
print(lat, lon)

params = {'latlng': {str(lat) + ',' + str(lon)}, 'sensor': 'false', 'key': 'AIzaSyBNg2yWiDaEa3lZL0yXnM9ubC-ZOPCWa7I'}
city_details = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params=params)

params = {'APPID' : '1d02acb0a01b4471272e58de491565e4', 'q': 'Cuttack'}
city_weather = requests.get('http://api.openweathermap.org/data/2.5/weather?', params=params)
print(city_weather.text)
