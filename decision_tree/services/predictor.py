import pickle

import numpy as np
import pandas as pd

_BASE = "decision_tree/ml"

with open(f"{_BASE}/dt_model.pkl", "rb") as f:
    _model = pickle.load(f)

with open(f"{_BASE}/dt_encoder.pkl", "rb") as f:
    _encoder = pickle.load(f)

with open(f"{_BASE}/dt_label_encoder.pkl", "rb") as f:
    _label_encoder = pickle.load(f)


def predict_severity(data: dict) -> tuple[str, float]:
    df = pd.DataFrame([{
        "DEPARTAMENTO": data["departamento"],
        "SEXO_PACIENTE": data["sexo"],
        "EDAD_PACIENTE": data["edad"],
        "glucosa": data["glucosa"],
        "colesterol": data["colesterol"],
    }])
    X = _encoder.transform(df)
    probs = _model.predict_proba(X)[0]
    class_idx = int(np.argmax(probs))
    class_name = _label_encoder.inverse_transform([class_idx])[0]
    confidence = float(probs[class_idx])
    return class_name, confidence
