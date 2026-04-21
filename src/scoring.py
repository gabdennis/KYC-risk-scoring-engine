# src/scoring.py
def assign_risk_band(score: float) -> str:
    if score <= 24:
        return "Low"
    elif score <= 49:
        return "Medium"
    elif score <= 74:
        return "High"
    return "Severe"

def assign_action(risk_band: str) -> str:
    actions = {
        "Low": "Approve",
        "Medium": "Monitor",
        "High": "Manual Review",
        "Severe": "Escalate"
    }
    return actions[risk_band]