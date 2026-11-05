"""
Customer Churn Risk Predictor - live demo app.

Run from the project root:
    streamlit run app.py

The app loads the exact pipeline saved by src/train.py, so the preprocessing
and the model are the same objects that were evaluated in the report.
"""

import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "churn_model.joblib"
METRICS_PATH = BASE_DIR / "reports" / "metrics.json"
FIGURE_DIR = BASE_DIR / "reports" / "figures"

st.set_page_config(
    page_title="Churn Risk Predictor",
    page_icon=":bar_chart:",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .block-container { padding-top: 1.6rem; padding-bottom: 3rem; max-width: 1250px; }
    .hero {
        background: linear-gradient(120deg, #123B5D 0%, #2E86AB 55%, #4FB3D9 100%);
        color: white; padding: 1.6rem 2rem; border-radius: 16px;
        margin-bottom: 1.4rem;
    }
    .hero h1 { color: white; margin: 0 0 .35rem 0; font-size: 2rem; }
    .hero p { color: #E8F4FA; margin: 0; font-size: 1.02rem; }
    .risk-card {
        border-radius: 16px; padding: 1.4rem 1.6rem; color: white;
        margin-bottom: 1rem;
    }
    .risk-card .label { font-size: .95rem; opacity: .92; letter-spacing: .04em; text-transform: uppercase; }
    .risk-card .value { font-size: 3.2rem; font-weight: 800; line-height: 1.05; margin: .2rem 0; }
    .risk-card .note { font-size: .98rem; opacity: .95; }
    .gauge-track {
        width: 100%; height: 16px; background: #E6EDF3; border-radius: 999px;
        overflow: hidden; margin: .8rem 0 .3rem 0;
    }
    .gauge-fill { height: 100%; border-radius: 999px; }
    .factor {
        display: inline-block; padding: .32rem .7rem; border-radius: 999px;
        margin: .18rem .3rem .18rem 0; font-size: .88rem; font-weight: 600;
    }
    .risk-up { background: #FDE8E4; color: #B23A1E; }
    .risk-down { background: #E3F4EA; color: #1E7A46; }
    .action-card {
        background: #F7FAFC; border: 1px solid #DCE6EE; border-radius: 12px;
        padding: .85rem 1rem; margin-bottom: .6rem;
    }
    .action-card b { color: #123B5D; }
    .small-muted { color: #5C6B77; font-size: .9rem; }
    div[data-testid="stMetricValue"] { font-size: 1.65rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_artifact():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_metrics():
    with open(METRICS_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


artifact = load_artifact()
model = artifact["model"]
model_name = artifact["model_name"]
metrics = load_metrics()
feature_list = artifact["features"]

SERVICE_COLUMNS = [
    "PhoneService",
    "MultipleLines",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
]


def build_customer(
    gender,
    senior,
    partner,
    dependents,
    phone_service,
    multiple_lines,
    internet_service,
    online_security,
    online_backup,
    device_protection,
    tech_support,
    streaming_tv,
    streaming_movies,
    contract,
    paperless_billing,
    payment_method,
    tenure,
    monthly_charges,
):
    """Build one model-ready row, including the engineered features."""
    total_charges = round(monthly_charges * max(tenure, 1), 2)
    row = {
        "gender": gender,
        "SeniorCitizen": 1 if senior else 0,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone_service,
        "MultipleLines": multiple_lines,
        "InternetService": internet_service,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
        "NumServices": sum(
            1
            for value in [
                phone_service,
                multiple_lines,
                online_security,
                online_backup,
                device_protection,
                tech_support,
                streaming_tv,
                streaming_movies,
            ]
            if value == "Yes"
        ),
        "AvgMonthlySpend": round(total_charges / max(tenure, 1), 2),
        "IsNewCustomer": int(tenure <= 6),
    }
    return pd.DataFrame([row])[feature_list]


def predict_probability(customer: pd.DataFrame) -> float:
    return float(model.predict_proba(customer)[0, 1])


def risk_band(probability: float):
    if probability < 0.30:
        return "Low risk", "#1E7A46", "#E3F4EA"
    if probability < 0.60:
        return "Medium risk", "#B7791F", "#FDF3D9"
    return "High risk", "#B23A1E", "#FDE8E4"


def gauge_html(probability: float, color: str) -> str:
    return f"""
    <div class="gauge-track">
      <div class="gauge-fill" style="width: {probability * 100:.1f}%; background: {color};"></div>
    </div>
    <div class="small-muted">0% (safe) &nbsp;|&nbsp; 50% (uncertain) &nbsp;|&nbsp; 100% (certain churn)</div>
    """


# ---------------------------------------------------------------------------
# Sidebar inputs
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("Customer profile")
    st.caption("Change any field and the prediction updates instantly.")

    with st.expander("Customer details", expanded=True):
        gender = st.selectbox("Gender", ["Female", "Male"])
        senior = st.checkbox("Senior citizen", value=False)
        partner = st.selectbox("Has a partner", ["Yes", "No"])
        dependents = st.selectbox("Has dependents", ["Yes", "No"])

    with st.expander("Services", expanded=False):
        phone_service = st.selectbox("Phone service", ["Yes", "No"])
        multiple_lines = st.selectbox(
            "Multiple lines", ["No", "Yes", "No phone service"]
        )
        internet_service = st.selectbox(
            "Internet service", ["Fiber optic", "DSL", "No"]
        )
        internet_options = ["No", "Yes", "No internet service"]
        online_security = st.selectbox("Online security", internet_options)
        online_backup = st.selectbox("Online backup", internet_options)
        device_protection = st.selectbox("Device protection", internet_options)
        tech_support = st.selectbox("Tech support", internet_options)
        streaming_tv = st.selectbox("Streaming TV", internet_options)
        streaming_movies = st.selectbox("Streaming movies", internet_options)
        st.caption(
            "Note: adding a service also raises the derived NumServices feature, "
            "so the net risk change combines both effects."
        )

    with st.expander("Account and billing", expanded=True):
        contract = st.selectbox(
            "Contract type", ["Month-to-month", "One year", "Two year"]
        )
        paperless_billing = st.selectbox("Paperless billing", ["Yes", "No"])
        payment_method = st.selectbox(
            "Payment method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)",
            ],
        )
        tenure = st.slider("Tenure (months)", 0, 72, 12)
        monthly_charges = st.slider(
            "Monthly charges (USD)", 18.0, 120.0, 70.0, step=0.5
        )

    st.divider()
    st.caption(
        "Model: Logistic Regression trained on the IBM Telco Customer Churn "
        "dataset (7,043 customers)."
    )

customer = build_customer(
    gender,
    senior,
    partner,
    dependents,
    phone_service,
    multiple_lines,
    internet_service,
    online_security,
    online_backup,
    device_protection,
    tech_support,
    streaming_tv,
    streaming_movies,
    contract,
    paperless_billing,
    payment_method,
    tenure,
    monthly_charges,
)

probability = predict_probability(customer)
band, band_color, band_bg = risk_band(probability)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
      <h1>Customer Churn Risk Predictor</h1>
      <p>An end-to-end data science project: explore the data, predict who will leave,
      and explain what to do about it.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_predict, tab_performance, tab_insights, tab_method = st.tabs(
    ["Risk assessment", "Model performance", "Data insights", "How it works"]
)

# ---------------------------------------------------------------------------
# Tab 1: prediction
# ---------------------------------------------------------------------------
with tab_predict:
    left, right = st.columns([1.15, 1], gap="large")

    with left:
        st.markdown(
            f"""
            <div class="risk-card" style="background:{band_color};">
              <div class="label">Predicted churn probability</div>
              <div class="value">{probability:.1%}</div>
              <div class="note">{band} - {model_name}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(gauge_html(probability, band_color), unsafe_allow_html=True)

        if probability >= 0.60:
            st.error(
                "This customer looks likely to leave. Prioritize a retention call "
                "and consider a contract or support offer."
            )
        elif probability >= 0.30:
            st.warning(
                "This customer is at moderate risk. A proactive check-in and a "
                "service review are worthwhile."
            )
        else:
            st.success(
                "This customer looks stable. Keep the experience strong and "
                "monitor for changes."
            )

        st.markdown("#### Snapshot")
        c1, c2, c3 = st.columns(3)
        c1.metric("Tenure", f"{tenure} mo")
        c2.metric("Monthly bill", f"${monthly_charges:,.0f}")
        c3.metric("Services", f"{int(customer['NumServices'].iloc[0])}")

    with right:
        st.markdown("#### Why this score?")
        st.caption(
            "These are known risk patterns from the training data. They explain "
            "the customer's situation, not the model's internal coefficients."
        )

        factors = []
        if contract == "Month-to-month":
            factors.append(("Month-to-month contract", True))
        if tenure <= 12:
            factors.append(("New customer (under 1 year)", True))
        if internet_service == "Fiber optic":
            factors.append(("Fiber optic internet", True))
        if payment_method == "Electronic check":
            factors.append(("Pays by electronic check", True))
        if tech_support != "Yes" and internet_service != "No":
            factors.append(("No tech support", True))
        if online_security != "Yes" and internet_service != "No":
            factors.append(("No online security", True))
        if monthly_charges >= 80:
            factors.append(("High monthly bill", True))
        if contract in ("One year", "Two year"):
            factors.append(("Long-term contract", False))
        if tenure > 24:
            factors.append(("Loyal customer (2+ years)", False))
        if tech_support == "Yes":
            factors.append(("Has tech support", False))
        if online_security == "Yes":
            factors.append(("Has online security", False))
        if dependents == "Yes":
            factors.append(("Has dependents", False))

        if not factors:
            st.write("No strong risk or protective patterns detected.")
        else:
            chips = "".join(
                f'<span class="factor {"risk-up" if is_risk else "risk-down"}">'
                f'{"+" if is_risk else "-"} {label}</span>'
                for label, is_risk in factors
            )
            st.markdown(chips, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### What if we intervened?")
    st.caption(
        "The model is re-scored with one change at a time. This turns the "
        "prediction into a concrete retention playbook."
    )

    scenarios = []
    if contract == "Month-to-month":
        scenarios.append(("Offer a one-year contract", "Contract", "One year"))
        scenarios.append(("Offer a two-year contract", "Contract", "Two year"))
    if payment_method == "Electronic check":
        scenarios.append(
            ("Move to automatic credit-card payment", "PaymentMethod", "Credit card (automatic)")
        )
    if tech_support != "Yes" and internet_service != "No":
        scenarios.append(("Add tech support", "TechSupport", "Yes"))
    if online_security != "Yes" and internet_service != "No":
        scenarios.append(("Add online security", "OnlineSecurity", "Yes"))

    if not scenarios:
        st.info("This customer is already on the main protective options.")
    else:
        columns = st.columns(min(3, len(scenarios)))
        for column, (label, field, value) in zip(columns, scenarios):
            changed = customer.copy()
            changed[field] = value
            if field in ("TechSupport", "OnlineSecurity"):
                changed["NumServices"] = int(
                    (changed[SERVICE_COLUMNS] == "Yes").sum(axis=1).iloc[0]
                )
            new_probability = predict_probability(changed)
            delta = new_probability - probability
            with column:
                st.markdown(
                    f'<div class="action-card"><b>{label}</b><br>'
                    f'<span class="small-muted">New estimated risk</span><br>'
                    f'<span style="font-size:1.35rem;font-weight:700;'
                    f'color:{risk_band(new_probability)[1]};">{new_probability:.1%}</span><br>'
                    f'<span class="small-muted">{delta:+.1%} vs current</span></div>',
                    unsafe_allow_html=True,
                )

    st.caption(
        "Note: these are model-based associations, not proven causal effects. "
        "A real retention program should validate them with an A/B test."
    )

# ---------------------------------------------------------------------------
# Tab 2: model performance
# ---------------------------------------------------------------------------
with tab_performance:
    st.markdown("### How well does the model perform?")
    st.caption(
        "Evaluated on 1,409 customers the model never saw during training "
        "(20% hold-out set)."
    )

    best = metrics["best_model_metrics"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("ROC-AUC", f"{best['roc_auc']:.3f}", help="0.5 = random, 1.0 = perfect")
    c2.metric("Recall (churners caught)", f"{best['recall']:.1%}")
    c3.metric("Precision", f"{best['precision']:.1%}")
    c4.metric("F1 score", f"{best['f1']:.3f}")

    st.info(
        "**Why not just use accuracy?** 73.5% of customers stay, so a model that "
        "predicts 'everyone stays' is 73.5% accurate while catching zero churners. "
        "We optimize ROC-AUC and recall instead, because a missed churner is "
        "expensive. This model catches about 79% of customers who actually leave."
    )

    left, right = st.columns(2, gap="large")
    with left:
        st.image(str(FIGURE_DIR / "07_roc_curves.png"), use_container_width=True)
    with right:
        st.image(str(FIGURE_DIR / "09_confusion_matrix.png"), use_container_width=True)

    left, right = st.columns(2, gap="large")
    with left:
        st.image(str(FIGURE_DIR / "08_model_comparison.png"), use_container_width=True)
    with right:
        st.image(str(FIGURE_DIR / "11_probability_distribution.png"), use_container_width=True)

    st.markdown("#### What drives the predictions?")
    st.image(str(FIGURE_DIR / "10_feature_importance.png"), use_container_width=True)

    with st.expander("Full metrics for all three models"):
        rows = []
        for name, result in metrics["all_models"].items():
            rows.append(
                {
                    "Model": name,
                    "CV ROC-AUC": result["cv_roc_auc_mean"],
                    "Test ROC-AUC": result["test"]["roc_auc"],
                    "Recall": result["test"]["recall"],
                    "Precision": result["test"]["precision"],
                    "F1": result["test"]["f1"],
                    "Accuracy": result["test"]["accuracy"],
                }
            )
        st.dataframe(
            pd.DataFrame(rows).set_index("Model").style.format("{:.3f}"),
            use_container_width=True,
        )

# ---------------------------------------------------------------------------
# Tab 3: data insights
# ---------------------------------------------------------------------------
with tab_insights:
    st.markdown("### What the data told us")
    st.caption(
        "7,043 telecom customers, 21 raw columns, 26.5% churn rate. "
        "These findings shaped the features and the retention recommendations."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Customers", f"{metrics['dataset']['rows']:,}")
    c2.metric("Churn rate", f"{metrics['dataset']['churn_rate_pct']}%")
    c3.metric("Raw columns", "21")

    left, right = st.columns(2, gap="large")
    with left:
        st.image(str(FIGURE_DIR / "02_churn_by_contract.png"), use_container_width=True)
        st.markdown(
            "- **42.7%** of month-to-month customers churn, versus **2.8%** on "
            "two-year contracts.\n"
            "- Contract type is the strongest actionable lever in the dataset."
        )
    with right:
        st.image(str(FIGURE_DIR / "03_tenure_distribution.png"), use_container_width=True)
        st.markdown(
            "- Churn is concentrated in the **first year**, especially the first "
            "few months.\n"
            "- Long-tenure customers are substantially more stable."
        )

    st.image(str(FIGURE_DIR / "05_churn_drivers.png"), use_container_width=True)
    st.markdown(
        "- **Fiber optic** customers churn at 41.9%, versus 7.4% with no internet.\n"
        "- **Electronic check** payers churn at 45.3%, versus about 15-19% for "
        "automatic payment methods.\n"
        "- Customers **without tech support or online security** churn at roughly "
        "42%, versus about 15% with those services."
    )

    left, right = st.columns(2, gap="large")
    with left:
        st.image(str(FIGURE_DIR / "04_monthly_charges.png"), use_container_width=True)
    with right:
        st.image(str(FIGURE_DIR / "01_churn_balance.png"), use_container_width=True)

    with st.expander("Correlation heatmap and extra charts"):
        st.image(str(FIGURE_DIR / "06_correlation_heatmap.png"), use_container_width=True)

# ---------------------------------------------------------------------------
# Tab 4: method
# ---------------------------------------------------------------------------
with tab_method:
    st.markdown("### The pipeline, in plain English")

    steps = [
        ("1. Clean", "Fixed 11 blank TotalCharges values, converted Yes/No to 0/1, dropped the customer ID."),
        ("2. Explore", "Compared churn across contract, tenure, services, billing and charges."),
        ("3. Engineer", "Added number of services, average monthly spend and a new-customer flag."),
        ("4. Split", "80% training / 20% test, stratified so both sets keep the same churn rate."),
        ("5. Train", "Compared Logistic Regression, Random Forest and Gradient Boosting with 5-fold CV."),
        ("6. Evaluate", "Chose the best ROC-AUC, then checked recall, precision, F1 and the confusion matrix."),
        ("7. Deploy", "Saved preprocessing + model together, and served it in this Streamlit app."),
    ]
    for title, description in steps:
        st.markdown(f"**{title}.** {description}")

    st.markdown("#### Features used by the model")
    left, right = st.columns(2, gap="large")
    with left:
        st.markdown(
            "**Numeric (7)**\n"
            "- `SeniorCitizen`\n"
            "- `tenure`\n"
            "- `MonthlyCharges`\n"
            "- `TotalCharges`\n"
            "- `NumServices` (engineered)\n"
            "- `AvgMonthlySpend` (engineered)\n"
            "- `IsNewCustomer` (engineered)"
        )
    with right:
        st.markdown(
            "**Categorical (15)**\n"
            "- `gender`, `Partner`, `Dependents`\n"
            "- `PhoneService`, `MultipleLines`, `InternetService`\n"
            "- `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`\n"
            "- `StreamingTV`, `StreamingMovies`\n"
            "- `Contract`, `PaperlessBilling`, `PaymentMethod`"
        )
    st.caption(
        "Target: Churn (1 = left, 0 = stayed). Categorical fields are one-hot encoded; "
        "numeric fields are scaled. customerID was dropped."
    )
    st.info(
        "**Feature interaction to know about:** NumServices is derived from the service "
        "toggles. Adding DeviceProtection changes both DeviceProtection and NumServices, "
        "so the net effect can differ from the service's isolated effect. On its own, "
        "DeviceProtection is slightly protective in this model (odds ratio about 0.95); "
        "the extra service count is what can nudge the score up."
    )

    st.divider()
    st.markdown("#### Why Logistic Regression?")
    st.markdown(
        "It won the cross-validated ROC-AUC comparison (0.847), tied with Random "
        "Forest (0.846) and beat Gradient Boosting (0.827). It is also simple, "
        "fast, well-calibrated and easy to explain to a business audience - a rare "
        "case where the most interpretable model is also the most accurate."
    )

    st.markdown("#### Limitations")
    st.markdown(
        "- The dataset is from one telecom company and is not recent, so results "
        "may not transfer directly.\n"
        "- The model finds associations, not causes. Retention offers should be "
        "tested experimentally.\n"
        "- The 0.50 threshold is a starting point; the business should choose a "
        "threshold based on the cost of a missed churner versus a wasted offer.\n"
        "- No customer lifetime value or competitor data is included."
    )

    st.markdown("#### Next steps")
    st.markdown(
        "- Add SHAP explanations for per-customer reasoning.\n"
        "- Track model performance over time and retrain as behavior changes.\n"
        "- Run A/B tests on the retention offers suggested by the what-if tool.\n"
        "- Add customer lifetime value so retention spending is prioritized by profit."
    )
