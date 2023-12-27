# weather_package/weather.py

import datetime
from .weather_api import WeatherData
from .extra_data import ExtrasData, TimeZone, MoonPhase
from .config import Config
from log_config import get_logger

logger = get_logger(__name__)

class Weather(WeatherData):
    def __init__(self, city, api_key=Config.OW_API_KEY, units=Config.UNITS, language=Config.LANGUAGE):
        super().__init__(city, api_key, units, language)
        
        latitude = self.data['coord']['lat']
        longitude = self.data['coord']['lon']
        self.time_zone = TimeZone(latitude, longitude)

        dt = datetime.datetime.fromtimestamp(self.data['dt'])
        self.moon_phase = MoonPhase(dt, self.time_zone.get_time_zone_name)

        self.extras_data = ExtrasData(self.data)

    @property
    def get_time_zone_name(self):
        return self.time_zone.get_time_zone_name
    
    @property
    def get_time_zone_icon(self):
        return self.time_zone.get_time_zone_icon
    
    @property
    def get_moon_phase_name(self):
        return self.moon_phase.get_moon_phase_name
    
    @property
    def get_moon_phase_icon(self):
        return self.moon_phase.get_moon_phase_icon
    
    @property
    def get_daylight_hours(self):
        return self.extras_data.get_daylight_hours
    
    @property
    def get_night_hours(self):
        return self.extras_data.get_night_hours
        
    @property
    def get_hemisphere(self):
        return self.extras_data.get_hemisphere

    @property
    def get_season_name(self):
        return self.extras_data.get_season_name

    @property
    def get_season_icon(self):
        return self.extras_data.get_season_icon
    
    @property
    def get_country_name(self):
        return self.extras_data.get_country_name
    
    @property
    def get_temperature_range(self):
        return self.extras_data.get_temperature_range

    @property
    def get_temperature_response(self):
        return (
            f"Estado Actual en {self.get_city_name}, {self.extras_data.get_country_name}:\n"
            f" - Temperatura: {self.get_temperature} (Min: {self.get_temperature_min}, Max: {self.get_temperature_max})\n"
            f" - Sensación Térmica: {self.get_feels_like}\n"
            f" - Amplitud Térmica: {self.get_temperature_range}"
        )

    @property
    def get_weather_condition_response(self):
        return (
            f"{self.get_weather_icon}\n"
            f"Clima Actual en {self.get_city_name}, {self.extras_data.get_country_name}:\n"
            f" - Estado: {self.get_weather_description}\n"
            f" - Presión Atmosférica: {self.get_pressure}\n"
            f" - Humedad: {self.get_humidity}\n"
            f" - Visibilidad: {self.get_visibility}\n"
            f" - Viento: {self.get_wind_speed} en dirección {self.get_wind_direction}\n"
            f" - Nubosidad: {self.get_cloudiness}"
        )

    @property
    def get_day_night_response(self):
        return (
            f"{self.get_weather_icon}\n"
            f"Horario Solar en {self.get_city_name}, {self.extras_data.get_country_name}:\n"
            f" - Salida del Sol: {self.get_sunrise_time} Hs\n"
            f" - Puesta del Sol: {self.get_sunset_time} Hs\n"
            f" - Horas de Luz: {self.get_daylight_hours} Hs\n"
            f" - Horas de Oscuridad: {self.get_night_hours} Hs"
        )

    @property
    def get_moon_seasons_response(self):
        return (
            f"{self.get_season_icon} | {self.get_moon_phase_icon}\n"
            f"Detalles Astronómicos en {self.get_city_name}, {self.extras_data.get_country_name}:\n"
            f" - Hemisferio: {self.get_hemisphere}\n"
            f" - Estación del Año: {self.get_season_name}\n"
            f" - Fase Lunar: {self.get_moon_phase_name}"
        )

    @property
    def get_geolocation_response(self):
        return (
            f"{self.get_time_zone_icon}\n"
            f"Geolocalización de {self.get_city_name}, {self.extras_data.get_country_name}:\n"
            f" - Coordenadas: {self.get_coordinates}\n"
            f" - Zona Horaria: {self.get_time_zone_name}, {self.get_time_zone}"
        )
