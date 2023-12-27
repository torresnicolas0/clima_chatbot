# weather_package/config.py

import os
from dotenv import load_dotenv
from log_config import get_logger

logger = get_logger(__name__)

# Carga de variables de entorno
load_dotenv()

class Config:
    """
    Clase Config para almacenar la configuración necesaria para la API de OpenWeatherMap.

    Esta clase contiene atributos estáticos que definen parámetros esenciales para
    realizar solicitudes a la API, como la clave API, la URL base, las unidades de medida,
    y el idioma de las respuestas.

    Atributos:
    - OW_API_KEY (str): Clave de la API de OpenWeatherMap.
    - OW_URL (str): URL base para las solicitudes a la API de OpenWeatherMap.
    - UNITS (str): Unidades de medida para los datos del clima (por defecto: 'metric').
    - LANGUAGE (str): Idioma para las respuestas de la API (por defecto: 'es').
    """

    # Clave API de OpenWeatherMap. Debe ser reemplazada por una clave API válida obtenida del usuario.
    OW_API_KEY = os.getenv('OW_API_KEY')

    # URL base para las solicitudes a la API de OpenWeatherMap.
    OW_URL = "http://api.openweathermap.org/data/2.5/weather?"

    # Unidades de medida para los datos del clima.
    # Opciones disponibles: 'metric' (Celsius), 'imperial' (Fahrenheit), o 'standard' (Kelvin).
    UNITS = 'metric'

    # Idioma para las respuestas de la API.
    # El idioma se configura según el código de idioma (por ejemplo, 'es' para español).
    LANGUAGE = 'es'

    """
    Nota importante:
    La clave API (OW_API_KEY) debe mantenerse segura y no debe ser compartida públicamente.
    Es recomendable obtener esta clave desde una variable de entorno o un archivo de configuración
    externo en un entorno de producción para mantener la seguridad.
    """
