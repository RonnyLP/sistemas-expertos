import pickle
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from sklearn.tree import DecisionTreeClassifier, plot_tree

ROOT = Path(__file__).resolve().parent.parent.parent
CSV = ROOT / "diabetes.csv"
OUT = Path(__file__).parent

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

X = df[["DEPARTAMENTO", "SEXO_PACIENTE", "EDAD_PACIENTE", "glucosa", "colesterol"]]
y = df["target"]

le = LabelEncoder()
y_encoded = le.fit_transform(y)

preprocessor = ColumnTransformer([
    ("cat", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1), ["DEPARTAMENTO", "SEXO_PACIENTE"]),
    ("num", "passthrough", ["EDAD_PACIENTE", "glucosa", "colesterol"]),
])

X_processed = preprocessor.fit_transform(X)

model = DecisionTreeClassifier(
    criterion="entropy",
    class_weight="balanced",
    max_depth=5,
    random_state=42,
)
model.fit(X_processed, y_encoded)

print(f"Accuracy (train): {100 * model.score(X_processed, y_encoded):.1f}%")

with open(OUT / "dt_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open(OUT / "dt_encoder.pkl", "wb") as f:
    pickle.dump(preprocessor, f)
with open(OUT / "dt_label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

# Guardar visualización del árbol
feature_names = ["Departamento", "Sexo", "Edad", "Glucosa (mg/dL)", "Colesterol (mg/dL)"]
class_names = le.classes_.tolist()

fig, ax = plt.subplots(figsize=(28, 12))
plot_tree(
    model,
    feature_names=feature_names,
    class_names=class_names,
    filled=True,
    rounded=True,
    fontsize=8,
    ax=ax,
)
fig.tight_layout()
fig.savefig(OUT / "tree.png", dpi=100, bbox_inches="tight")
plt.close(fig)

print("Árbol entrenado, guardado y visualización generada.")
