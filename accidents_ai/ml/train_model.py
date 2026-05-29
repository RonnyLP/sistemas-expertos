from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.utils.class_weight import compute_class_weight
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

ROOT = Path(__file__).resolve().parent.parent.parent
CSV = ROOT / "diabetes.csv"

df = pd.read_csv(CSV, sep=";", on_bad_lines="skip")

mask_gluc1 = df["PROCEDIMIENTO_1"].str.contains("GLUCOSA", na=False)
df["glucosa"] = df["RESULTADO_1"].where(mask_gluc1, df["RESULTADO_2"])
df["colesterol"] = df["RESULTADO_2"].where(mask_gluc1, df["RESULTADO_1"])

def _target(diag):
    if "SIN MENCION" in str(diag):
        return "sin_complicacion"
    if "COMPLICACION" in str(diag):
        return "con_complicacion"
    return "otro_trastorno"

df["target"] = df["DIAGNOSTICO"].apply(_target)

df = df[["DEPARTAMENTO", "EDAD_PACIENTE", "SEXO_PACIENTE", "glucosa", "colesterol", "target"]].dropna()

X = df[["DEPARTAMENTO", "EDAD_PACIENTE", "SEXO_PACIENTE", "glucosa", "colesterol"]]
y = df["target"]

le = LabelEncoder()
y_encoded = le.fit_transform(y)
joblib.dump(le, "./label_encoder.pkl")

preprocessor = ColumnTransformer([
    ("num", StandardScaler(), ["EDAD_PACIENTE", "glucosa", "colesterol"]),
    ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), ["DEPARTAMENTO", "SEXO_PACIENTE"]),
])

X_processed = preprocessor.fit_transform(X)
joblib.dump(preprocessor, "./encoder.pkl")

X_train, X_test, y_train, y_test = train_test_split(
    X_processed, y_encoded, test_size=0.2, random_state=42
)

classes = np.unique(y_encoded)
weights = compute_class_weight("balanced", classes=classes, y=y_encoded)
class_weight = dict(zip(classes.tolist(), weights.tolist()))

model = Sequential([
    Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
    Dense(32, activation="relu"),
    Dense(16, activation="relu"),
    Dense(3, activation="softmax"),
])

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

model.fit(
    X_train,
    y_train,
    epochs=20,
    batch_size=64,
    class_weight=class_weight,
    validation_data=(X_test, y_test),
)

model.save("./model.keras")
print("Red neuronal entrenada y guardada.")
