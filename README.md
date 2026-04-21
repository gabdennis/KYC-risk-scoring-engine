# KYC Risk Scoring Engine

This a portfolio project that simulates a KYC style transaction risk scoring engine using a sythetic fraud dataset (courtsey of kaggle).

This project combines:
- A **rules-based risk engine** for transparent analyst-friendly scoring
- A **logistic regression model** for ML based fraud risk prediction
- A **cute minimalist dashboard**

## Overview

Th egoal of this project is to show how a transaction monitoring or due diligence workflow could be built using structured transaction data.

The engine scores transactions using signals such as:
- Transaction amount
- Transaction type
- Merchant category
- Country
- Hour of transaction
- Device risk score
- IP risk score

Each transaction is assigned:
- A **rules based risk score**
- A **rules bases risk band** of Low, Medium, High & Severe
- A **recommended action** of Approve, Monitor, Manual Review, Escalate

## Features

- Data loading and schema validation
- Risk band assignment and action mapping
- Streamlit dashboard with filters, charts, and case review table
  
## Project Structure
```text
kyc-risk-scoring-engine/
├── data/
│   └── synthetic_fraud_dataset.csv
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── rules_engine.py
│   ├── scoring.py
│   └── model.py
├── app/
│   └── dashboard.py
├── tests/
├── notebooks/
├── outputs/
├── requirements.txt
├── .gitignore
├── main.py
├── train_model.py
├── compare_scores.py
└── validate_output.py
```
## Results

On this synthetic dataset, the model achieved:
- ROC-AUC: 1.0
- Precision: 1.0
- Recall: 1.0
- F1 Score: 1.0

The rules engine also showed a clear increase in fraud rate across risk bands:

- Low: 9.83%
- Medium: 30.88%
- High: 62.52%
- Severe: 95.97%

## Bias Note
During validation, I found a strong country-level pattern where **NG** transactions were disproportionately assigned Severe risk and were highly associated with fraud. This is probably due to the bias within the sythetic dataset. 
