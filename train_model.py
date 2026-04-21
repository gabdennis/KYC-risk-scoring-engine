import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score

from src.data_loader import load_data
from src.model import build_model, FEATURES, TARGET
from src.scoring import assign_risk_band

DATA_PATH = "data/synthetic_fraud_dataset.csv"
MODEL_PATH = "outputs/logistic_model.joblib"
SCORED_OUTPUT_PATH = "outputs/ml_scored_transactions.csv"
METRICS_OUTPUT_PATH = "outputs/model_metrics.csv"

def main():
    df = load_data(DATA_PATH)

    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    model = build_model()
    model.fit(X_train, y_train)

    y_proba = model.predict_proba(X_test)[:, 1]
    y_pred = (y_proba >= 0.5).astype(int)

    metrics = pd.DataFrame([{
        "model": "logistic_regression",
        "roc_auc": roc_auc_score(y_test, y_proba),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1": f1_score(y_test, y_pred, zero_division=0),
    }])

    os.makedirs("outputs", exist_ok=True)
    metrics.to_csv(METRICS_OUTPUT_PATH, index=False)

    df["ml_risk_score"] = model.predict_proba(df[FEATURES])[:, 1] * 100
    df["ml_risk_score"] = df["ml_risk_score"].round(2)
    df["ml_risk_band"] = df["ml_risk_score"].apply(assign_risk_band)

    df.to_csv(SCORED_OUTPUT_PATH, index=False)
    joblib.dump(model, MODEL_PATH)

    print("Training complete.")
    print(metrics)
    print(f"Saved model to: {MODEL_PATH}")
    print(f"Saved scored data to: {SCORED_OUTPUT_PATH}")
    print(f"Saved metrics to: {METRICS_OUTPUT_PATH}")

if __name__ == "__main__":
    main()