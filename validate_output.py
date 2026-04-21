import pandas as pd

df = pd.read_csv("outputs/high_risk_transactions.csv")

print("\n==== First 10 rows of the scored transactions ====\n")
print(
    df[
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

print("\n==== Summary of risk bands ====\n")
print(df["risk_band"].value_counts())

print("\n==== Summary of recommended actions ====\n")
print(df["recommended_action"].value_counts())

print("\n==== Sample of high risk transactions ====\n")
print(
    df[df["risk_band"].isin(["High", "Severe"])][
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

print("\n==== Sample of low risk transactions ====\n")
print(
    df[df["risk_band"] == "Low"][
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

print("\n==== Top 10 most common reasons for high risk transactions ====\n")
high_risk_reasons = df[df["risk_band"].isin(["High", "Severe"])]["reasons"].str.split(", ").explode()
print(high_risk_reasons.value_counts().head(10))

print("\n==== Fraud rate by risk band ====\n")
fraud_rate_by_band = df.groupby("risk_band")["rule_score"].mean()
print(fraud_rate_by_band)

print("\n==== Average values by risk band ====\n")
avg_values_by_band = df.groupby("risk_band")[["amount", "device_risk_score", "ip_risk_score"]].mean()
print(avg_values_by_band)

print("\n==== Country distribution for high risk transactions ====\n")
high_risk_countries = df[df["risk_band"].isin(["High", "Severe"])]["country"].value_counts()
print(high_risk_countries.head(10))
