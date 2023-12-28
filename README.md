# Chatbot Weather Inteligente
- SpaCy
- Scikit-learn
- Telegram
## Descripción
Este proyecto es un chatbot inteligente diseñado para interactuar con usuarios en tiempo real a través de Telegram. Utiliza Spacy para el procesamiento avanzado del lenguaje natural, permitiendo entender y responder preguntas en español. Además, está equipado con una integración a una API de clima para proporcionar actualizaciones meteorológicas y puede ser fácilmente accedido y utilizado a través de la plataforma de Telegram.
## Obtención de API Keys
Para que el chatbot funcione correctamente, necesitarás obtener claves API de Telegram y de OpenWeatherMap.
### Telegram Bot API Key
Para obtener una API key de Telegram mediante BotFather:
1. **Inicia una conversación con BotFather:** Ve a Telegram y busca '@BotFather' para iniciar una conversación.
2. **Crea un nuevo bot:** Escribe `/newbot` y sigue las instrucciones. BotFather te pedirá que elijas un nombre y un nombre de usuario para tu bot.
3. **Guarda la API Key:** Una vez creado el bot, BotFather te proporcionará una token API. Esta es la API key que deberás incluir en tus variables de entorno como `TELEGRAM_TOKEN`.
### OpenWeatherMap API Key
Para obtener una API key de OpenWeatherMap:
1. **Regístrate o Inicia Sesión:** Ve al sitio web de OpenWeatherMap (https://openweathermap.org/) y crea una cuenta o inicia sesión si ya tienes una.
2. **Crea una API Key:** Navega a la sección de API y selecciona el plan gratuito. Sigue las instrucciones para generar una nueva API key.
3. **Guarda la API Key:** Una vez creada, tu API key aparecerá en tu panel de control. Guárdala para incluirla en tus variables de entorno como `OW_API_KEY`.
### Configurar las API Keys
Una vez obtenidas las claves:
- Añade las claves a tu archivo `.env` como se explicó anteriormente:
    ```plaintext
    TELEGRAM_TOKEN=your_telegram_bot_token
    OW_API_KEY=your_openweathermap_api_key
    ```
    Recuerda que estas claves son sensibles y personales. No las compartas públicamente ni las subas a repositorios de código abierto.
## Dependencias
Este proyecto requiere las siguientes herramientas y paquetes:
- **Python 3.8** o superior
- **Spacy 3.7.2**: Para procesamiento de lenguaje natural.
- **NumPy 1.26.2**: Para cálculos numéricos.
- **Pandas 2.1.4**: Para manipulación de datos.
- **Scikit-learn 1.3.2**: Para algoritmos de aprendizaje automático.
- **Python-telegram-bot 20.7**: Para la creación de bots de Telegram.
- **Requests 2.31.0**: Para realizar solicitudes HTTP.
- **Joblib 1.3.2**: Para la serialización de modelos.
- **Language-tool-python 2.7.1**: Para la corrección de texto.
- **es-core-news-sm 3.7.0**: Modelo en español para Spacy.
- **pycountry 23.12.11**: Datos de países e idiomas.
- **python-dotenv 1.0.0**: Gestión de variables de entorno.
- **ephem 4.1.5**: Cálculos astronómicos.
- **timezonefinder 6.2.0**: Determinación de zonas horarias.
Puedes instalar todas las dependencias necesarias ejecutando:
```bash
pip install -r requirements.txt
```
Instala el modelo de Spacy con:
```bash
python -m spacy download es_core_news_sm
```
### Pre-requisitos
- Tener Python 3.8 o superior instalado.
### Instalación
1. Clonar el repositorio.
2. Instalar las dependencias con `pip install -r requirements.txt`.
3. Configurar las variables de entorno necesarias en `config.py`.
4. Ejecutar `main.py` para iniciar el bot.
## Configuración del Modelo
Para que el chatbot funcione correctamente, necesita un modelo de clasificación previamente entrenado. Puedes crear el archivo `final_classification_model.pkl` siguiendo estos pasos:
1. **Posicionarse en la Raíz del Proyecto:** Asegúrate de estar en el directorio raíz del proyecto antes de ejecutar cualquier script. Esto es generalmente donde se encuentra el archivo `main.py`.
2. **Ejecutar el Script de Guardado del Modelo:** Ejecuta el siguiente comando para generar el modelo de clasificación:
    ```bash
    python model/save_model.py
    ```
       Este script procesará los datos necesarios, entrenará el modelo y lo guardará como `final_classification_model.pkl` en el directorio especificado dentro del script.
   3. **Verificar la Creación del Modelo:** Asegúrate de que el archivo `final_classification_model.pkl` se haya creado en la ubicación correcta. Este archivo es esencial para que el chatbot realice la clasificación de mensajes y responda adecuadamente.
## Uso
Después de iniciar el bot, puedes interactuar con él a través de la plataforma de Telegram. Puedes pedirle información del tiempo, realizar preguntas generales o pedir ayuda.
## Uso con GitHub Codespaces
GitHub Codespaces proporciona un entorno de desarrollo completo y configurable en la nube. Puedes usar Codespaces para configurar y ejecutar el chatbot directamente desde tu navegador, sin necesidad de configurar tu entorno local. Aquí te explicamos cómo:
### Configurar Codespaces
1. **Iniciar Codespace:** Navega al repositorio de tu proyecto en GitHub y haz clic en el botón 'Code' seguido de 'Open with Codespaces'. Luego, selecciona 'New codespace'.
2. **Espera la Preparación:** GitHub preparará un entorno de desarrollo que contiene una versión en la nube de tu repositorio con un editor de código y terminal integrados.
### Instalar Dependencias
Una vez dentro de tu Codespace:
1. **Abre la Terminal:** Encontrarás una terminal integrada en la parte inferior de la interfaz.
2. **Instalar Dependencias:** Ejecuta `pip install -r requirements.txt` para instalar todas las dependencias necesarias para el proyecto.
3. **Instalar Modelo de Spacy:** Ejecuta `python -m spacy download es_core_news_sm`.
### Configurar Variables de Entorno
1. **Crear Archivo `.env`:** Usa el editor de texto en Codespaces para crear un archivo `.env` en la raíz del proyecto y añade las claves API necesarias como se describió anteriormente.
### Ejecutar el Bot
1. **Entrenar el Modelo:** Asegúrate de haber ejecutado `python model/save_model.py` para generar `final_classification_model.pkl`.
2. **Iniciar el Bot:** Ejecuta `python main.py` para iniciar el bot.
### Acceso y Edición
- **Editar Código:** Puedes editar tu código directamente en el editor de Codespaces.
- **Acceso Persistente:** Tu Codespace se guardará y podrás regresar a él desde tu repositorio de GitHub cuando lo necesites.
Con estos pasos, puedes aprovechar GitHub Codespaces para trabajar en tu proyecto desde cualquier lugar, sin necesidad de una configuración de entorno local compleja.
## Contribuir
Si deseas contribuir al proyecto, por favor haz un 'fork' del repositorio, realiza tus cambios y envía un 'pull request' para su revisión.
## Licencia
Este proyecto está bajo la Licencia Apache License.
## Autores
- Nicolás Torres - Desarrollo inicial y mantenimiento.
## Contacto
- torresnicolas@gmail.com - Para cualquier consulta o sugerencia.
