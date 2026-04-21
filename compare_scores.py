import pandas as pd

rules_df = pd.read_csv("outputs/high_risk_transactions.csv")
ml_df = pd.read_csv("outputs/ml_scored_transactions.csv")

comparison = rules_df.merge(
    ml_df[["transaction_id", "ml_risk_score", "ml_risk_band"]],
    on="transaction_id",
    how="inner"
)

print("\n=== First 10 comparisons ===")
print(comparison[[
    "transaction_id",
    "rule_score",
    "risk_band",
    "ml_risk_score",
    "ml_risk_band",
    "is_fraud"
]].head(10))

print("\n=== Average ML risk score by rules band ===")
print(comparison.groupby("risk_band")["ml_risk_score"].mean())

comparison.to_csv("outputs/rules_vs_ml_comparison.csv", index=False)
print("\nSaved: outputs/rules_vs_ml_comparison.csv")