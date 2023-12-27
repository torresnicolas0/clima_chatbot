# weather_package/weather_api.py

import requests
from .config import Config
from datetime import datetime
import time
from log_config import get_logger

logger = get_logger(__name__)

class WeatherData:
    """
    Clase WeatherData para interactuar con la API de OpenWeatherMap.
    Permite obtener y procesar datos del clima para una ciudad específica.
    """
    _cache = {}    
    def __init__(self, city, api_key=Config.OW_API_KEY, units=Config.UNITS, language=Config.LANGUAGE):
        """
        Inicializa una instancia de WeatherData.

        Parámetros:
        - city (str): Nombre de la ciudad.
        - api_key (str): Clave API para OpenWeatherMap.
        - units (str): Unidades de medida para los datos del clima ('metric' o 'imperial').
        - language (str): Idioma para las respuestas de la API.
        """        
        self.city = city
        self.api_key = api_key
        self.units = units
        self.language = language
        self.data = self.get_climate()

    def build_url(self):
        """
        Construye la URL de solicitud a la API de OpenWeatherMap.

        Retorna:
        - str: URL construida para realizar la solicitud a la API.
        """
        return f"{Config.OW_URL}appid={self.api_key}&q={self.city}&units={self.units}&lang={self.language}"

    def get_climate(self):
        url = self.build_url()

        if url in WeatherData._cache:
            storage_time, storage_data = WeatherData._cache[url]
            if time.time() - storage_time < 3600:  # 3600 segundos = 1 hora (tiempo de refresco de la API)
                return storage_data

        try:
            answer = requests.get(url)
            answer.raise_for_status()
            WeatherData._cache[url] = (time.time(), answer.json())
            return answer.json()
        except requests.RequestException as e:
            logger.error(f"Error al realizar la petición a la API: {e}")
            return None
    
    @property
    def get_coordinates(self):
        try:
            return f"Longitud {self.data['coord']['lon']}, Latitud {self.data['coord']['lat']}"
        except KeyError:
            return "Error: Coordenadas no encontradas en el objeto JSON."
    @property
    def get_main_weather(self):
        try:
            id = self.data['weather'][0]['id']
            main = self.data['weather'][0]['main']
            return f"{id}"
        except (KeyError, IndexError):
            return "Error: Id no encontrada en el objeto JSON."
    @property
    def get_weather_description(self):
        try:
            description = self.data['weather'][0]['description']
            return f"{description}"
        except (KeyError, IndexError):
            return "Error: Descripción del clima no encontrada en el objeto JSON."
    @property
    def get_weather_icon(self):
        weatherIcons = {
            "01d": "☀️🌞", "01n": "🌕✨", "02d": "⛅🌤️", "02n": "🌑☁️", "03d": "☁️🌥️",
            "03n": "☁️🌙", "04d": "☁️🌧️", "04n": "☁️☁️", "09d": "🌧️💧", "09n": "🌧️🌒",
            "10d": "🌦️☔", "10n": "🌧️🌜", "11d": "⛈️🌩️", "11n": "⛈️🌌", "13d": "❄️🌨️",
            "13n": "❄️🌛", "50d": "🌫️🌁", "50n": "🌫️🌒"
        }
        try:
            icon_code = self.data['weather'][0]['icon']
            if icon_code in weatherIcons:
                icons = weatherIcons[icon_code]
                return f"{icons[0]} {icons[1]}"
            else:
                return "Icono del clima no encontrado."
        except (KeyError, IndexError):
            return "Error: Icono del clima no encontrada en el objeto JSON."
    @property
    def get_base(self):
        try:
            return f"{self.data['base']}"
        except KeyError:
            return "Error: Base no encontrada en el objeto JSON."
    @property 
    def get_main(self):
        try:
            return f"{self.data['weather'][0]['main']}"
        except (KeyError, IndexError):
            return "Error: Estado del cielo no encontrado en el objeto JSON."
    @property
    def get_temperature(self):
        try:
            return f"{self.data['main']['temp']}°C"
        except KeyError:
            return "Error: Temperatura no encontrada en el objeto JSON."
    @property
    def get_feels_like(self):
        try:
            return f"{self.data['main']['feels_like']}°C"
        except KeyError:
            return "Error: Sensación térmica no encontrada en el objeto JSON."
    @property
    def get_temperature_min(self):
        try:
            return f"{self.data['main']['temp_min']}°C"
        except KeyError:
            return "Error: Temperatura mínima no encontrada en el objeto JSON."
    @property
    def get_temperature_max(self):
        try:
            return f"{self.data['main']['temp_max']}°C"
        except KeyError:
            return "Error: Temperatura máxima no encontrada en el objeto JSON."
    @property
    def get_pressure(self):
        try:
            return f"{self.data['main']['pressure']} hPa"
        except KeyError:
            return "Error: Presión no encontrada en el objeto JSON."
    @property
    def get_humidity(self):
        try:
            return f"{self.data['main']['humidity']}%"
        except KeyError:
            return "Error: Humedad no encontrada en el objeto JSON."
    @property
    def get_visibility(self):
        try:
            visibility = self.data.get('visibility', 0)
            return f"{visibility} metros"
        except KeyError:
            return "Error: Visibilidad no encontrada en el objeto JSON."
    @property
    def get_wind_speed(self):
        try:
            return f"{self.data['wind']['speed']} metros/seg"
        except KeyError:
            return "Error: Velocidad del viento no encontrada en el objeto JSON."
    @property
    def get_wind_direction(self):
        direcciones = {
            "N": "⬆️", "NNE": "⬆️↗️", "NE": "↗️", "ENE": "➡️↗️", 
            "E": "➡️", "ESE": "➡️↘️", "SE": "↘️", "SSE": "⬇️↘️",
            "S": "⬇️", "SSW": "⬇️↙️", "SW": "↙️", "WSW": "⬅️↙️",
            "W": "⬅️", "WNW": "⬅️↖️", "NW": "↖️", "NNW": "⬆️↖️"
        }
        try:
            grados = self.data['wind']['deg']
            indice = int((grados + 11.25) / 22.5) % 16
            direccion_cardinal = list(direcciones)[indice]
            emoji = direcciones[direccion_cardinal]
            return f"{grados}° {direccion_cardinal} {emoji}"
        except KeyError:
            return "Error: Dirección del viento no encontrada en el objeto JSON."
    @property
    def get_cloudiness(self):
        try:
            return f"{self.data['clouds']['all']}%"
        except KeyError:
            return "Error: Nubosidad no encontrada en el objeto JSON."
    @property
    def get_dt(self):
        try:
            dt_timestamp = self.data['dt']
            dt_time = datetime.fromtimestamp(dt_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            return f"{dt_time}"
        except KeyError:
            return "Error: Fecha y hora de los datos no encontrada en el objeto JSON."
    @property
    def get_type(self):
        try:
            return f"{self.data['sys']['type']}"
        except KeyError:
            return "Error: Type no encontrado en el objeto JSON."
    @property
    def get_country_id(self):
        try:
            return f"{self.data['sys']['id']}"
        except KeyError:
            return "Error: Id de país no encontrado en el objeto JSON."
    @property
    def get_country(self):
        try:
            return f"{self.data['sys']['country']}"
        except KeyError:
            return "Error: País no encontrado en el objeto JSON."
    @property
    def get_sunrise_time(self):
        try:
            sunrise_timestamp = self.data['sys']['sunrise']
            sunrise_time = datetime.fromtimestamp(sunrise_timestamp).strftime('%H:%M:%S')
            return f"{sunrise_time}"
        except KeyError:
            return "Error: Hora de salida del sol no encontrada en el objeto JSON."
    @property
    def get_sunset_time(self):
        try:
            sunset_timestamp = self.data['sys']['sunset']
            sunset_time = datetime.fromtimestamp(sunset_timestamp).strftime('%H:%M:%S')
            return f"{sunset_time}"
        except KeyError:
            return "Error: Hora de puesta del sol no encontrada en el objeto JSON."
    @property
    def get_time_zone(self):
        try:
            return f"{self.data['timezone']} UTC"
        except KeyError:
            return "Error: Zona horaria no encontrada en el objeto JSON."
    @property
    def get_id(self):
        try:
            return f"{self.data['id']}"
        except KeyError:
            return "Error: Id de la ciudad no encontrada en el objeto JSON."
    @property
    def get_city_name(self):
        try:
            return f"{self.data['name']}"
        except KeyError:
            return "Error: Nombre no encontrado en el objeto JSON."
    @property
    def get_cod(self):
        try:
            return f"{self.data['cod']}"
        except KeyError:
            return "Error: Código de respuesta no encontrado en el objeto JSON."
