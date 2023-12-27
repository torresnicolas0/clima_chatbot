# model/model_adjustment.py

from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib
import numpy as np

from preparation_data import X_train, X_test, y_train, y_test

OPTIMIZED_MODEL_FILE = 'model/optimized_classification_model.pkl'

def model_adjustment(X_train, y_train, X_test, y_test):
    better_alpha = 0
    better_precision = 0
    better_model = None

    for alpha in np.arange(0.0, 1.1, 0.1):
        model = MultinomialNB(alpha=alpha)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        precision = accuracy_score(y_test, y_pred)

        print(f"Probando alpha={alpha}: Precisión = {precision}")

        if precision > better_precision:
            better_alpha = alpha
            better_precision = precision
            better_model = model

    print(f"\nMejor alpha: {better_alpha} con una precisión de: {better_precision}")
    return better_model

optimized_model = model_adjustment(X_train, y_train, X_test, y_test)

joblib.dump(optimized_model, OPTIMIZED_MODEL_FILE)
