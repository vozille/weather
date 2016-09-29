import requests
import json
import signal
import gi
import time
from gi.repository import Gtk, AppIndicator3, GObject

gi.require_version('Gtk', '3.0')


# fix this location stuff

# send_url = 'http://freegeoip.net/json'
# request = requests.get(send_url)
# json_data = json.loads(request.text)
# lat = json_data['latitude']
# lon = json_data['longitude']
# print(lat, lon)
#
# params = {'latlng': {str(lat) + ',' + str(lon)}, 'sensor': 'false', 'key': 'AIzaSyBNg2yWiDaEa3lZL0yXnM9ubC-ZOPCWa7I'}
# city_details = requests.get('https://maps.googleapis.com/maps/api/geocode/json?', params=params)
# print(city_details.text)


def get_weather(city):

    params = {'APPID': '1d02acb0a01b4471272e58de491565e4', 'q': city}
    city_weather = requests.get('http://api.openweathermap.org/data/2.5/weather?', params=params)
    weather_details = json.loads(city_weather.text)
    print(weather_details)
    print(weather_details["weather"][0]["icon"])
    icon = requests.get('http://openweathermap.org/img/w/' + weather_details["weather"][0]["icon"] + '.png',
                        stream=True)
    if icon.status_code == 200:
        with open('./icon.png', 'wb') as f:
            for chunk in icon:
                f.write(chunk)
    data = {}
    data["city"] = city
    data["temp"] = str(
        round(float((weather_details["main"]["temp_max"]) + float(weather_details["main"]["temp_min"])) / 2 - 273.15, 2)
    )
    data["weather"] = weather_details["weather"][0]["description"]
    return data


class Indicator:
    def __init__(self, data):
        self.app = 'weather_app'
        iconpath = "/home/anwesh/PycharmProjects/myapps/Weather/icon.png"
        self.indicator = AppIndicator3.Indicator.new(
            self.app, iconpath,
            AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.cnt = 0
        self.indicator.set_label(data["city"] + " - " + data["temp"] + " °C, " + data["weather"], self.app)
        GObject.timeout_add(1000*15, self.refresh)

    def refresh(self):
        data = get_weather(city_lists[self.cnt])
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label(data["city"] + " - " + data["temp"] + " °C, " + data["weather"], self.app)
        return True

    def create_menu(self):
        menu = Gtk.Menu()
        # menu item 1
        item_1 = Gtk.MenuItem('')
        # item_about.connect('activate', self.about)
        menu.append(item_1)
        # separator
        menu_sep = Gtk.SeparatorMenuItem()
        menu.append(menu_sep)
        # quit
        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def quit(self, src):
        exit(0)

city_lists = ['cuttack', 'bhubaneswar', 'puri', 'bangalore', 'kolkata']
i = 1
stats = get_weather(city_lists[i])
widget = Indicator(stats)
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()



