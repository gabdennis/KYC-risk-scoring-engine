# src/data_loader.py
import re
import pandas as pd

REQUIRED_COLUMNS = [
    "transaction_id",
    "user_id",
    "amount",
    "transaction_type",
    "merchant_category",
    "country",
    "hour",
    "device_risk_score",
    "ip_risk_score",
    "is_fraud",
]

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [
        re.sub(r"[^a-z0-9]+", "_", col.strip().lower()).strip("_")
        for col in df.columns
    ]
    return df

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = clean_columns(df)

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    return df