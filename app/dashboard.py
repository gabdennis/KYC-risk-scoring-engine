import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="KYC Risk Scoring Engine",
    page_icon="🛡️",
    layout="wide"
)

@st.cache_data
def load_data():
    rules_df = pd.read_csv("outputs/high_risk_transactions.csv")
    ml_df = pd.read_csv("outputs/ml_scored_transactions.csv")

    df = rules_df.merge(
        ml_df[["transaction_id", "ml_risk_score", "ml_risk_band"]],
        on="transaction_id",
        how="left"
    )
    return df

df = load_data()

st.title("KYC Risk Scoring Engine")
st.caption("Rules-based and ML-based transaction risk monitoring dashboard")

with st.expander("Project notes and limitations"):
    st.markdown("""
- This project uses a synthetic fraud dataset.
- Scores come from both a transparent rules engine and a logistic regression model.
- Country-level patterns should be interpreted carefully because synthetic data can encode unrealistic or biased relationships.
- This dashboard is for portfolio demonstration, not production compliance use.
""")

# Sidebar
st.sidebar.header("Filters")

risk_band_filter = st.sidebar.selectbox(
    "Rules Risk Band",
    ["All"] + sorted(df["risk_band"].dropna().unique().tolist())
)

ml_band_filter = st.sidebar.selectbox(
    "ML Risk Band",
    ["All"] + sorted(df["ml_risk_band"].dropna().unique().tolist())
)

country_filter = st.sidebar.selectbox(
    "Country",
    ["All"] + sorted(df["country"].dropna().unique().tolist())
)

transaction_type_filter = st.sidebar.selectbox(
    "Transaction Type",
    ["All"] + sorted(df["transaction_type"].dropna().unique().tolist())
)

min_rule_score = st.sidebar.slider("Minimum Rule Score", 0, 100, 0)
min_ml_score = st.sidebar.slider("Minimum ML Score", 0, 100, 0)

filtered_df = df.copy()

if risk_band_filter != "All":
    filtered_df = filtered_df[filtered_df["risk_band"] == risk_band_filter]

if ml_band_filter != "All":
    filtered_df = filtered_df[filtered_df["ml_risk_band"] == ml_band_filter]

if country_filter != "All":
    filtered_df = filtered_df[filtered_df["country"] == country_filter]

if transaction_type_filter != "All":
    filtered_df = filtered_df[filtered_df["transaction_type"] == transaction_type_filter]

filtered_df = filtered_df[
    (filtered_df["rule_score"] >= min_rule_score) &
    (filtered_df["ml_risk_score"] >= min_ml_score)
]

tab1, tab2, tab3 = st.tabs(["Overview", "Case Review", "Bias Check"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Transactions", f"{len(filtered_df):,}")
    col2.metric("Avg Rule Score", f"{filtered_df['rule_score'].mean():.2f}")
    col3.metric("Avg ML Score", f"{filtered_df['ml_risk_score'].mean():.2f}")
    col4.metric("Fraud Rate", f"{filtered_df['is_fraud'].mean() * 100:.2f}%")

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("Risk Band Distribution")
        band_counts = filtered_df["risk_band"].value_counts().reset_index()
        band_counts.columns = ["risk_band", "count"]

        fig_band = px.bar(
            band_counts,
            x="risk_band",
            y="count",
            color="risk_band",
            category_orders={"risk_band": ["Low", "Medium", "High", "Severe"]},
            title="Rules Risk Band Counts"
        )
        st.plotly_chart(fig_band, use_container_width=True, theme="streamlit")

    with right_col:
        st.subheader("Rules vs ML Score")
        fig_scatter = px.scatter(
            filtered_df,
            x="rule_score",
            y="ml_risk_score",
            color="risk_band",
            hover_data=["transaction_id", "country", "transaction_type", "is_fraud"],
            title="Rules Score vs ML Score"
        )
        st.plotly_chart(fig_scatter, use_container_width=True, theme="streamlit")

    st.subheader("Fraud Rate by Rules Band")
    fraud_rate_df = (
        filtered_df.groupby("risk_band")["is_fraud"]
        .mean()
        .reset_index()
    )
    fraud_rate_df["fraud_rate_pct"] = fraud_rate_df["is_fraud"] * 100

    fig_fraud = px.bar(
        fraud_rate_df,
        x="risk_band",
        y="fraud_rate_pct",
        color="risk_band",
        category_orders={"risk_band": ["Low", "Medium", "High", "Severe"]},
        title="Fraud Rate by Rules Risk Band (%)"
    )
    st.plotly_chart(fig_fraud, use_container_width=True, theme="streamlit")

with tab2:
    st.subheader("Top Risky Transactions")

    sort_option = st.selectbox(
        "Sort cases by",
        ["rule_score", "ml_risk_score", "amount"]
    )

    display_cols = [
        "transaction_id",
        "user_id",
        "amount",
        "country",
        "transaction_type",
        "merchant_category",
        "hour",
        "device_risk_score",
        "ip_risk_score",
        "rule_score",
        "risk_band",
        "ml_risk_score",
        "ml_risk_band",
        "recommended_action",
        "reasons",
        "is_fraud"
    ]

    case_df = filtered_df[display_cols].sort_values(sort_option, ascending=False)
    st.dataframe(case_df, use_container_width=True, height=500)

    csv_data = case_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download filtered cases as CSV",
        data=csv_data,
        file_name="filtered_kyc_cases.csv",
        mime="text/csv"
    )

with tab3:
    st.subheader("Country-Level Bias Check")

    country_summary = (
        filtered_df.groupby("country")
        .agg(
            transactions=("transaction_id", "count"),
            fraud_rate=("is_fraud", "mean"),
            avg_rule_score=("rule_score", "mean"),
            avg_ml_score=("ml_risk_score", "mean"),
            severe_rate=("risk_band", lambda s: (s == "Severe").mean())
        )
        .reset_index()
    )

    country_summary["fraud_rate_pct"] = country_summary["fraud_rate"] * 100
    country_summary["severe_rate_pct"] = country_summary["severe_rate"] * 100

    st.markdown(
        "Use this section to check whether one geography is being assigned disproportionately high risk or fraud rates."
    )

    st.dataframe(
        country_summary[[
            "country",
            "transactions",
            "fraud_rate_pct",
            "severe_rate_pct",
            "avg_rule_score",
            "avg_ml_score"
        ]].sort_values("severe_rate_pct", ascending=False),
        use_container_width=True
    )

    fig_country = px.bar(
        country_summary.sort_values("severe_rate_pct", ascending=False),
        x="country",
        y="severe_rate_pct",
        color="country",
        title="Severe Band Rate by Country (%)"
    )
    st.plotly_chart(fig_country, use_container_width=True, theme="streamlit")

    fig_country_fraud = px.bar(
        country_summary.sort_values("fraud_rate_pct", ascending=False),
        x="country",
        y="fraud_rate_pct",
        color="country",
        title="Fraud Rate by Country (%)"
    )
    st.plotly_chart(fig_country_fraud, use_container_width=True, theme="streamlit")

    ng_rows = country_summary[country_summary["country"] == "NG"]
    if not ng_rows.empty:
        ng_severe = ng_rows["severe_rate_pct"].iloc[0]
        ng_fraud = ng_rows["fraud_rate_pct"].iloc[0]

        st.warning(
            f"NG appears unusually concentrated: Severe rate = {ng_severe:.2f}% and Fraud rate = {ng_fraud:.2f}%. "
            "This suggests a synthetic-data bias or label shortcut that should be documented in the README."
        )