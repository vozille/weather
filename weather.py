import requests
import json
import signal
import gi
from gi.repository import Gtk, AppIndicator3, GObject

gi.require_version('Gtk', '3.0')


# add error handling

def get_city():
    send_url = 'http://freegeoip.net/json'
    try:
        request = requests.get(send_url)
        if request.status_code == 200:
            json_data = json.loads(request.text)
            lat = json_data["latitude"]
            long = json_data["longitude"]
            return json_data["city"]
        else:
            return None
    except requests.ConnectionError:
        return None


def get_weather():
    city = get_city()
    # no internet
    if city is None:
        print('no internet connection')
        with open('./data.txt') as file:
            data = json.load(file)
        return data

    try:
        params = {'APPID': '1d02acb0a01b4471272e58de491565e4', 'q': city.lower(), 'units' : 'metric'}
        city_weather = requests.get('http://api.openweathermap.org/data/2.5/weather?', params=params)
        # internet connection lost midway
        if city_weather.status_code == 200:
            weather_details = json.loads(city_weather.text)
            print(weather_details)
            icon = requests.get('http://openweathermap.org/img/w/' + weather_details["weather"][0]["icon"] + '.png',
                                stream=True)
            if icon.status_code == 200:
                with open('./icon.png', 'wb') as f:
                    for chunk in icon:
                        f.write(chunk)
            data = dict()
            data["city"] = city
            data["temp"] = str(
                round(float((weather_details["main"]["temp_max"]) + float(weather_details["main"]["temp_min"])) / 2, 2)
            )
            data["weather"] = weather_details["weather"][0]["description"]
            data["humidity"] = str(weather_details["main"]["humidity"])
            with open('./data.txt', 'w') as file:
                json.dump(data, file)

            return data
        else:
            print('no internet connection')
            with open('./data.txt') as file:
                data = json.load(file)
                return data
    except requests.ConnectionError:
        print('we lost internet connection')
        with open('./data.txt') as file:
            data = json.load(file)
            return data


class Indicator:
    def __init__(self, data):
        self.app = 'weather_app'
        iconpath = "/home/anwesh/PycharmProjects/myapps/Weather/icon.png"
        self.indicator = AppIndicator3.Indicator.new(
            self.app, iconpath,
            AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu(data))
        self.indicator.set_label(data["city"] + " - " + data["temp"] + " °C", self.app)
        GObject.timeout_add(1000*60, self.refresh)

    def refresh(self):
        data = get_weather()
        self.indicator.set_menu(self.create_menu(data))
        self.indicator.set_label(data["city"] + " - " + data["temp"] + " °C", self.app)
        return True

    def create_menu(self, data):
        menu = Gtk.Menu()
        # menu item 1
        item_1 = Gtk.MenuItem('today: '+data["weather"])
        menu.append(item_1)
        item_2 = Gtk.MenuItem('humidity: '+data["humidity"]+'%')
        menu.append(item_2)
        menu_sep = Gtk.SeparatorMenuItem()
        menu.append(menu_sep)

        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def quit(self, src):
        exit(0)


def main():
    stats = get_weather()
    widget = Indicator(stats)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    Gtk.main()


if __name__ == '__main__':
    main()
