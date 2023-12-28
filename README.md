# Chatbot Weather Inteligente
- SpaCy
- Scikit-learn
- Telegram

## Descripción
Este proyecto es un chatbot inteligente diseñado para interactuar con usuarios en tiempo real a través de Telegram. Utiliza Spacy para el procesamiento avanzado del lenguaje natural, permitiendo entender y responder preguntas en español. Además, está equipado con una integración a una API de clima para proporcionar actualizaciones meteorológicas y puede ser fácilmente accedido y utilizado a través de la plataforma de Telegram.

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

## Contribuir
Si deseas contribuir al proyecto, por favor haz un 'fork' del repositorio, realiza tus cambios y envía un 'pull request' para su revisión.

## Licencia
Este proyecto está bajo la Licencia Apache License.

## Autores
- Nicolás Torres - Desarrollo inicial y mantenimiento.

## Contacto
- torresnicolas@gmail.com - Para cualquier consulta o sugerencia.
