# main.py
import os
from src.data_loader import load_data
from src.rules_engine import calculate_rule_score
from src.scoring import assign_risk_band, assign_action

DATA_PATH = "data/synthetic_fraud_dataset.csv"
OUTPUT_PATH = "outputs/high_risk_transactions.csv"

def main():
    df = load_data(DATA_PATH)

    scores = df.apply(lambda row: calculate_rule_score(row), axis=1)
    df["rule_score"] = [s[0] for s in scores]
    df["reasons"] = [", ".join(s[1]) for s in scores]

    df["risk_band"] = df["rule_score"].apply(assign_risk_band)
    df["recommended_action"] = df["risk_band"].apply(assign_action)

    high_risk_df = df.sort_values("rule_score", ascending=False)

    os.makedirs("outputs", exist_ok=True)
    high_risk_df.to_csv(OUTPUT_PATH, index=False)

    print("Top 10 risky transactions:")
    print(
        high_risk_df[
            [
                "transaction_id",
                "user_id",
                "amount",
                "country",
                "transaction_type",
                "device_risk_score",
                "ip_risk_score",
                "rule_score",
                "risk_band",
                "recommended_action",
                "reasons",
            ]
        ].head(10)
    )

if __name__ == "__main__":
    main()