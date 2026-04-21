# src/model.py
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression

FEATURES = [
    "amount",
    "transaction_type",
    "merchant_category",
    "country",
    "hour",
    "device_risk_score",
    "ip_risk_score",
]

TARGET = "is_fraud"

NUM_COLS = ["amount", "hour", "device_risk_score", "ip_risk_score"]
CAT_COLS = ["transaction_type", "merchant_category", "country"]

def build_model():
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", Pipeline([
                ("imputer", SimpleImputer(strategy="median"))
            ]), NUM_COLS),
            ("cat", Pipeline([
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("encoder", OneHotEncoder(handle_unknown="ignore"))
            ]), CAT_COLS),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))
        ]
    )

    return model