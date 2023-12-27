# chatbot.py

import json
import spacy
import language_tool_python
import joblib
from model.preparation_data import preprocess_question, vectorizer
from weather_package import Weather
from log_config import get_logger

logger = get_logger(__name__)

class WeatherChatbot:
    MODEL_PATH = 'model/final_classification_model.pkl'
    # NLP_MODEL = 'es_core_news_lg'
    # NLP_MODEL = 'es_core_news_md'
    NLP_MODEL = 'es_core_news_sm'
    NLP_MODEL_CUSTOM = 'model/nlp_cargado'
    CITY_FILE = 'model/names_of_cities.json'

    def __init__(self):
        self.tool = language_tool_python.LanguageTool('es')
        self.nlp = None
        self.ruler = None
        self.modelo = None
        self.city_data_list = []
        self._initialize_tools()

    def _load_cities(self):
        try:
            with open(self.CITY_FILE, 'r') as archivo:
                city_data = json.load(archivo)

            self.city_data_list = set()
            for city_info in city_data:
                main_name = city_info[0]
                if isinstance(main_name, str):
                    self.city_data_list.add(main_name.lower())
                else:
                    logger.error(f"Nombre principal de ciudad esperado como cadena, encontrado {type(main_name)}: {main_name}")

                for alt_name in city_info[1]:
                    if isinstance(alt_name, str):
                        self.city_data_list.add(alt_name.lower())
                    else:
                        logger.error(f"Nombre alternativo de ciudad esperado como cadena, encontrado {type(alt_name)}: {alt_name}")

            self.city_data_list = list(self.city_data_list)
            logger.info(f'Carga de {len(self.city_data_list)} nombres de ciudades desde "{self.CITY_FILE}". Completada.')
        except Exception as e:
            logger.error(f"Error al cargar ciudades: {e}")

    def _load_model(self):
        try:
            self.modelo = joblib.load(self.MODEL_PATH)
            logger.info(f'Carga de "{self.MODEL_PATH}". Completada.')
        except Exception as e:
            logger.error(f"Error al cargar el modelo: {e}")

    def _initialize_nlp(self):
        try:
            self.nlp = spacy.load(self.NLP_MODEL_CUSTOM)
            logger.info(f'{self.NLP_MODEL_CUSTOM} cargado exitosamente.')
            self.ruler = self.nlp.get_pipe("entity_ruler")
        except Exception:
            logger.info(f'{self.NLP_MODEL_CUSTOM} no encontrado, usando {self.NLP_MODEL} por defecto.')
            self.nlp = spacy.load(self.NLP_MODEL)
            self.ruler = self.nlp.add_pipe("entity_ruler", config={"overwrite_ents": True})
            self._load_city_patterns()
            self.nlp.to_disk(self.NLP_MODEL_CUSTOM)
            logger.info(f'{self.NLP_MODEL_CUSTOM} creado y guardado para uso futuro.')

    def _initialize_tools(self):
        self._load_model()
        self._load_cities()
        self._initialize_nlp()

    def _load_city_patterns(self):
        patterns = [{"label": "GPE", "pattern": city} for city in self.city_data_list]
        self.ruler.add_patterns(patterns)
        logger.info(f'Carga de {len(patterns)} patrones de ciudades completada.')

    def _is_city_name(self, rule):
        return any(city in rule.context.lower() for city in self.city_data_list)

    def correct_text(self, text, max_iterations=10):
        for _ in range(max_iterations):
            matches = self.tool.check(text)
            matches = [rule for rule in matches if not self._is_city_name(rule)]
            if not matches:
                break
            text = language_tool_python.utils.correct(text, matches)
        return text

    def split_into_sentences(self, corrected_text):
        doc = self.nlp(corrected_text)
        return [sent.text.strip() for sent in doc.sents]

    def classify_intent(self, text):
        processed_text = preprocess_question(text, '', self.nlp)
        vector = vectorizer.transform([processed_text])
        probability = self.modelo.predict_proba(vector)[0]
        max_probability = max(probability)
        intent_index = probability.argmax()
        intent = self.modelo.classes_[intent_index]
        return max_probability, intent

    def classify_city(self, input_text):
        starts_with_how = input_text.lower().strip().startswith(('como ', '¿como '))
        doc = self.nlp(input_text)
        cities = [ent.text.lower() for ent in doc.ents if ent.label_ == 'GPE' and ent.text.lower() not in ['como', 'sale'] and not (starts_with_how and ent.text.lower() == 'como') and ent.text.lower() in self.city_data_list]
        return cities
    
    def process_query(self, texto):
        try:
            corrected_text = self.correct_text(texto, 100)
            sentences = self.split_into_sentences(corrected_text)
            responses = []
            seen_combinations = set()
            for sentence in sentences:
                max_probabilidad, intent = self.classify_intent(sentence)
                cities = self.classify_city(sentence.lower())
                if cities:
                    if max_probabilidad < .5:
                        responses.append(f'No entiendo la pregunta "{sentence}".')
                    else:
                        for city in cities:
                            combinacion = (city, intent)
                            if combinacion not in seen_combinations:
                                weather_data = getattr(Weather(city), intent, lambda: 'Información no disponible')
                                responses.append(weather_data)
                                seen_combinations.add(combinacion)
                else:
                    responses.append(f'¿A qué ciudad te refieres en "{sentence}"?')
            return '\n\n'.join(set(responses))
        except Exception as e:
            logger.error(f"Error al analizar el texto: {e}")
            return 'Hubo un error al procesar tu solicitud, vuelve a intentarlo.'

if __name__ == "__main__":
    weather_bot = WeatherChatbot()
