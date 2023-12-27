# model/save_model.py

import joblib

from model_adjustment import optimized_model

FINAL_MODEL_FILE = 'model/final_classification_model.pkl'

def save_model(modelo, file_name):
    joblib.dump(modelo, file_name)
    print(f"Modelo guardado como '{file_name}'")

save_model(optimized_model, FINAL_MODEL_FILE)
