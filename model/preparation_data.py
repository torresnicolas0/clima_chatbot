# model/preparacion_datos.py

import json
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import numpy as np

# nlp = spacy.load('es_core_news_sm')
# nlp = spacy.load('es_core_news_md')
# nlp = spacy.load('es_core_news_lg')
nlp = spacy.load('model/nlp_cargado')

keyword_files = {
    'get_temperature_response':       'model/keyword/temperature_response.json',
    'get_weather_condition_response': 'model/keyword/weather_condition_response.json',
    'get_day_night_response':         'model/keyword/day_night_response.json',
    'get_moon_seasons_response':      'model/keyword/moon_seasons_response.json',
    'get_geolocation_response':       'model/keyword/geolocation_response.json'
}
files_questions = {
    'get_temperature_response':       'model/questions/temperature_response.json',
    'get_weather_condition_response': 'model/questions/weather_condition_response.json',
    'get_day_night_response':         'model/questions/day_night_response.json',
    'get_moon_seasons_response':      'model/questions/moon_seasons_response.json',
    'get_geolocation_response':       'model/questions/geolocation_response.json'
}

def load_data(file_name):
    with open(file_name, 'r', encoding="utf8") as file:
        datos = json.load(file)
    return datos

def preprocess_question(question, keywords_intention, nlp):
    doc = nlp(question)
    processed_words = []
    for token in doc:
        if not token.is_stop and token.is_alpha:
            processed_words.append(token.lemma_)
            if token.text in keywords_intention:
                processed_words.append(token.lemma_)
    return ' '.join(processed_words)

vectorizer = CountVectorizer()
X = []
y = []

for intention, file_questions in files_questions.items():
    preguntas = load_data(file_questions)
    keywords_intention = load_data(keyword_files[intention])
    for question in preguntas:
        processed_question = preprocess_question(question, keywords_intention, nlp)
        X.append(processed_question)
        y.append(intention)

vectores = vectorizer.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(vectores, np.array(y), test_size=0.2, random_state=42)
