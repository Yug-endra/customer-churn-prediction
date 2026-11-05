"""Chapters 1 to 6 of the internship report."""

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from report_config import APP_SHOTS, ASSETS, DECK_FIGURES, EDA, FIGURES, METRICS, STUDENT
from report_style import (
    BLUE,
    GRAY,
    NAVY,
    caption,
    body,
    bullet,
    chapter,
    code_block,
    figure,
    numbered,
    section,
    subsection,
    table,
)

BEST = METRICS["best_model_metrics"]
ALL = METRICS["all_models"]
DATASET = METRICS["dataset"]


# ---------------------------------------------------------------------------
# 1. INTRODUCTION
# ---------------------------------------------------------------------------
def chapter_1(doc):
    chapter(doc, 1, "INTRODUCTION")

    body(
        doc,
        (
            "Telecommunications is one of the most competitive subscription industries in the "
            "world. Customers can compare tariffs in minutes, switch providers without visiting a "
            "store, and bundle or unbundle services as their needs change. In this environment, "
            "acquiring a new customer is considerably more expensive than retaining an existing "
            "one, and a single percentage point of avoidable churn can translate into a large "
            "amount of recurring revenue. Retention is therefore no longer only a customer-service "
            "concern; it is a core commercial capability that depends on the ability to anticipate "
            "which customers are about to leave and to act before they do."
        ),
    )
    body(
        doc,
        (
            f"This report documents the design, implementation and evaluation of a **Customer "
            f"Churn Prediction** system completed during a 45-day Data Science internship under "
            f"the **{STUDENT['programme']}**, hosted by **{STUDENT['organisation']}** in "
            f"association with **ZERO P4 Poverty**. The system uses the publicly available IBM "
            f"Telco Customer Churn dataset, compares three classification algorithms, selects the "
            f"most suitable model on cross-validated performance, and exposes the result through an "
            f"interactive Streamlit application that a retention team can use without writing code."
        ),
    )

    section(doc, "1.1", "Background and Motivation")
    body(
        doc,
        (
            "Every subscription business maintains a record of its relationship with each customer: "
            "how long the customer has been with the company, which services are active, how much "
            "is paid each month, which contract has been signed and how the bill is settled. "
            "Individually these fields are operational data. Collectively they describe behaviour, "
            "and behaviour carries signal. A customer on a month-to-month contract who pays by "
            "electronic check, has been with the company for three months and has never contacted "
            "technical support is not a random customer; that combination is statistically much "
            "more likely to end in cancellation than a two-year customer with automatic payment and "
            "a long tenure."
        ),
    )
    body(
        doc,
        (
            "Traditional reporting answers the question *what happened*. A churn dashboard that "
            "shows last month's cancellations is useful for accounting, but it cannot prevent the "
            "next cancellation. Predictive analytics changes the question from *what happened* to "
            "*what is likely to happen*, and then to *what should we do about it*. A supervised "
            "machine learning model learns the relationship between customer attributes and the "
            "observed churn outcome, and applies that relationship to current customers. The output "
            "is a probability, not a verdict. Customers can then be ranked, and retention resources "
            "can be concentrated on the segment where the expected benefit is highest."
        ),
    )
    body(
        doc,
        (
            "The motivation for this project is practical. Retention teams usually have limited "
            "capacity: a call centre can contact only a few hundred customers per week, and every "
            "retention offer has a cost. A model that identifies the highest-risk customers with "
            "reasonable precision allows the team to spend that capacity where it matters. An "
            "explanation of why each customer is at risk allows the team to choose an appropriate "
            "intervention - a contract upgrade, a service review, a payment-method change or a "
            "goodwill credit - instead of applying the same discount to everyone."
        ),
    )

    section(doc, "1.2", "Problem Statement")
    body(
        doc,
        (
            "The host organisation and its partners work with communities and enterprises that "
            "depend on sustained participation. In a commercial subscription setting, the problem "
            "can be stated precisely: given a customer's demographic, account, service and billing "
            "attributes at a point in time, estimate the probability that the customer will cancel "
            "the service in the near future, and present that estimate in a form that supports a "
            "retention decision."
        ),
    )
    body(doc, "The project addresses four specific sub-problems:")

    numbered(
        doc,
        [
            "**Data preparation.** The raw dataset contains a numeric field stored as text, "
            "missing values and an imbalanced target. The data must be cleaned and transformed "
            "without leaking information from the test set.",
            "**Model selection.** Several algorithms can model a binary outcome. The project must "
            "compare them under a fair protocol and choose a model that performs well on customers "
            "it has never seen.",
            "**Evaluation.** Accuracy is misleading when only about one in four customers churns. "
            "The evaluation must focus on ranking quality (ROC-AUC) and on the proportion of "
            "churners that are actually caught (recall), while reporting precision and F1 as "
            "trade-off indicators.",
            "**Deployment and explanation.** A model that exists only in a notebook has limited "
            "value. The result must be packaged into an application that accepts customer details, "
            "returns a risk score, explains the main contributing factors and allows a what-if "
            "analysis of retention scenarios.",
        ],
        size=12,
        space_after=5,
    )

    section(doc, "1.3", "Objectives")
    body(doc, "The objectives of the internship project are as follows:")
    objectives = [
        "To understand the business meaning of customer churn and the cost structure that makes retention economically important.",
        "To perform a structured data-quality audit and clean the Telco Customer Churn dataset reproducibly.",
        "To explore the data visually and quantify the relationship between contract, tenure, charges, services and churn.",
        "To engineer a small number of interpretable features that capture service breadth, spending behaviour and customer maturity.",
        "To build a leakage-free preprocessing and modelling pipeline using scikit-learn.",
        "To train and compare Logistic Regression, Random Forest and Gradient Boosting with stratified cross-validation.",
        "To evaluate the selected model on a held-out test set using accuracy, precision, recall, F1, ROC-AUC and PR-AUC.",
        "To interpret the model using permutation importance and connect the results to retention practice.",
        "To deploy the model in an interactive Streamlit application with a risk score, factor explanation and what-if simulator.",
        "To document the work in a professional internship report and present it to an academic and industry audience.",
    ]
    for item in objectives:
        bullet(doc, item, size=12, space_after=4)

    section(doc, "1.4", "Scope and Delimitations")
    body(
        doc,
        (
            "The scope of the project is a single-tabular, binary classification problem using "
            "historical customer records. The model predicts whether a customer will churn, not "
            "when the customer will churn. It does not use text, call transcripts, network "
            "telemetry, social media activity or competitor pricing, because those sources are not "
            "part of the public dataset. The model is intended as a decision-support tool; it does "
            "not automate cancellations, pricing or contract decisions."
        ),
    )
    body(
        doc,
        (
            "The dataset is a cross-sectional snapshot rather than a longitudinal event log. As a "
            "result, the model cannot capture the effect of a retention campaign that has already "
            "been run, nor can it account for seasonality. These limitations are discussed in "
            "Chapter 11."
        ),
    )

    section(doc, "1.5", "Dataset Overview")
    body(
        doc,
        (
            f"The IBM Telco Customer Churn dataset contains **{DATASET['rows']:,} customers** and "
            f"**21 columns**. Each row represents one customer at the time the snapshot was taken. "
            f"The target column, `Churn`, records whether the customer left. The dataset is "
            f"imbalanced: **1,869 customers (26.5%) churned**, while 5,174 (73.5%) stayed. The "
            f"columns can be grouped as shown in Table 1.1."
        ),
    )
    table(
        doc,
        ["Group", "Attributes", "Type", "Example"],
        [
            ["Identity", "customerID", "Text", "7590-VHVEG"],
            ["Demographics", "gender, SeniorCitizen, Partner, Dependents", "Categorical / binary", "Female, 0, Yes, No"],
            ["Account", "tenure, Contract, PaperlessBilling, PaymentMethod", "Numeric / categorical", "1 month, Month-to-month, Yes, Electronic check"],
            ["Services", "PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies", "Categorical", "Yes, No, Fiber optic"],
            ["Billing", "MonthlyCharges, TotalCharges", "Numeric", "29.85, 29.85"],
            ["Target", "Churn", "Binary", "Yes / No"],
        ],
        widths=[1.0, 3.0, 1.2, 1.3],
        font_size=8.5,
        first_col_bold=True,
        cap="Table 1.1: Structure of the Telco Customer Churn dataset",
    )
    body(
        doc,
        (
            "The dataset is widely used in churn research and teaching because it combines "
            "demographic, contractual and behavioural variables in a realistic proportions. It is "
            "small enough to train on a laptop, yet rich enough to demonstrate a complete machine "
            "learning workflow. Chapter 9 describes the audit and preparation of the data in "
            "detail."
        ),
    )

    section(doc, "1.6", "Contributions of the Project")
    body(doc, "The project makes the following practical contributions:")
    numbered(
        doc,
        [
            "A reproducible data-cleaning and feature-engineering pipeline that can be re-run from the raw CSV with a single command.",
            "An honest model comparison using stratified five-fold cross-validation and a held-out test set that is never used for model selection.",
            "A selected model with a documented operating threshold and an explicit discussion of the precision-recall trade-off.",
            "A permutation-importance analysis that identifies the variables a retention team should monitor.",
            "A deployed Streamlit application with a live risk score, a factor explanation, a what-if simulator, a model-performance view and a data-insights view.",
            "A written record of the methodology, results and limitations suitable for academic review and for handover to a future intern.",
        ],
        size=12,
        space_after=5,
    )

    section(doc, "1.7", "Organisation of the Report")
    body(
        doc,
        (
            "The remainder of the report is organised as follows. **Chapter 2** traces the history "
            "of churn analysis and the technologies used. **Chapter 3** defines churn and the "
            "machine learning concepts that the project relies on. **Chapter 4** presents the system "
            "architecture. **Chapter 5** discusses applications of the solution. **Chapter 6** "
            "describes the technologies used. **Chapter 7** lists advantages and disadvantages. "
            "**Chapter 8** states the hardware, software and data requirements. **Chapter 9** "
            "explains the methodology and includes selected source code. **Chapter 10** presents the "
            "results and output screenshots. **Chapter 11** concludes the report and outlines future "
            "work. **Chapter 12** lists the references consulted."
        ),
    )


# ---------------------------------------------------------------------------
# 2. HISTORY
# ---------------------------------------------------------------------------
def chapter_2(doc):
    chapter(doc, 2, "HISTORY")

    body(
        doc,
        (
            "Churn analysis did not begin with machine learning. It emerged from the commercial "
            "pressures of deregulated telecommunications markets, matured through the data-mining "
            "wave of the 1990s, and was transformed by the open-source scientific computing stack "
            "in the 2010s. Understanding this history explains why churn models look the way they "
            "do today and why certain metrics, particularly recall and ROC-AUC, have become standard "
            "in retention analytics."
        ),
    )

    section(doc, "2.1", "The Emergence of Customer Retention in Telecommunications")
    body(
        doc,
        (
            "For much of the twentieth century, telephone service was delivered by state-owned or "
            "regulated monopolies. Customers had little choice, and churn was a minor operational "
            "issue. The deregulation of telecommunications in the United States in the 1980s, "
            "followed by similar reforms in Europe and Asia, created competitive markets with "
            "multiple long-distance and mobile carriers. Switching became possible, tariffs became "
            "visible, and acquisition costs rose sharply. Carriers responded by building customer "
            "databases and by tracking cancellation rates as a key performance indicator."
        ),
    )
    body(
        doc,
        (
            "Early retention practice was largely reactive and rule-based. A customer who had not "
            "renewed a contract was contacted; a customer who complained repeatedly was escalated. "
            "As billing systems became computerised in the 1980s and 1990s, carriers accumulated "
            "detailed records of usage, payment and service calls. This data made it possible to "
            "move from intuition to statistical segmentation, and the first churn scorecards were "
            "built using logistic regression on a small number of account variables."
        ),
    )

    section(doc, "2.2", "From Descriptive Reporting to Predictive Modelling")
    body(
        doc,
        (
            "The 1990s saw the emergence of data mining as a discipline. Decision trees, neural "
            "networks and logistic regression were applied to customer databases in banking, "
            "insurance and telecommunications. The landmark work of Berry and Linoff on data mining "
            "techniques, and the development of the CRISP-DM process model in 1996, gave "
            "practitioners a shared vocabulary for business understanding, data preparation, "
            "modelling, evaluation and deployment. Churn prediction became a standard case study in "
            "both academic research and commercial analytics."
        ),
    )
    body(
        doc,
        (
            "A second wave arrived with ensemble methods. Random Forests, introduced by Leo Breiman "
            "in 2001, combined many decision trees to reduce variance and improved predictive "
            "accuracy on tabular data. Gradient boosting machines, developed by Jerome Friedman in "
            "the same period, built trees sequentially to correct previous errors and became the "
            "dominant approach in many competitions. These methods are now available in mature "
            "open-source libraries such as scikit-learn, XGBoost and LightGBM, which brought "
            "high-quality modelling to ordinary analysts."
        ),
    )
    body(
        doc,
        (
            "Despite the sophistication of modern algorithms, logistic regression remains a "
            "strong baseline for churn. It is fast, stable, interpretable and often competitive "
            "when the relationship between features and the log-odds of churn is approximately "
            "linear. This project treats it as a serious candidate rather than a token baseline, "
            "and the results in Chapter 10 show why."
        ),
    )

    section(doc, "2.3", "The Rise of the Open-Source Data Science Stack")
    body(
        doc,
        (
            "Python was created by Guido van Rossum in 1991 as a general-purpose language "
            "emphasising readability. Its adoption for scientific computing accelerated after "
            "NumPy (2006) and pandas (2008) provided efficient arrays and data frames. "
            "scikit-learn, released in 2007 by David Cournapeau and later maintained by a broad "
            "community, unified model selection, preprocessing and evaluation under a consistent "
            "API. Matplotlib and Seaborn made publication-quality visualisation accessible, while "
            "Jupyter notebooks changed the way analysts explored data."
        ),
    )
    body(
        doc,
        (
            "Streamlit, launched in 2019, lets a Python script become an interactive web "
            "application without front-end code, lowering the barrier between analysis and use."
        ),
    )

    section(doc, "2.4", "History of the Telco Customer Churn Dataset")
    body(
        doc,
        (
            "The dataset used in this project was published by IBM as a sample dataset for "
            "analytics education. It represents a fictional telecommunications company with 7,043 "
            "customers in California and contains demographic information, subscribed services, "
            "contract details, billing information and a churn label. Because it is synthetic but "
            "realistic, it has become one of the most widely used benchmarks for binary "
            "classification with mixed numerical and categorical features."
        ),
    )
    body(
        doc,
        (
            "The dataset's popularity has both benefits and risks. The benefit is comparability: "
            "many published analyses provide context for the results obtained here. The risk is "
            "overfitting to a well-known benchmark. For that reason, this project emphasises "
            "methodological discipline - a fixed train/test split, cross-validation on the training "
            "set only, and a clear separation between model selection and final evaluation - rather "
            "than chasing a leaderboard score."
        ),
    )

    section(doc, "2.5", "The Internship Context")
    body(
        doc,
        (
            f"The project was carried out during a **45-day Data Science internship** under the "
            f"**{STUDENT['programme']}**, hosted by **{STUDENT['organisation']}** in association "
            f"with **ZERO P4 Poverty**. The programme's structure - an independent project with "
            f"periodic reviews - mirrors professional analytics work: the intern defines the "
            f"problem, prepares the data, builds and validates the model, and communicates the "
            f"result to a non-technical audience. The certificate of achievement was issued on "
            f"**{STUDENT['issue_date']}** and is reproduced in the front matter of this report."
        ),
    )
    body(
        doc,
        (
            "The choice of a churn project was deliberate. Churn is a problem that connects "
            "statistics, software engineering and business communication. It requires the analyst "
            "to reason about class imbalance and evaluation metrics, to write clean and "
            "reproducible code, and to explain a probability in language that a retention manager "
            "can act on. These are precisely the competencies that the internship aimed to develop."
        ),
    )


# ---------------------------------------------------------------------------
# 3. DEFINITION
# ---------------------------------------------------------------------------
def chapter_3(doc):
    chapter(doc, 3, "DEFINITION")

    body(
        doc,
        (
            "This chapter defines the central concepts used throughout the report. It begins with "
            "the business definition of churn, distinguishes its different forms, and then "
            "translates the business problem into a machine learning formulation. The evaluation "
            "metrics are defined mathematically so that the results in Chapter 10 can be read "
            "without ambiguity."
        ),
    )

    section(doc, "3.1", "Customer Churn")
    body(
        doc,
        (
            "**Customer churn**, also called customer attrition, is the loss of a customer who "
            "stops using a company's product or service. In a contractual setting, churn is "
            "observed when a subscription is cancelled or not renewed. In a non-contractual "
            "setting, such as retail banking or e-commerce, churn is inferred from a prolonged "
            "absence of activity. The Telco dataset is contractual: the `Churn` column explicitly "
            "records whether the customer left the company."
        ),
    )
    body(
        doc,
        (
            "Churn is usually expressed as a rate over a defined period. The overall churn rate in "
            "the dataset is 26.5%, calculated as the number of customers who left divided by the "
            "total number of customers. This aggregate figure conceals large differences between "
            "segments: the churn rate is 42.7% for month-to-month customers but only 2.8% for "
            "customers on two-year contracts. Segment-level rates are therefore more useful for "
            "management than a single company-wide number."
        ),
    )

    section(doc, "3.2", "Types of Churn")
    body(doc, "Retention analysts distinguish several forms of churn:")
    bullet(
        doc,
        "**Voluntary churn.** The customer actively cancels or does not renew. This is the form "
        "recorded in the Telco dataset and the form that retention campaigns can influence.",
    )
    bullet(
        doc,
        "**Involuntary churn.** The customer is lost because of payment failure, fraud or credit "
        "action rather than a deliberate decision. It is often addressed through billing recovery "
        "rather than predictive modelling.",
    )
    bullet(
        doc,
        "**Partial churn.** The customer remains but reduces usage or drops some services. It is "
        "an early warning signal and often precedes full churn.",
    )
    bullet(
        doc,
        "**Silent churn.** The customer remains formally subscribed but stops engaging. In "
        "non-contractual businesses this is the dominant form and requires an activity-based "
        "definition.",
    )
    bullet(
        doc,
        "**Seasonal churn.** Cancellations concentrated in a particular period, such as the end of "
        "an academic year or a promotional cycle. It should be separated from structural churn.",
        space_after=8,
    )
    body(
        doc,
        (
            "The project models voluntary churn at the customer level. This is the most actionable "
            "definition for a telecom operator because the customer's decision is preceded by "
            "observable account and service characteristics."
        ),
    )

    section(doc, "3.3", "Key Terms")
    table(
        doc,
        ["Term", "Definition"],
        [
            ["Churn", "Loss of a customer who stops using the product or service."],
            ["Churn rate", "Number of customers lost in a period divided by the customers at risk at the start of the period."],
            ["Feature", "An input variable used by the model, such as tenure or contract type."],
            ["Target", "The outcome the model learns to predict; here, the binary churn label."],
            ["Class imbalance", "A situation in which one outcome is much more frequent than the other."],
            ["Training set", "The portion of data used to fit the model parameters."],
            ["Validation set", "Data used to compare models and tune settings without touching the test set."],
            ["Test set", "A held-out portion used once to estimate final performance."],
            ["Pipeline", "A sequence of preprocessing and modelling steps applied as one object."],
            ["Probability", "A number between 0 and 1 expressing the model's estimated likelihood of churn."],
            ["Threshold", "The probability cut-off above which a customer is classified as a churner."],
            ["ROC-AUC", "The probability that the model ranks a random churner above a random non-churner."],
            ["Recall", "The proportion of actual churners that the model identifies."],
            ["Precision", "The proportion of customers flagged as churners who actually churn."],
            ["Permutation importance", "The drop in model performance when a feature's values are randomly shuffled."],
        ],
        widths=[1.45, 5.0],
        font_size=9,
        first_col_bold=True,
        cap="Table 3.1: Glossary of terms used in the report",
    )

    section(doc, "3.4", "Churn as a Binary Classification Problem")
    body(
        doc,
        (
            "Let each customer be represented by a feature vector **x** containing account, "
            "service and billing attributes, and let **y** be a binary label with y = 1 for churn "
            "and y = 0 for retention. A classifier estimates the conditional probability "
            "P(y = 1 | x). The model is trained on a labelled sample and then applied to new "
            "customers. A decision rule converts the probability into a class label: if the "
            "estimated probability exceeds a threshold t, the customer is classified as a "
            "predicted churner."
        ),
    )
    body(
        doc,
        (
            "The choice of threshold is a business decision, not a statistical one. A low "
            "threshold flags more customers, catching more true churners at the cost of contacting "
            "more customers who would have stayed. A high threshold conserves retention capacity "
            "but misses customers who are about to leave. This project uses the conventional 0.50 "
            "threshold for the reported results and discusses the trade-off explicitly in Chapter "
            "10. The application also reports the raw probability, so a manager can apply a "
            "different threshold if the economics of the campaign justify it."
        ),
    )
    body(
        doc,
        (
            "The features are a mixture of numeric variables (tenure, monthly charges, total "
            "charges) and categorical variables (contract, payment method, internet service). "
            "Categorical variables cannot be used directly by most algorithms and must be encoded. "
            "Numeric variables have different scales and must be standardised for logistic "
            "regression. These transformations are learned from the training data and applied "
            "unchanged to the test data, which prevents information leakage."
        ),
    )

    section(doc, "3.5", "Evaluation Metrics")
    body(
        doc,
        (
            "A binary classifier produces four outcomes: true positives (TP), customers who "
            "churned and were correctly flagged; true negatives (TN), customers who stayed and were "
            "correctly left alone; false positives (FP), customers who stayed but were flagged; and "
            "false negatives (FN), customers who churned but were missed. The metrics used in this "
            "report are defined in Table 3.2."
        ),
    )
    table(
        doc,
        ["Metric", "Formula", "Interpretation"],
        [
            ["Accuracy", "(TP + TN) / (TP + TN + FP + FN)", "Overall proportion of correct predictions; misleading under class imbalance."],
            ["Precision", "TP / (TP + FP)", "Of the customers flagged, the proportion who actually churn."],
            ["Recall", "TP / (TP + FN)", "Of the customers who churn, the proportion that is caught."],
            ["F1 score", "2 × (Precision × Recall) / (Precision + Recall)", "Harmonic mean of precision and recall."],
            ["ROC-AUC", "Area under the true-positive vs false-positive curve", "Probability of ranking a churner above a non-churner."],
            ["PR-AUC", "Area under the precision-recall curve", "Summary of precision-recall performance; sensitive to imbalance."],
        ],
        widths=[1.1, 2.5, 2.85],
        font_size=8.8,
        first_col_bold=True,
        cap="Table 3.2: Evaluation metrics and their interpretation",
    )
    body(
        doc,
        (
            "Accuracy is included for completeness but is not used to select the model. A trivial "
            "classifier that predicts *no churn* for every customer would achieve 73.5% accuracy "
            "while catching zero churners. The project therefore selects on cross-validated "
            "ROC-AUC, which measures ranking quality independent of the threshold, and reports "
            "recall and precision at the chosen operating point."
        ),
    )
    body(
        doc,
        (
            "ROC-AUC has a precise interpretation: it is the probability that a randomly chosen "
            "churner receives a higher risk score than a randomly chosen non-churner. A value of "
            "0.5 corresponds to random ranking and 1.0 to perfect ranking. The selected model "
            "achieves 0.846, which means that in roughly 85 of every 100 randomly formed "
            "churner/non-churner pairs, the churner is ranked higher. This is a strong result for "
            "tabular customer data."
        ),
    )

    section(doc, "3.6", "Business Interpretation of a Probability")
    body(
        doc,
        (
            "A churn probability is not a certainty about an individual. It is an estimate of the "
            "frequency with which customers with similar characteristics leave. If the model "
            "assigns a probability of 0.72 to a customer, the correct interpretation is that among "
            "customers with a similar profile, approximately 72% churned in the historical data. "
            "The retention team can use that estimate to prioritise, but it should not treat the "
            "score as a guarantee."
        ),
    )
    body(
        doc,
        (
            "This distinction matters for communication. Saying *this customer will leave* is "
            "overconfident and can damage trust when the customer stays. Saying *this customer has "
            "a high estimated risk and here are the factors driving it* is accurate, actionable "
            "and consistent with the model's actual output. The Streamlit application is designed "
            "around this interpretation: it presents a risk band, a probability and a list of "
            "contributing factors rather than a binary verdict."
        ),
    )


# ---------------------------------------------------------------------------
# 4. SYSTEM ARCHITECTURE
# ---------------------------------------------------------------------------
def chapter_4(doc):
    chapter(doc, 4, "SYSTEM ARCHITECTURE")

    body(
        doc,
        (
            "The system is organised as a sequence of well-defined stages that transform raw "
            "customer records into an actionable risk score. The architecture separates offline "
            "model development from online inference, keeps preprocessing inside the saved "
            "pipeline, and exposes the model through a thin presentation layer. This separation "
            "makes the system reproducible, testable and easy to extend."
        ),
    )

    section(doc, "4.1", "Architectural Overview")
    body(
        doc,
        (
            "Figure 4.1 shows the end-to-end architecture. Raw data enters the system once and is "
            "cleaned and enriched before being split into training and test partitions. The "
            "training partition is used for cross-validation and model selection; the test "
            "partition is held back until the final evaluation. The selected pipeline, together "
            "with its metadata and evaluation artifacts, is persisted to disk. The Streamlit "
            "application loads the persisted pipeline and serves predictions to the user."
        ),
    )
    figure(
        doc,
        FIGURES / "12_architecture.png",
        width=6.45,
        cap="Figure 4.1: End-to-end system architecture",
    )
    body(
        doc,
        (
            "The architecture is deliberately batch-oriented on the training side and "
            "request-oriented on the serving side. Training is an offline, reproducible job that "
            "can be re-run when new data arrives. Serving is a stateless function of the customer "
            "record and the saved pipeline, which makes the application easy to host and reason "
            "about."
        ),
    )

    section(doc, "4.2", "Architectural Principles")
    body(doc, "Five principles guided the design:")
    numbered(
        doc,
        [
            "**Single source of truth.** All preprocessing is defined inside the scikit-learn "
            "pipeline. The same transformations are used during training, evaluation and "
            "inference, eliminating training-serving skew.",
            "**No leakage.** The test set is created once with a fixed random seed and is never "
            "used for feature selection, hyperparameter tuning or threshold selection.",
            "**Reproducibility.** Random seeds, package versions, input data and output artifacts "
            "are recorded so that the experiment can be reconstructed.",
            "**Separation of concerns.** Data preparation, modelling, evaluation and presentation "
            "are implemented in separate modules with clear responsibilities.",
            "**Explainability by design.** The system stores feature names and permutation "
            "importance so that predictions can be explained to a non-technical audience.",
        ],
        size=12,
        space_after=5,
    )

    section(doc, "4.3", "System Components")
    table(
        doc,
        ["Component", "Responsibility", "Implementation"],
        [
            ["Data layer", "Stores the raw CSV and the cleaned modelling table.", "data/Telco-Customer-Churn.csv"],
            ["Preparation module", "Loads, validates, cleans and enriches the data.", "src/train.py"],
            ["Preprocessing pipeline", "Imputes, scales and one-hot encodes features.", "scikit-learn ColumnTransformer"],
            ["Model layer", "Trains and compares three classifiers; selects the best.", "LogisticRegression, RandomForestClassifier, HistGradientBoostingClassifier"],
            ["Evaluation layer", "Computes metrics, curves and permutation importance.", "scikit-learn metrics and inspection"],
            ["Artifact layer", "Persists the pipeline, metrics and human-readable report.", "joblib, JSON, text"],
            ["Presentation layer", "Provides risk scoring, explanations and what-if analysis.", "Streamlit application (app.py)"],
            ["Documentation layer", "Records methodology, results and operating instructions.", "Markdown, DOCX and PDF reports"],
        ],
        widths=[1.35, 2.75, 2.35],
        font_size=8.6,
        first_col_bold=True,
        cap="Table 4.1: System components and responsibilities",
    )

    section(doc, "4.4", "End-to-End Workflow")
    body(doc, "The workflow consists of eight stages:")
    numbered(
        doc,
        [
            "**Acquisition.** The raw CSV is read into a pandas DataFrame. The schema is checked "
            "and the target is mapped from Yes/No to 1/0.",
            "**Cleaning.** `TotalCharges` is converted from text to numeric. Eleven blank values, "
            "all belonging to customers with zero tenure, are imputed from `MonthlyCharges`. The "
            "identifier column is dropped.",
            "**Feature engineering.** Three features are added: the number of active services, the "
            "average monthly spend and a new-customer indicator.",
            "**Splitting.** The data is divided into 80% training and 20% test partitions using "
            "stratified sampling with a fixed random seed.",
            "**Preprocessing.** Numeric features are median-imputed and standardised; categorical "
            "features are most-frequent-imputed and one-hot encoded with unknown-category "
            "tolerance.",
            "**Training and selection.** Three models are evaluated with stratified five-fold "
            "cross-validation on the training partition. The model with the highest mean "
            "cross-validated ROC-AUC is selected.",
            "**Evaluation.** The selected model is fitted on the full training partition and "
            "evaluated once on the test partition. Confusion matrix, classification report, ROC "
            "curve, PR curve and permutation importance are computed.",
            "**Packaging and deployment.** The fitted pipeline and metadata are saved with joblib. "
            "The Streamlit application loads them and serves the interactive interface.",
        ],
        size=12,
        space_after=5,
    )

    section(doc, "4.5", "Data Flow and Transformations")
    body(
        doc,
        (
            "Table 4.2 summarises how the data changes as it moves through the pipeline. The "
            "number of columns increases from 21 to 23 after feature engineering, and then expands "
            "substantially after one-hot encoding. The exact encoded width depends on the "
            "categories observed in the training data, which is why the encoder is fitted inside "
            "the pipeline rather than on the full dataset."
        ),
    )
    table(
        doc,
        ["Stage", "Rows", "Columns", "Transformation"],
        [
            ["Raw CSV", "7,043", "21", "As downloaded; TotalCharges stored as text."],
            ["Cleaned", "7,043", "20", "Target encoded; identifier dropped; TotalCharges numeric."],
            ["Feature-engineered", "7,043", "23", "NumServices, AvgMonthlySpend and IsNewCustomer added."],
            ["Training partition", "5,634", "22 features", "Stratified 80% split; target separated."],
            ["Test partition", "1,409", "22 features", "Held out until final evaluation."],
            ["Encoded matrix", "5,634", "≈ 45", "Numeric scaled; categorical variables one-hot encoded."],
        ],
        widths=[1.4, 0.85, 0.95, 3.25],
        font_size=8.8,
        center_cols=[1, 2],
        first_col_bold=True,
        cap="Table 4.2: Data transformations through the pipeline",
    )

    section(doc, "4.6", "Deployment Architecture")
    body(
        doc,
        (
            "The deployed application is a single-process Streamlit server. On start-up it loads "
            "`models/churn_model.joblib`, which contains the fitted pipeline, the ordered feature "
            "list and the model name. It also loads `reports/metrics.json` for the performance "
            "view. When the user changes an input in the sidebar, Streamlit re-executes the script, "
            "builds a one-row DataFrame with the engineered features, calls `predict_proba` and "
            "renders the result."
        ),
    )
    body(
        doc,
        (
            "This architecture is appropriate for demonstration and internal review. It requires "
            "no database, no authentication layer and no separate API server. For production use, "
            "the same pipeline could be wrapped in a REST endpoint and placed behind an "
            "authenticated gateway; the model artifact would not need to change. Chapter 11 "
            "discusses this path."
        ),
    )

    section(doc, "4.7", "Design Decisions and Trade-offs")
    body(doc, "Several design decisions shaped the system:")
    bullet(
        doc,
        "**Pipeline over ad-hoc preprocessing.** Wrapping all transformations in a "
        "`ColumnTransformer` and `Pipeline` costs a little extra code but guarantees that "
        "inference uses exactly the same transformations as training.",
    )
    bullet(
        doc,
        "**Logistic Regression as a serious candidate.** The model is often treated as a "
        "baseline, but it offers interpretability, fast training and stable probabilities. It "
        "won the cross-validated comparison and was therefore selected on evidence rather than "
        "assumption.",
    )
    bullet(
        doc,
        "**Fixed 0.50 threshold for reporting.** Reporting at a standard threshold makes the "
        "results comparable with other studies. The application exposes the probability so that "
        "a different operating point can be chosen for a specific campaign.",
    )
    bullet(
        doc,
        "**Permutation importance over coefficients.** Coefficients are informative for logistic "
        "regression but depend on the encoding and scale. Permutation importance measures the "
        "actual drop in ROC-AUC when a feature is disrupted, which is easier to communicate.",
    )
    bullet(
        doc,
        "**Streamlit over a custom web application.** Streamlit delivers an interactive "
        "experience in a single Python file, which is appropriate for an internship timeline and "
        "keeps the focus on the model rather than on front-end engineering.",
        space_after=8,
    )


# ---------------------------------------------------------------------------
# 5. APPLICATIONS
# ---------------------------------------------------------------------------
def chapter_5(doc):
    chapter(doc, 5, "APPLICATIONS")

    body(
        doc,
        (
            "A churn model is valuable only when its output changes a decision. This chapter "
            "describes the practical applications of the system, moving from the retention "
            "workflow where it originated to adjacent uses in service design, financial planning "
            "and social programmes. It also states where the model should not be used, because "
            "the boundary between a useful decision aid and an inappropriate automation is an "
            "important part of professional practice."
        ),
    )

    section(doc, "5.1", "Retention Prioritisation")
    body(
        doc,
        (
            "The primary application is the ranking of customers by churn risk. A retention team "
            "typically has capacity to contact a few hundred customers per week. Sorting the "
            "customer base by predicted probability produces a work queue in which the expected "
            "number of true churners is much higher than in a random sample. At the selected "
            "operating point, the model catches about 79% of churners while flagging roughly 587 "
            "customers; a team that works through that list spends its effort where the risk is "
            "concentrated."
        ),
    )
    body(
        doc,
        (
            "Ranking is more useful than a binary flag because it supports triage. The highest-risk "
            "customers can receive a personal call, the next tier an automated offer, and the "
            "lowest-risk customers no intervention at all. The risk bands used in the application "
            "(low below 30%, medium between 30% and 60%, high above 60%) provide a simple triage "
            "scheme that can be adjusted to the team's capacity."
        ),
    )

    section(doc, "5.2", "Campaign Targeting and Offer Design")
    body(
        doc,
        (
            "The factor explanation in the application helps match the intervention to the "
            "reason for risk. A customer who is flagged because of a month-to-month contract may "
            "respond to a discounted annual plan. A customer who is flagged because of high "
            "monthly charges may respond to a service review or a loyalty credit. A customer who "
            "is flagged because of fiber-optic service and no technical support may need a "
            "service-quality conversation rather than a price discount."
        ),
    )
    body(
        doc,
        (
            "This is the difference between a churn score and a retention strategy. The score "
            "answers *who*; the explanation suggests *why*; the what-if simulator answers *what "
            "would change the score*. A retention manager can test a proposed intervention - for "
            "example, moving a customer from electronic check to automatic card payment, or from "
            "month-to-month to a one-year contract - and see the estimated effect before making "
            "the offer."
        ),
    )

    section(doc, "5.3", "Customer Segmentation and Lifetime Value")
    body(
        doc,
        (
            "Churn probabilities combine with customer value to prioritise by expected loss, not "
            "risk alone. Expected value at risk is approximately the churn probability multiplied "
            "by the present value of future margin."
        ),
    )
    body(
        doc,
        (
            "The same scores support segmentation. Customers can be grouped into risk tiers and "
            "cross-tabulated with contract type, tenure band or service mix. This produces a "
            "retention heat map that shows where risk is concentrated and whether the pattern is "
            "structural (for example, a product that consistently disappoints) or transient (for "
            "example, a billing problem affecting a cohort)."
        ),
    )

    section(doc, "5.4", "Service Quality and Product Feedback")
    body(
        doc,
        (
            "Churn is a lagging indicator of customer experience. A model that identifies "
            "high-risk customers before they leave provides an early warning system for service "
            "problems. If a disproportionate number of high-risk customers share a particular "
            "internet service, payment method or support configuration, the operations team has a "
            "signal to investigate. In the Telco data, fiber-optic customers churn at 41.9% and "
            "electronic-check customers at 45.3%; these are not causal findings, but they are "
            "legitimate prompts for further investigation."
        ),
    )
    body(
        doc,
        (
            "The model can also be used to evaluate the effect of service changes. If a new "
            "technical-support programme is introduced, the churn rate of the treated cohort can "
            "be compared with the model's expectation. This is not a substitute for a controlled "
            "experiment, but it provides a useful operational check."
        ),
    )

    section(doc, "5.5", "Financial Planning and Forecasting")
    body(
        doc,
        (
            "Aggregate churn probabilities can feed revenue forecasts. If the retention team "
            "knows that a certain number of high-risk customers are likely to leave, the finance "
            "team can model revenue under different retention scenarios. The probability "
            "distribution is more informative than a binary count because it allows a range of "
            "outcomes to be estimated rather than a single point forecast."
        ),
    )
    body(
        doc,
        (
            "The same logic applies to capacity planning. The number of predicted churners sets "
            "the workload for the retention call centre; the expected success rate of each offer "
            "sets the number of retained customers; and the retained revenue sets the return on "
            "the campaign. A model with a well-calibrated probability is therefore a planning "
            "asset, not only a targeting tool."
        ),
    )

    section(doc, "5.6", "Application in Social and Development Programmes")
    body(
        doc,
        (
            f"The host organisation, **{STUDENT['organisation']}**, works with communities and "
            "partners on welfare, skills and livelihood initiatives. The same analytical pattern "
            "- identifying participants who are at risk of disengaging and intervening early - "
            "applies to social programmes. A skills programme can use attendance and engagement "
            "data to identify learners at risk of dropping out; a livelihood programme can use "
            "participation data to identify households that may need additional support. The "
            "features and the label change, but the workflow does not."
        ),
    )
    body(
        doc,
        (
            "This transferability is one of the reasons the project is relevant to the internship "
            "programme. It demonstrates that data science is not confined to commercial "
            "optimisation; the same methods can support social outcomes when they are applied "
            "with care, transparency and respect for the people represented in the data."
        ),
    )

    section(doc, "5.7", "Where the Model Should Not Be Used")
    body(
        doc,
        (
            "The model should not be used to deny service, set individual prices or make "
            "automated decisions without human review. It is a probabilistic estimate trained on "
            "historical data, and historical data can encode unfair patterns. If a feature such as "
            "gender or senior-citizen status is correlated with churn, using the model to allocate "
            "offers could produce discriminatory outcomes. The application is therefore framed as "
            "a decision-support tool for a human retention team, not as an autonomous decision "
            "system."
        ),
    )
    body(
        doc,
        (
            "The model should also not be used outside the population on which it was trained. A "
            "model fitted to residential telecom customers may not transfer to enterprise "
            "accounts, prepaid mobile users or a different market. Before any operational use, the "
            "model should be validated on a recent, representative sample of the target "
            "population, and its performance should be monitored after deployment."
        ),
    )


# ---------------------------------------------------------------------------
# 6. TECHNOLOGIES USED
# ---------------------------------------------------------------------------
def chapter_6(doc):
    chapter(doc, 6, "TECHNOLOGIES USED")

    body(
        doc,
        (
            "The project uses a compact, well-established open-source stack. Every technology was "
            "chosen for a specific role: data manipulation, modelling, visualisation, persistence "
            "or presentation. The versions listed in this chapter are the versions used to "
            "produce the results in Chapter 10."
        ),
    )

    section(doc, "6.1", "Python")
    body(
        doc,
        (
            "Python is the primary implementation language. It provides readable syntax, a mature "
            "scientific ecosystem and excellent support for rapid experimentation. The project is "
            "organised into modules: `src/train.py` for data preparation, training and evaluation; "
            "`src/make_deck_assets.py` for presentation figures; `app.py` for the Streamlit "
            "application; and the report-generation modules under `src/`. All scripts are executed "
            "from the project root so that relative paths resolve consistently."
        ),
    )
    body(
        doc,
        (
            "Python's dynamic typing and interactive tools make it well suited to exploratory "
            "work, while its packaging and testing ecosystem make it suitable for reproducible "
            "delivery. The project uses type hints and docstrings in the core modules to keep the "
            "code understandable."
        ),
    )

    section(doc, "6.2", "pandas and NumPy")
    body(
        doc,
        (
            "pandas provides the `DataFrame` abstraction used throughout the project. It handles "
            "CSV loading, column selection, grouping, aggregation, missing-value treatment and "
            "feature construction. NumPy supplies the underlying numerical arrays and is used for "
            "probability thresholds and array operations. The combination makes it possible to "
            "express data transformations concisely without writing manual loops."
        ),
    )
    body(
        doc,
        (
            "pandas is also used in the application to construct a one-row DataFrame from the "
            "sidebar inputs. This ensures that the inference path receives the same column names "
            "and order as the training data, which is a common source of production errors."
        ),
    )

    section(doc, "6.3", "scikit-learn")
    body(
        doc,
        (
            "scikit-learn is the modelling backbone. It supplies the classifiers "
            "(`LogisticRegression`, `RandomForestClassifier`, `HistGradientBoostingClassifier`), "
            "the preprocessing transformers (`SimpleImputer`, `StandardScaler`, `OneHotEncoder`), "
            "the composition tools (`ColumnTransformer`, `Pipeline`), the model-selection utilities "
            "(`StratifiedKFold`, `cross_val_score`, `train_test_split`) and the evaluation metrics "
            "(`roc_auc_score`, `precision_score`, `recall_score`, `f1_score`, "
            "`average_precision_score`, `confusion_matrix`, `classification_report`)."
        ),
    )
    body(
        doc,
        (
            "The pipeline abstraction is particularly important. It binds preprocessing and "
            "modelling into a single object that can be fitted, evaluated and serialised as a "
            "unit. This eliminates the risk of applying a different encoding at inference time "
            "and makes cross-validation honest, because the transformers are re-fitted inside each "
            "fold."
        ),
    )

    section(doc, "6.4", "Matplotlib and Seaborn")
    body(
        doc,
        (
            "Matplotlib is the low-level plotting library used for the architecture diagram and "
            "for charts that require precise control over layout. Seaborn is used for statistical "
            "plots such as distribution plots and heat maps. The presentation figures in this "
            "report were generated with a consistent palette and typography so that the report and "
            "the slide deck share a visual language."
        ),
    )
    body(
        doc,
        (
            "Charts are saved as high-resolution PNG files rather than embedded as interactive "
            "objects. This keeps the report portable and ensures that the figures render "
            "identically on any machine."
        ),
    )

    section(doc, "6.5", "Streamlit")
    body(
        doc,
        (
            "Streamlit converts a Python script into an interactive web application. The "
            "application uses a sidebar for customer inputs, tabs for prediction, model "
            "performance, data insights and methodology, and custom HTML/CSS for the risk card and "
            "gauge. Streamlit's reactive execution model means that every input change triggers a "
            "re-run of the script and an updated prediction, with no explicit event handlers."
        ),
    )
    body(
        doc,
        (
            "The application is intentionally thin. It does not retrain the model or recompute "
            "metrics; it loads the artifacts produced by the training script. This separation "
            "keeps the demo fast and ensures that the displayed performance numbers correspond "
            "exactly to the saved model."
        ),
    )

    section(doc, "6.6", "joblib and JSON Artifacts")
    body(
        doc,
        (
            "joblib serialises the fitted pipeline, including the preprocessing steps and the "
            "classifier, into `models/churn_model.joblib`. The artifact also stores the ordered "
            "feature list and the model name. JSON files store the evaluation metrics and the EDA "
            "insights, which are read by the application and by the report generator. Plain text "
            "is used for the human-readable model report."
        ),
    )
    body(
        doc,
        (
            "The use of simple, inspectable formats is deliberate. A JSON metrics file can be "
            "diffed in version control, read by any language and understood without the original "
            "code. A joblib artifact is Python-specific, but it preserves the exact fitted state "
            "of the pipeline, which is essential for reproducible inference."
        ),
    )

    section(doc, "6.7", "Development and Documentation Tools")
    body(
        doc,
        (
            "Development was carried out in Visual Studio Code with the Python extension, which "
            "provides debugging, linting and integrated terminals. PowerShell was used to run the "
            "training script and the Streamlit server. Microsoft Word and python-docx were used to "
            "produce this report, and python-pptx was used to produce the accompanying "
            "presentation. The project is version-controlled in a local folder structure; a Git "
            "repository can be initialised without changing the code."
        ),
    )

    section(doc, "6.8", "Technology Stack Summary")
    table(
        doc,
        ["Technology", "Version", "Role in the Project"],
        [
            ["Python", "3.11+", "Implementation language for all modules."],
            ["pandas", "3.1.1", "Data loading, cleaning, aggregation and feature engineering."],
            ["NumPy", "2.5.4", "Numerical arrays and vectorised operations."],
            ["scikit-learn", "1.9.1", "Preprocessing, models, cross-validation and metrics."],
            ["Matplotlib", "3.11.2", "Charts and the architecture diagram."],
            ["Seaborn", "0.13.2", "Statistical visualisations."],
            ["Streamlit", "1.66.1", "Interactive web application."],
            ["joblib", "1.6.0", "Model persistence."],
            ["python-docx", "1.2.0", "Programmatic report generation."],
            ["python-pptx", "1.0.2", "Programmatic slide generation."],
        ],
        widths=[1.3, 0.9, 4.25],
        font_size=9,
        center_cols=[1],
        first_col_bold=True,
        cap="Table 6.1: Technology stack and versions",
    )
    body(
        doc,
        (
            "The stack is intentionally conservative. Every library is widely used, well "
            "documented and available under a permissive open-source licence. This reduces the "
            "risk of maintenance problems and makes the project easy for another student or "
            "developer to continue."
        ),
    )
