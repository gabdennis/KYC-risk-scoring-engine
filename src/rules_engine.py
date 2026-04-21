# src/rules_engine.py
def calculate_rule_score(row):
    score = 0
    reasons = []

    if row["device_risk_score"] >= 0.8:
        score += 45
        reasons.append("High device risk")

    if row["ip_risk_score"] >= 0.8:
        score += 45
        reasons.append("High IP risk")

    if row["device_risk_score"] >= 0.6 and row["ip_risk_score"] >= 0.6:
        score += 25
        reasons.append("Device and IP both elevated")

    if row["country"] == "NG":
        score += 20
        reasons.append("High-risk geography")

    if row["country"] == "TR":
        score += 8
        reasons.append("Moderate geography risk")

    if row["amount"] >= 100:
        score += 8
        reasons.append("High amount")

    if row["amount"] >= 150:
        score += 8
        reasons.append("Very high amount")

    if row["hour"] in [22, 23, 0, 1, 2, 3, 4, 5]:
        score += 6
        reasons.append("Unusual transaction hour")

    if row["transaction_type"] in ["Online", "QR"]:
        score += 6
        reasons.append("Higher-risk transaction channel")

    return min(score, 100), reasons