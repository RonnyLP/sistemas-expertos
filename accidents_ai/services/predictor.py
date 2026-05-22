import pandas as pd
import joblib

from tensorflow.keras.models import load_model

model = load_model("accidents_ai/ml/model.keras")

encoder = joblib.load(
    "accidents_ai/ml/encoder.pkl"
)


def predict_survival(data):

    df = pd.DataFrame([data])

    X = encoder.transform(df)

    prediction = model.predict(X)[0][0]

    return prediction
