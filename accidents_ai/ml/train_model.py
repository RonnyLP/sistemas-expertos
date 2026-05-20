import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# cargar csv
df = pd.read_csv("./titanic.csv")

# eliminar nulos
df = df.dropna()

# X e y
X = df.drop("survived", axis=1)
y = df["survived"]

# columnas
numeric_features = [
    "age",
    "n_siblings_spouses",
    "parch",
    "fare"
]

categorical_features = [
    "sex",
    "class",
    "deck",
    "embark_town",
    "alone"
]

# preprocessing
preprocessor = ColumnTransformer([
    (
        "num",
        StandardScaler(),
        numeric_features
    ),
    (
        "cat",
        OneHotEncoder(),
        categorical_features
    )
])

X_processed = preprocessor.fit_transform(X)

# guardar preprocessor
joblib.dump(preprocessor, "./encoder.pkl")

# split
X_train, X_test, y_train, y_test = train_test_split(
    X_processed,
    y,
    test_size=0.2,
    random_state=42
)

# modelo
model = Sequential([
    Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(16, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# entrenar
model.fit(
    X_train,
    y_train,
    epochs=20,
    batch_size=16
)

# guardar
model.save("./model.keras")

print("Modelo entrenado")
