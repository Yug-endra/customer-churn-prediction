# Customer Churn Prediction

An end-to-end data science project that predicts which telecom customers are likely to
leave, explains why, and turns the prediction into retention actions.

Built with Python, pandas, scikit-learn and Streamlit.

---

## Results at a glance

| Metric | Score | What it means |
|---|---:|---|
| ROC-AUC | **0.846** | Strong ability to rank at-risk customers above safe ones |
| Recall | **79.4%** | Catches about 4 out of 5 customers who actually churn |
| Precision | **50.6%** | About half of flagged customers would have stayed |
| F1 score | **0.618** | Balance between precision and recall |
| Accuracy | **74.0%** | Misleading here - see the note below |

The dataset is imbalanced: 73.5% of customers stayed. A model that predicts "everyone
stays" would be 73.5% accurate while catching zero churners. This model has almost the
same accuracy but catches 79.4% of churners, which is why ROC-AUC and recall are the
metrics that matter.

**Best model:** Logistic Regression (cross-validated ROC-AUC 0.847), chosen over Random
Forest (0.846) and Gradient Boosting (0.827).

---

## Quick start

Open a terminal in this folder (`D:\Internship`) and run:

```powershell
# 1. Install dependencies (already installed on this machine)
pip install -r requirements.txt

# 2. Retrain the model and regenerate every chart (optional)
python src/train.py

# 3. Launch the live demo
streamlit run app.py
```

The app opens at <http://localhost:8501>. If the port is busy, use:

```powershell
streamlit run app.py --server.port 8502
```

If you retrain the model while the app is open, restart the app so it reloads the new
`models/churn_model.joblib`.

You can also double-click `start_demo.bat`.

---

## What is in this folder

```
D:\Internship
|-- data\
|   `-- Telco-Customer-Churn.csv        Raw dataset (7,043 customers)
|-- src\
|   |-- train.py                        Full pipeline: clean -> EDA -> train -> evaluate
|   `-- make_slides.py                  Rebuilds the PowerPoint from the saved results
|-- models\
|   `-- churn_model.joblib              Saved preprocessing + model pipeline
|-- reports\
|   |-- figures\                        All charts used in the deck and app
|   |-- metrics.json                    Machine-readable results
|   |-- eda_insights.json               Key exploratory numbers
|   `-- model_report.txt                Human-readable report
|-- slides\
|   |-- Customer_Churn_Prediction_Review.pptx
|   `-- render\                         PNG preview of every slide
|-- app.py                              Streamlit live demo
|-- README.md                           This file
|-- PROJECT_REPORT.md                   Formal written report
|-- PRESENTATION_GUIDE.md               Speaking script, concepts and likely Q&A
|-- DEMO_SCRIPT.md                      One-page click-by-click demo plan
|-- requirements.txt
`-- start_demo.bat
```

---

## How the project works

1. **Clean** - Fix 11 blank `TotalCharges` values, convert `Churn` from Yes/No to 1/0,
   drop `customerID`.
2. **Explore** - Quantify churn by contract, tenure, internet service, payment method,
   support and charges.
3. **Engineer features** - Add `NumServices`, `AvgMonthlySpend` and `IsNewCustomer`.
4. **Split** - 80% training (5,634 rows) and 20% test (1,409 rows), stratified so both
   sets keep the same churn rate.
5. **Train** - Compare Logistic Regression, Random Forest and Gradient Boosting with
   stratified 5-fold cross-validation.
6. **Evaluate** - Select the best cross-validated ROC-AUC, then evaluate once on the
   held-out test set with accuracy, precision, recall, F1, ROC-AUC and a confusion matrix.
7. **Deploy** - Save preprocessing and model as one pipeline, then serve it in Streamlit.

The preprocessing steps (imputation, scaling, one-hot encoding) live **inside** the model
pipeline. That prevents data leakage and guarantees the app applies the same
transformations as training.

---

## Dataset

- **Source:** IBM Telco Customer Churn (public dataset)
- **Rows:** 7,043 customers
- **Raw columns:** 21
- **Target:** `Churn` - Yes (1) or No (0)
- **Churn rate:** 26.5%
- **Features:** demographics, subscribed services, contract type, payment method,
  monthly charges and tenure.

`TotalCharges` is stored as text in the raw file and has 11 blanks, all for customers with
tenure zero. These are converted to numbers and filled with the customer's monthly charge.

### Features used by the model

- **Numeric (7):** `SeniorCitizen`, `tenure`, `MonthlyCharges`, `TotalCharges`,
  `NumServices`, `AvgMonthlySpend`, `IsNewCustomer`.
- **Categorical (15):** `gender`, `Partner`, `Dependents`, `PhoneService`,
  `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`,
  `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`, `Contract`,
  `PaperlessBilling`, `PaymentMethod`.
- **Dropped:** `customerID`.
- **Target:** `Churn` (1 = left, 0 = stayed).

The three engineered features are `NumServices` (count of active services),
`AvgMonthlySpend` (total charges / tenure) and `IsNewCustomer` (tenure of 6 months or less).

---

## Model comparison

| Model | CV ROC-AUC | Test ROC-AUC | Recall | Precision | F1 |
|---|---:|---:|---:|---:|---:|
| **Logistic Regression** | **0.847** | **0.846** | **79.4%** | 50.6% | 0.618 |
| Random Forest | 0.846 | 0.841 | 74.1% | 54.6% | 0.629 |
| Gradient Boosting | 0.827 | 0.826 | 50.3% | 60.5% | 0.549 |

Logistic Regression is the best choice because it has the highest cross-validated ROC-AUC,
the highest recall, and is the easiest model to explain. Random Forest has a slightly
higher F1 on the test set, but it catches 5 percentage points fewer churners.

---

## The live demo

The app has four tabs:

- **Risk assessment** - Customer inputs, churn probability, risk band, contributing
  factors and a what-if panel that re-scores the customer with one change at a time.
- **Model performance** - ROC curves, confusion matrix, model comparison, probability
  distribution and feature importance.
- **Data insights** - The exploratory charts and the story behind them.
- **How it works** - The pipeline in plain English, plus limitations and next steps.

Default demo profile: month-to-month fiber customer, 12 months tenure, electronic check,
no support or security. Predicted risk is **71.3%**. Switching to a two-year contract
lowers it to **34.2%**.

---

## Important notes

- The model finds **associations, not proven causes**. The what-if panel is a discussion
  tool, not a causal guarantee. Retention offers should be validated with an A/B test.
- `NumServices` is derived from the service toggles. Adding DeviceProtection changes both its
  flag and `NumServices`, so the app can show a small net increase even though device
  protection alone is associated with lower churn (22.5% versus 39.1%). That is a feature
  interaction, not evidence that device protection causes churn.
- The 0.50 threshold is a neutral starting point. A business that values recall over
  precision can lower it.
- The dataset comes from one telecom company and is not recent, so results may not
  transfer directly to another market.
- Slide 1 and 18 already carry the corrected internship identity (Yugendra Pujari,
  Avishkarana Andhra Summer Internship, Bharat Care Life Line Foundation). Set
  `STUDENT['reg_no']` in `src/report_config.py` once a registration number is available.

For the full speaking script, plain-English concept explanations and likely reviewer
questions, open `PRESENTATION_GUIDE.md`.
