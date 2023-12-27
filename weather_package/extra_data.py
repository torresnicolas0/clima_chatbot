# weather_package/extras_data.py

import pycountry
import ephem
import pytz
from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder
from log_config import get_logger

logger = get_logger(__name__)

class TimeZone:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.time_zone_info = self.get_time_zone()

    def get_time_zone(self):
        tf = TimezoneFinder()
        name = tf.timezone_at(lat=self.latitude, lng=self.longitude)
        icon = self.determine_time_zone_icon()
        return {"name": name, "icon": icon}

    def determine_time_zone_icon(self):
        if -90 <= self.longitude <= -30:
            return "🌎"
        elif -30 < self.longitude < 60:
            return "🌍"
        else:
            return "🌏"

    @property
    def get_time_zone_name(self):
        return self.time_zone_info["name"]

    @property
    def get_time_zone_icon(self):
        return self.time_zone_info["icon"]

class MoonPhase:
    def __init__(self, date, time_zone):
        self.date = date
        self.time_zone = time_zone
        self.moon_phase_info = self.get_moon_phase()

    def get_moon_phase(self):
        observer = ephem.Observer()
        observer.date = self.date.astimezone(pytz.timezone(self.time_zone))
        moon_age = observer.date - ephem.previous_new_moon(observer.date)
        return self.determine_moon_phase(moon_age)

    def determine_moon_phase(self, moon_age):
        age_days = moon_age
        if age_days < 1:
            return {"name": "Luna nueva", "icon": "🌑"}
        elif 1 <= age_days < 7:
            return {"name": "Luna creciente", "icon": "🌒"}
        elif age_days == 7:
            return {"name": "Cuarto creciente", "icon": "🌓"}
        elif 7 < age_days < 14:
            return {"name": "Luna gibosa creciente", "icon": "🌔"}
        elif age_days == 14:
            return {"name": "Luna llena", "icon": "🌕"}
        elif 14 < age_days < 21:
            return {"name": "Luna gibosa menguante", "icon": "🌖"}
        elif age_days == 21:
            return {"name": "Cuarto menguante", "icon": "🌗"}
        else:
            return {"name": "Luna menguante", "icon": "🌘"}

    @property
    def get_moon_phase_name(self):
        return f'{self.moon_phase_info["name"]}'

    @property
    def get_moon_phase_icon(self):
        return self.moon_phase_info["icon"]
    
class ExtrasData:
    def __init__(self, data):
        self.data = data
        self.lat = data['coord']['lat']
        self.lon = data['coord']['lon']
        self.temp_max = data['main']['temp_max']
        self.temp_min = data['main']['temp_min']
        self.sunrise = data['sys']['sunrise']
        self.sunset = data['sys']['sunset']
        self.country = data['sys']['country']
        self.dt = data['dt']

    @property
    def get_daylight_hours(self):
        sunrise = datetime.fromtimestamp(self.sunrise)
        sunset = datetime.fromtimestamp(self.sunset)
        return f'{str(sunset - sunrise)}'

    @property
    def get_night_hours(self):
        sunrise = datetime.fromtimestamp(self.sunrise)
        sunset = datetime.fromtimestamp(self.sunset)
        return f'{str(timedelta(hours=24) - (sunset - sunrise))}'

    def determine_season(self):
        date = datetime.fromtimestamp(self.dt)
        month = date.month
        day = date.day

        if self.lat > 0:
            if (month > 3 and month < 6) or (month == 3 and day >= 21) or (month == 6 and day < 21):
                return {"hemisphere": "Norte","name": "Primavera", "icon": "🌸"}
            elif (month > 6 and month < 9) or (month == 6 and day >= 21) or (month == 9 and day < 23):
                return {"hemisphere": "Norte","name": "Verano", "icon": "☀️"}
            elif (month > 9 and month < 12) or (month == 9 and day >= 23) or (month == 12 and day < 21):
                return {"hemisphere": "Norte","name": "Otoño", "icon": "🍂"}
            else:
                return {"hemisphere": "Norte","name": "Invierno", "icon": "❄️"}

        else:
            if (month > 3 and month < 6) or (month == 3 and day >= 21) or (month == 6 and day < 21):
                return {"hemisphere": "Sur", "name": "Otoño", "icon": "🍂"}
            elif (month > 6 and month < 9) or (month == 6 and day >= 21) or (month == 9 and day < 23):
                return {"hemisphere": "Sur", "name": "Invierno", "icon": "❄️"}            
            elif (month > 9 and month < 12) or (month == 9 and day >= 23) or (month == 12 and day < 21):
                return {"hemisphere": "Sur", "name": "Primavera", "icon": "🌸"}
            else:
                return {"hemisphere": "Sur", "name": "Verano", "icon": "☀️"}

    @property
    def get_hemisphere(self):
        return f"{self.determine_season()['hemisphere']}"
    @property
    def get_season_name(self):
        return f"{self.determine_season()['name']}"
    @property
    def get_season_icon(self):
        return self.determine_season()['icon']

    @property
    def get_country_name(self):
        country_code = self.country
        country = pycountry.countries.get(alpha_2=country_code)
        return f'{country.name if country else "Desconocido"}'

    @property
    def get_temperature_range(self):
        return f'{(self.temp_max - self.temp_min):.2f}°C'
