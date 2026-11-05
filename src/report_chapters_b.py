"""Chapters 7 to 12 of the internship report."""

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from report_config import APP_SHOTS, DECK_FIGURES, EDA, FIGURES, METRICS, STUDENT
from report_style import (
    BLUE,
    GRAY,
    NAVY,
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
# 7. ADVANTAGES AND DISADVANTAGES
# ---------------------------------------------------------------------------
def chapter_7(doc):
    chapter(doc, 7, "ADVANTAGES AND DISADVANTAGES")

    body(
        doc,
        (
            "No model is universally appropriate. A churn prediction system offers clear "
            "advantages over unaided retention work, but it also introduces costs, assumptions and "
            "risks. This chapter presents both sides honestly and describes how the project "
            "mitigates the main limitations."
        ),
    )

    section(doc, "7.1", "Advantages")
    body(
        doc,
        (
            "The system improves retention work in several concrete ways. The advantages below are "
            "stated in terms of what the organisation can do that it could not do before, rather "
            "than in terms of abstract model quality."
        ),
    )

    subsection(doc, "7.1.1", "Prioritisation under Limited Capacity")
    body(
        doc,
        (
            "The most immediate benefit is a ranked work queue. Retention teams cannot contact "
            "every customer, and contacting at random wastes effort on customers who would have "
            "stayed anyway. At the selected operating point the model flags 587 customers and "
            "correctly identifies 297 of the 374 churners in the test set. A random sample of the "
            "same size would be expected to contain only about 156 churners. The model therefore "
            "roughly doubles the yield of a fixed outreach budget."
        ),
    )

    subsection(doc, "7.1.2", "Early Warning")
    body(
        doc,
        (
            "Churn is observed only after the customer has left. A predictive model moves the "
            "observation point forward, giving the retention team time to intervene. This is "
            "especially important for customers on month-to-month contracts, whose departure can "
            "be abrupt. The model can be re-scored monthly, creating a rolling early-warning "
            "system."
        ),
    )

    subsection(doc, "7.1.3", "Explainability")
    body(
        doc,
        (
            "The application does not only return a score. It lists the factors that push the "
            "customer's risk up or down, and the report quantifies the global importance of each "
            "feature. This makes the output usable in a conversation with a customer or a "
            "manager, and it supports the choice of intervention. An unexplainable score is "
            "difficult to trust and difficult to act on."
        ),
    )

    subsection(doc, "7.1.4", "Consistency and Reproducibility")
    body(
        doc,
        (
            "A manual retention process depends on the judgement and memory of individual "
            "agents. Two agents may treat similar customers differently. A model applies the same "
            "logic to every customer and produces an auditable record. The pipeline, random seeds "
            "and package versions are recorded, so the result can be reproduced and reviewed."
        ),
    )

    subsection(doc, "7.1.5", "Low Operating Cost")
    body(
        doc,
        (
            "The stack is open source, the dataset is small and the model trains in seconds on a "
            "laptop. Inference is a single `predict_proba` call. There is no GPU requirement, no "
            "managed service and no licence fee. This makes the approach accessible to small "
            "organisations and to students, which is consistent with the inclusive ethos of the "
            "internship programme."
        ),
    )

    subsection(doc, "7.1.6", "Extensibility")
    body(
        doc,
        (
            "The pipeline is modular. New features can be added to the transformer, new models "
            "can be compared in the same cross-validation loop, and the presentation layer can be "
            "replaced without retraining. The same pattern can be applied to dropout prediction, "
            "loan default, equipment failure or any other binary outcome with tabular features."
        ),
    )

    section(doc, "7.2", "Disadvantages")
    body(
        doc,
        (
            "The limitations fall into three groups: data limitations, modelling limitations and "
            "deployment limitations. Recognising them is part of using the model responsibly."
        ),
    )

    subsection(doc, "7.2.1", "Historical and Observational Data")
    body(
        doc,
        (
            "The model learns associations in historical data, not causation. Features such as "
            "fiber-optic internet may reflect price, service quality or competition rather than a "
            "direct cause, so associations should generate hypotheses, not prescriptions."
        ),
    )

    subsection(doc, "7.2.2", "Class Imbalance and Metric Trade-offs")
    body(
        doc,
        (
            "Only 26.5% of customers churn. The model therefore produces more false positives than "
            "a balanced problem would: at the 0.50 threshold, 290 customers are flagged who would "
            "have stayed. This is a deliberate trade-off in favour of recall, but it has a cost in "
            "outreach effort and in the risk of annoying customers who were not at risk. A "
            "different campaign economics would justify a different threshold."
        ),
    )

    subsection(doc, "7.2.3", "Limited Context")
    body(
        doc,
        (
            "The dataset contains account and service attributes but not the full context of the "
            "customer relationship: call transcripts, complaints, network outages, competitor "
            "offers and life events are absent. The model can therefore miss sudden changes that "
            "are not reflected in the recorded features. It should be complemented by qualitative "
            "feedback from front-line staff."
        ),
    )

    subsection(doc, "7.2.4", "Temporal Validity")
    body(
        doc,
        (
            "The data is a snapshot. Customer behaviour, pricing and competition change over time, "
            "and a model trained on one period may lose accuracy in another. The project does not "
            "include a temporal validation split because the dataset does not provide reliable "
            "timestamps. In production, the model should be retrained and monitored regularly."
        ),
    )

    subsection(doc, "7.2.5", "Fairness and Privacy")
    body(
        doc,
        (
            "The dataset includes gender, age and family status. A model trained on these "
            "attributes can reproduce historical inequalities. The project does not perform a "
            "formal fairness audit, and the application is intended for decision support rather "
            "than automated action. Any operational deployment should include a fairness review, "
            "data-minimisation review and compliance check."
        ),
    )

    subsection(doc, "7.2.6", "Operational Dependence")
    body(
        doc,
        (
            "A model is only useful if its output is integrated into a workflow. If the retention "
            "team does not trust the score, cannot access it at the point of contact, or is not "
            "given the authority to act on it, the system becomes a dashboard that nobody uses. "
            "Deployment is therefore as much an organisational challenge as a technical one."
        ),
    )

    section(doc, "7.3", "Mitigation Strategies")
    table(
        doc,
        ["Risk", "Mitigation in the Project"],
        [
            ["Overfitting to the test set", "The test partition is created once and used only for the final evaluation; model selection uses cross-validation on the training partition."],
            ["Training-serving skew", "All preprocessing is stored inside the serialised pipeline and reused at inference."],
            ["Misleading accuracy", "Selection is based on ROC-AUC; recall, precision, F1 and PR-AUC are reported alongside accuracy."],
            ["Unclear model behaviour", "Permutation importance and per-customer factor explanations are provided."],
            ["Class imbalance", "Stratified splitting and cross-validation preserve the churn proportion in every fold."],
            ["Data quality problems", "Missing values and text-encoded numbers are handled explicitly and documented."],
            ["Automation bias", "The application presents a probability and risk band, not an automatic decision."],
            ["Model drift", "The pipeline is reproducible and can be retrained; monitoring is proposed in Chapter 11."],
        ],
        widths=[1.7, 4.75],
        font_size=9,
        first_col_bold=True,
        cap="Table 7.1: Risks and mitigation strategies",
    )

    section(doc, "7.4", "When to Use This Approach")
    body(
        doc,
        (
            "The approach is appropriate when historical labelled outcomes exist, when the "
            "features are available at prediction time, and when the cost of false positives is "
            "lower than the cost of missing a genuine churner. It is less appropriate when the "
            "population is small, when the outcome is driven by sudden external shocks, or when "
            "the organisation cannot act on the output. In those cases, a simpler segmentation or "
            "a qualitative review may be more useful than a sophisticated model."
        ),
    )


# ---------------------------------------------------------------------------
# 8. REQUIREMENTS
# ---------------------------------------------------------------------------
def chapter_8(doc):
    chapter(doc, 8, "REQUIREMENTS")

    body(
        doc,
        (
            "This chapter specifies the resources needed to reproduce, run and evaluate the "
            "project. The requirements are deliberately modest: the system runs on a standard "
            "student laptop and uses only open-source software. The figures below are the "
            "configurations used during development and are stated as minimums where appropriate."
        ),
    )

    section(doc, "8.1", "Hardware Requirements")
    table(
        doc,
        ["Component", "Minimum", "Recommended"],
        [
            ["Processor", "Intel Core i3 (8th generation) or equivalent", "Intel Core i5 / Ryzen 5 or better"],
            ["Memory", "8 GB RAM", "16 GB RAM"],
            ["Storage", "2 GB free disk space", "5 GB free solid-state storage"],
            ["Display", "1366 × 768", "1920 × 1080"],
            ["Network", "Not required for local use", "Required only to install packages or share the app"],
            ["GPU", "Not required", "Not required"],
        ],
        widths=[1.35, 2.55, 2.55],
        font_size=9.5,
        first_col_bold=True,
        cap="Table 8.1: Hardware requirements",
    )
    body(
        doc,
        (
            "The model is small enough to train on a CPU in a few seconds. Memory usage is "
            "dominated by the Python interpreter and the plotting libraries rather than by the "
            "dataset, which contains fewer than 10,000 rows."
        ),
    )

    section(doc, "8.2", "Software Requirements")
    table(
        doc,
        ["Software", "Version", "Purpose"],
        [
            ["Windows / Linux / macOS", "Windows 10 or 11 (tested)", "Operating system"],
            ["Python", "3.11 or later", "Runtime for all project code"],
            ["pip", "Latest", "Package installation"],
            ["Visual Studio Code", "Latest", "Code editing and debugging"],
            ["PowerShell", "5.1 or later", "Command execution"],
            ["Web browser", "Chrome, Edge or Firefox", "Streamlit interface"],
            ["Microsoft Word", "2016 or later", "Review of the generated report"],
            ["PDF reader", "Any", "Review of the exported report"],
        ],
        widths=[2.0, 1.9, 2.55],
        font_size=9.5,
        first_col_bold=True,
        cap="Table 8.2: Software requirements",
    )

    section(doc, "8.3", "Python Package Requirements")
    table(
        doc,
        ["Package", "Version", "Use"],
        [
            ["pandas", "3.1.1", "Tabular data manipulation"],
            ["numpy", "2.5.4", "Numerical operations"],
            ["scikit-learn", "1.9.1", "Preprocessing, models and metrics"],
            ["matplotlib", "3.11.2", "Plotting"],
            ["seaborn", "0.13.2", "Statistical plots"],
            ["streamlit", "1.66.1", "Interactive application"],
            ["joblib", "1.6.0", "Model serialisation"],
            ["python-docx", "1.2.0", "Report generation"],
            ["python-pptx", "1.0.2", "Presentation generation"],
            ["Pillow", "Latest", "Image processing"],
        ],
        widths=[1.55, 1.0, 3.9],
        font_size=9.5,
        center_cols=[1],
        first_col_bold=True,
        cap="Table 8.3: Python package requirements",
    )
    body(
        doc,
        (
            "The versions are pinned in `requirements.txt` so that a fresh environment can be "
            "recreated with `pip install -r requirements.txt`. Minor version differences are "
            "usually harmless, but the pinned versions are the ones used for the reported "
            "results."
        ),
    )

    section(doc, "8.4", "Data Requirements")
    body(doc, "The system expects a CSV file with the following characteristics:")
    bullet(doc, "One row per customer and a unique identifier column named `customerID`.")
    bullet(doc, "A binary target column named `Churn` containing `Yes` or `No`.")
    bullet(doc, "Twenty predictor columns covering demographics, account, services and billing.")
    bullet(doc, "Numeric columns `tenure`, `MonthlyCharges` and `TotalCharges`; `TotalCharges` may contain blanks and is converted during cleaning.")
    bullet(doc, "Categorical columns stored as text, with missing values allowed.", space_after=8)
    body(
        doc,
        (
            "The file is stored at `data/Telco-Customer-Churn.csv`. The training script validates "
            "the presence of the target and identifier columns and fails early with a clear error "
            "if either is missing."
        ),
    )

    section(doc, "8.5", "Functional Requirements")
    table(
        doc,
        ["ID", "Requirement", "Acceptance Criterion"],
        [
            ["FR-01", "Load and validate the raw dataset.", "The script reads the CSV and confirms 7,043 rows and the required columns."],
            ["FR-02", "Clean missing and malformed values.", "`TotalCharges` is numeric and contains no missing values after cleaning."],
            ["FR-03", "Engineer the three additional features.", "`NumServices`, `AvgMonthlySpend` and `IsNewCustomer` exist for every row."],
            ["FR-04", "Create a stratified train/test split.", "5,634 training rows and 1,409 test rows with matching churn proportions."],
            ["FR-05", "Train and compare three classifiers.", "Cross-validated ROC-AUC is recorded for every model."],
            ["FR-06", "Select and evaluate the best model.", "The selected model is evaluated once on the test set and all metrics are saved."],
            ["FR-07", "Explain model behaviour.", "Permutation importance is computed and stored for the top features."],
            ["FR-08", "Provide an interactive prediction interface.", "The Streamlit app accepts customer inputs and returns a probability and risk band."],
            ["FR-09", "Support what-if analysis.", "Changing contract, payment or service settings updates the estimated risk."],
            ["FR-10", "Persist artifacts for reuse.", "The pipeline, metrics and model report are saved to disk."],
        ],
        widths=[0.65, 2.4, 3.4],
        font_size=8.8,
        center_cols=[0],
        first_col_bold=True,
        cap="Table 8.4: Functional requirements",
    )

    section(doc, "8.6", "Non-Functional Requirements")
    table(
        doc,
        ["Attribute", "Requirement"],
        [
            ["Usability", "A non-technical user can obtain a risk score without reading documentation."],
            ["Performance", "Training completes in under one minute; a prediction is returned in under one second."],
            ["Reliability", "The same input and the same saved model always produce the same output."],
            ["Reproducibility", "A fixed random seed and pinned package versions reproduce the reported metrics."],
            ["Maintainability", "Data preparation, modelling, evaluation and presentation are separate modules."],
            ["Portability", "The application runs on Windows, Linux and macOS with the same Python dependencies."],
            ["Explainability", "Every prediction is accompanied by the factors that influenced it."],
            ["Privacy", "The demo uses a public dataset and does not process personal data."],
        ],
        widths=[1.35, 5.1],
        font_size=9.2,
        first_col_bold=True,
        cap="Table 8.5: Non-functional requirements",
    )

    section(doc, "8.7", "Installation and Execution")
    body(doc, "The project is executed from the project root with the following commands:")
    code_block(
        doc,
        [
            "# 1. Create and activate a virtual environment (recommended)",
            "python -m venv .venv",
            ".venv\\Scripts\\activate",
            "",
            "# 2. Install the pinned dependencies",
            "pip install -r requirements.txt",
            "",
            "# 3. Reproduce the training, evaluation and figures",
            "python src/train.py",
            "",
            "# 4. Launch the interactive application",
            "streamlit run app.py",
        ],
        cap="Code 8.1: Installation and execution commands",
        font_size=8.6,
    )
    body(
        doc,
        (
            "The application opens at `http://localhost:8501`. If the port is in use, an "
            "alternative port can be supplied with `--server.port`. The training script is "
            "idempotent: running it again overwrites the saved model and charts with artifacts "
            "computed from the same fixed seed."
        ),
    )


# ---------------------------------------------------------------------------
# 9. METHODOLOGY AND SOURCE CODE
# ---------------------------------------------------------------------------
def chapter_9(doc):
    chapter(doc, 9, "METHODOLOGY AND SOURCE CODE")

    body(
        doc,
        (
            "This chapter describes how the system was built. The methodology follows the "
            "CRISP-DM process model - business understanding, data understanding, data "
            "preparation, modelling, evaluation and deployment - adapted to the constraints of a "
            "45-day internship. Each stage is explained, the important design choices are "
            "justified, and selected source code is reproduced so that the implementation can be "
            "reviewed without opening the repository."
        ),
    )

    section(doc, "9.1", "Research Design")
    body(
        doc,
        (
            "The project is an applied, quantitative study. It uses a publicly available "
            "observational dataset, a supervised learning design and a held-out evaluation. The "
            "unit of analysis is the customer; the outcome is the binary churn label; the "
            "predictors are the account, service, demographic and billing attributes. The study "
            "is cross-sectional: each customer is observed once, and the model estimates the "
            "probability associated with that profile."
        ),
    )
    table(
        doc,
        ["CRISP-DM Phase", "Activity in This Project", "Output"],
        [
            ["Business understanding", "Define churn, retention value and the decision the model should support.", "Problem statement and objectives"],
            ["Data understanding", "Audit schema, missing values, distributions and class balance.", "Data-quality report and EDA charts"],
            ["Data preparation", "Clean, engineer features, split and build the preprocessing pipeline.", "Modelling table and pipeline"],
            ["Modelling", "Train three classifiers and compare them with cross-validation.", "Cross-validated scores"],
            ["Evaluation", "Evaluate the selected model on the test set; interpret importance.", "Metrics, curves and importance"],
            ["Deployment", "Package the pipeline and build the Streamlit interface.", "Saved model and live application"],
        ],
        widths=[1.35, 3.25, 1.85],
        font_size=8.8,
        first_col_bold=True,
        cap="Table 9.1: Mapping of the project to CRISP-DM",
    )

    section(doc, "9.2", "Data Acquisition")
    body(
        doc,
        (
            "The dataset was downloaded as a single CSV file and stored in the `data` directory. "
            "The file contains 7,043 rows and 21 columns. The first column, `customerID`, is a "
            "unique identifier; the last column, `Churn`, is the target. The remaining 19 columns "
            "are predictors. No external data was merged, which keeps the study self-contained and "
            "reproducible."
        ),
    )
    body(
        doc,
        (
            "The data was loaded with `pandas.read_csv`. Column names were checked against the "
            "expected schema, and the target was mapped from the strings `Yes` and `No` to the "
            "integers 1 and 0. This mapping is explicit rather than implicit, so the positive "
            "class is unambiguously the churn class."
        ),
    )

    section(doc, "9.3", "Data Quality Audit and Cleaning")
    body(
        doc,
        (
            "A structured audit was performed before any modelling. The audit checked row counts, "
            "duplicate identifiers, data types, missing values, category consistency and the "
            "distribution of the target. The findings are summarised in Table 9.2."
        ),
    )
    table(
        doc,
        ["Issue", "Finding", "Treatment"],
        [
            ["TotalCharges type", "Stored as text rather than numeric.", "Converted with `pd.to_numeric(errors='coerce')`."],
            ["Missing TotalCharges", "11 blank values, all with tenure = 0.", "Filled with the customer's MonthlyCharges."],
            ["Identifier", "customerID is unique and random.", "Dropped before modelling."],
            ["Target encoding", "Churn stored as Yes/No.", "Mapped to 1/0."],
            ["Class balance", "1,869 churners (26.5%) and 5,174 stayers (73.5%).", "Stratified split and stratified cross-validation."],
            ["Category consistency", "No unexpected categories or trailing spaces.", "No action required."],
            ["Duplicates", "No duplicate customer identifiers.", "No action required."],
        ],
        widths=[1.35, 2.55, 2.55],
        font_size=8.8,
        first_col_bold=True,
        cap="Table 9.2: Data-quality findings and treatments",
    )
    body(
        doc,
        (
            "The eleven missing `TotalCharges` values are not random. They belong to customers "
            "with zero tenure, who have not yet received a bill. Imputing them with the median "
            "would be wrong because it would assign a lifetime spend to a customer who has just "
            "joined. Filling them with the monthly charge is a sensible approximation of the first "
            "bill and preserves the customer in the dataset."
        ),
    )
    code_block(
        doc,
        [
            "def load_and_clean(path: Path) -> pd.DataFrame:",
            '    df = pd.read_csv(path)',
            "",
            "    # TotalCharges is text with 11 blanks for tenure = 0 customers.",
            '    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")',
            '    df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"])',
            "",
            "    # Encode the target explicitly: churn = 1, stay = 0.",
            '    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})',
            "",
            "    # The identifier has no predictive value.",
            '    df = df.drop(columns=["customerID"])',
            "    return df",
        ],
        cap="Code 9.1: Data loading and cleaning",
        font_size=8.6,
    )

    section(doc, "9.4", "Exploratory Data Analysis")
    body(
        doc,
        (
            "Exploratory analysis was used to understand the data before modelling, not to select "
            "features on the test set. The analysis examined the target distribution, the "
            "relationship between churn and contract type, the tenure distribution, the "
            "relationship between churn and charges, and the churn rate across service and payment "
            "categories. The main findings are summarised below; the corresponding figures appear "
            "in Chapter 10."
        ),
    )
    body(
        doc,
        (
            "The target is imbalanced: 73.5% of customers stayed and 26.5% churned. Contract type "
            "is the strongest single segmentation variable, with churn rates of 42.7%, 11.3% and "
            "2.8% for month-to-month, one-year and two-year contracts respectively. Churners have "
            "a mean tenure of 18.0 months compared with 37.6 months for stayers, and a mean "
            "monthly charge of $74.44 compared with $61.27. Fiber-optic customers churn at 41.9%, "
            "compared with 19.0% for DSL and 7.4% for customers with no internet service. "
            "Electronic-check customers churn at 45.3%, the highest of any payment method."
        ),
    )
    body(
        doc,
        (
            "These patterns are descriptive. They motivate the feature set and the later "
            "interpretation, but they are not causal claims. The modelling stage determines how "
            "much unique information each variable contributes once the others are taken into "
            "account."
        ),
    )
    figure(
        doc,
        FIGURES / "03_tenure_distribution.png",
        width=5.9,
        cap="Figure 9.1: Tenure distribution by churn outcome",
    )
    figure(
        doc,
        FIGURES / "06_correlation_heatmap.png",
        width=5.6,
        cap="Figure 9.2: Correlation between numeric features and churn",
    )

    section(doc, "9.5", "Feature Engineering")
    body(
        doc,
        (
            "Three features were added to the raw data. They were chosen because they are "
            "interpretable, computable at prediction time and motivated by the exploratory "
            "analysis. The first is the number of active services, which captures the breadth of "
            "the customer's relationship with the company. The second is the average monthly "
            "spend, which normalises total charges by tenure and distinguishes customers who pay "
            "a high rate from those whose total is high only because they have stayed for a long "
            "time. The third is a new-customer indicator for tenure of six months or less, which "
            "captures the high-risk early period observed in the tenure distribution."
        ),
    )
    table(
        doc,
        ["Feature", "Definition", "Rationale"],
        [
            ["NumServices", "Count of the eight service columns equal to `Yes`.", "Customers with a broader service relationship may be more embedded, or may be paying for services they do not value."],
            ["AvgMonthlySpend", "TotalCharges divided by tenure (minimum 1).", "Separates high spenders from long-tenured customers whose total is large only because of time."],
            ["IsNewCustomer", "1 if tenure ≤ 6 months, otherwise 0.", "The early months are the highest-risk period in the tenure distribution."],
        ],
        widths=[1.2, 2.55, 2.7],
        font_size=8.8,
        first_col_bold=True,
        cap="Table 9.3: Engineered features",
    )
    code_block(
        doc,
        [
            'service_cols = [',
            '    "PhoneService", "MultipleLines", "OnlineSecurity", "OnlineBackup",',
            '    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",',
            ']',
            'df["NumServices"] = (df[service_cols] == "Yes").sum(axis=1)',
            'df["AvgMonthlySpend"] = df["TotalCharges"] / df["tenure"].clip(lower=1)',
            'df["IsNewCustomer"] = (df["tenure"] <= 6).astype(int)',
        ],
        cap="Code 9.2: Feature engineering",
        font_size=8.6,
    )

    section(doc, "9.6", "Preprocessing Pipeline")
    body(
        doc,
        (
            "The preprocessing pipeline is a `ColumnTransformer` with two branches. Numeric "
            "features are median-imputed and standardised. Categorical features are "
            "most-frequent-imputed and one-hot encoded. The encoder uses "
            "`handle_unknown='ignore'` so that a category not seen during training does not cause "
            "an error at inference; it is simply encoded as all zeros for that feature group."
        ),
    )
    body(
        doc,
        (
            "The pipeline is fitted inside each cross-validation fold, which means that imputation "
            "and scaling parameters are learned only from the training portion of that fold. This "
            "is the correct way to prevent leakage. Fitting the scaler on the full dataset before "
            "splitting would allow information from the test set to influence the training "
            "process and would produce optimistic performance estimates."
        ),
    )
    code_block(
        doc,
        [
            "numeric_pipeline = Pipeline([",
            '    ("imputer", SimpleImputer(strategy="median")),',
            '    ("scaler", StandardScaler()),',
            "])",
            "",
            "categorical_pipeline = Pipeline([",
            '    ("imputer", SimpleImputer(strategy="most_frequent")),',
            '    ("onehot", OneHotEncoder(handle_unknown="ignore")),',
            "])",
            "",
            "preprocessor = ColumnTransformer([",
            '    ("num", numeric_pipeline, NUMERIC_FEATURES),',
            '    ("cat", categorical_pipeline, CATEGORICAL_FEATURES),',
            "])",
        ],
        cap="Code 9.3: Preprocessing pipeline",
        font_size=8.6,
    )

    section(doc, "9.7", "Model Selection and Training")
    body(
        doc,
        (
            "Three classifiers were compared: Logistic Regression, Random Forest and Histogram "
            "Gradient Boosting. The three represent different inductive biases. Logistic "
            "Regression assumes a linear relationship in the log-odds and produces a smooth, "
            "well-calibrated probability. Random Forest averages many decorrelated decision trees "
            "and captures non-linear interactions. Gradient Boosting builds trees sequentially, "
            "each one correcting the errors of its predecessor, and often achieves high accuracy "
            "on tabular data."
        ),
    )
    table(
        doc,
        ["Model", "Key Settings", "Rationale"],
        [
            ["Logistic Regression", "max_iter=2000, default L2 penalty, lbfgs solver", "Interpretable linear baseline; stable probabilities."],
            ["Random Forest", "300 trees, max_depth=None, min_samples_leaf=2, n_jobs=-1", "Captures non-linearities and interactions; robust to outliers."],
            ["Histogram Gradient Boosting", "learning_rate=0.08, max_iter=250, max_leaf_nodes=31", "Strong tabular learner; handles mixed feature scales."],
        ],
        widths=[1.5, 2.55, 2.4],
        font_size=8.6,
        first_col_bold=True,
        cap="Table 9.4: Model configurations",
    )
    body(
        doc,
        (
            "The comparison uses stratified five-fold cross-validation on the training partition. "
            "In each fold, four parts are used to fit the pipeline and one part is used to score "
            "it. The reported score is the mean ROC-AUC across the five folds, and the standard "
            "deviation is retained as a measure of stability. The test partition is not touched "
            "during this process."
        ),
    )
    code_block(
        doc,
        [
            "cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)",
            "",
            "for name, estimator in MODELS.items():",
            "    pipeline = Pipeline([",
            '        ("preprocessor", build_preprocessor()),',
            '        ("classifier", estimator),',
            "    ])",
            "    scores = cross_val_score(",
            "        pipeline, X_train, y_train,",
            '        cv=cv, scoring="roc_auc", n_jobs=-1,',
            "    )",
            '    print(f"{name}: {scores.mean():.4f} +/- {scores.std():.4f}")',
        ],
        cap="Code 9.4: Stratified cross-validation",
        font_size=8.6,
    )

    section(doc, "9.8", "Evaluation Protocol")
    body(
        doc,
        (
            "The model with the highest mean cross-validated ROC-AUC is selected. It is then "
            "fitted on the entire training partition and evaluated once on the test partition. "
            "The evaluation reports accuracy, precision, recall, F1, ROC-AUC and PR-AUC, together "
            "with the confusion matrix and the classification report. ROC and precision-recall "
            "curves are plotted, and permutation importance is computed on the test set to "
            "quantify the contribution of each feature."
        ),
    )
    body(
        doc,
        (
            "Permutation importance is calculated by shuffling one feature at a time and measuring "
            "the resulting drop in ROC-AUC. The procedure is repeated several times per feature to "
            "obtain a mean and standard deviation. Unlike a coefficient, the measure reflects the "
            "model's actual reliance on the feature in the context of all other features, which "
            "makes it more suitable for communicating importance to a business audience."
        ),
    )
    code_block(
        doc,
        [
            "probs = best_model.predict_proba(X_test)[:, 1]",
            "preds = (probs >= 0.5).astype(int)",
            "",
            "print(classification_report(",
            '    y_test, preds, target_names=["Stayed", "Churned"],',
            "))",
            'print("ROC-AUC:", roc_auc_score(y_test, probs))',
            'print("PR-AUC :", average_precision_score(y_test, probs))',
        ],
        cap="Code 9.5: Final evaluation",
        font_size=8.6,
    )

    section(doc, "9.9", "Threshold Selection")
    body(
        doc,
        (
            "The reported results use a probability threshold of 0.50. This is a conventional "
            "choice that makes the results comparable with other studies, but it is not "
            "necessarily the optimal operating point for a retention campaign. If a contact costs "
            "$5 and a retained customer is worth $500, the optimal threshold is much lower than "
            "0.50 because a false negative is far more expensive than a false positive. The "
            "application therefore exposes the probability and the risk band, allowing the "
            "retention team to apply its own cost assumptions."
        ),
    )
    body(
        doc,
        (
            "The threshold should be chosen on a validation set, not on the test set. In this "
            "project, the test set is reserved for the final report; a production deployment "
            "would use a separate validation partition or a time-based holdout to tune the "
            "operating point."
        ),
    )

    section(doc, "9.10", "Application Implementation")
    body(
        doc,
        (
            "The Streamlit application loads the saved pipeline and feature list at start-up. The "
            "sidebar collects the customer's demographic, account, service and billing details. "
            "The application constructs a one-row DataFrame, computes the engineered features, "
            "calls `predict_proba` and renders a risk card, a gauge and a list of contributing "
            "factors. The factor logic compares the customer's values with known risk patterns "
            "from the training data, such as a month-to-month contract or electronic-check "
            "payment, and labels each factor as risk-increasing or risk-reducing."
        ),
    )
    body(
        doc,
        (
            "The what-if simulator reuses the same inference function with modified contract, "
            "payment or service values. It displays the original probability, the new probability "
            "and the difference, which makes the effect of a proposed intervention concrete. The "
            "model-performance and data-insights tabs read the saved metrics and charts, so the "
            "application remains consistent with the report."
        ),
    )
    code_block(
        doc,
        [
            "customer = build_customer(",
            "    gender, senior, partner, dependents, phone_service, multiple_lines,",
            "    internet_service, online_security, online_backup, device_protection,",
            "    tech_support, streaming_tv, streaming_movies, contract,",
            "    paperless_billing, payment_method, tenure, monthly_charges,",
            ")",
            "probability = float(model.predict_proba(customer)[0, 1])",
            "band, colour, background = risk_band(probability)",
        ],
        cap="Code 9.6: Inference in the Streamlit application",
        font_size=8.6,
    )

    section(doc, "9.11", "Reproducibility and Code Quality")
    body(
        doc,
        (
            "The project fixes the random seed at 42 for the train/test split, the cross-validation "
            "folds and the Random Forest. Package versions are pinned in `requirements.txt`. The "
            "training script writes the model, metrics, EDA insights and figures to known paths, so "
            "the application and the report generator can consume them without manual steps. "
            "Functions are small and named after the operation they perform, and the main modules "
            "include docstrings that explain their purpose."
        ),
    )
    body(
        doc,
        (
            "A limitation is that the project does not include an automated test suite or a "
            "continuous-integration pipeline. For an internship project of this scope, manual "
            "verification and a reproducible script were considered sufficient. A production "
            "version would add unit tests for the cleaning and feature-engineering functions, an "
            "integration test for the pipeline and a smoke test for the application."
        ),
    )


# ---------------------------------------------------------------------------
# 10. RESULTS AND OUTPUT SCREENSHOTS
# ---------------------------------------------------------------------------
def chapter_10(doc):
    chapter(doc, 10, "RESULTS AND OUTPUT SCREENSHOTS")

    body(
        doc,
        (
            "This chapter presents the results of the study. It begins with the exploratory "
            "findings, then reports the model comparison, the final test-set performance, the "
            "confusion matrix, the ranking curves and the feature importance. It concludes with "
            "screenshots of the deployed application and a discussion of the errors the model "
            "makes."
        ),
    )

    section(doc, "10.1", "Experimental Setup")
    body(
        doc,
        (
            f"The cleaned dataset contains **{DATASET['rows']:,} customers** and 22 predictors "
            f"after feature engineering. A stratified 80/20 split produced **{DATASET['train_rows']:,} "
            f"training customers** and **{DATASET['test_rows']:,} test customers**. The test set "
            f"contains 374 churners and 1,035 stayers, which matches the overall churn rate of "
            f"26.5%. All models were trained on the same training partition and evaluated on the "
            f"same test partition with the same preprocessing pipeline."
        ),
    )

    section(doc, "10.2", "Exploratory Findings")
    body(
        doc,
        (
            "Figure 10.1 shows the class distribution. The imbalance is substantial: a model that "
            "always predicts *stay* would be 73.5% accurate while never identifying a churner. "
            "This is why the evaluation focuses on ROC-AUC and recall rather than accuracy."
        ),
    )
    figure(
        doc,
        DECK_FIGURES / "balance.png",
        width=4.6,
        cap="Figure 10.1: Class distribution in the dataset",
    )
    body(
        doc,
        (
            f"Figure 10.2 shows churn by contract type. The gradient is steep: **42.7%** of "
            f"month-to-month customers churn, compared with **11.3%** of one-year customers and "
            f"**2.8%** of two-year customers. Contract type is therefore a powerful segmentation "
            f"variable and a plausible target for retention offers, although the observational "
            f"data cannot prove that upgrading a contract causes a customer to stay."
        ),
    )
    figure(
        doc,
        DECK_FIGURES / "contract.png",
        width=5.7,
        cap="Figure 10.2: Churn rate by contract type",
    )
    body(
        doc,
        (
            "Figure 10.3 shows the tenure distribution. Churners are concentrated at low tenure, "
            "with a mean of 18.0 months, while stayers have a mean of 37.6 months. The shape "
            "suggests that the first year is the critical retention window and that interventions "
            "should be concentrated early in the customer lifecycle."
        ),
    )
    figure(
        doc,
        DECK_FIGURES / "tenure.png",
        width=5.9,
        cap="Figure 10.3: Tenure distribution for churned and retained customers",
    )
    body(
        doc,
        (
            "Figure 10.4 summarises four behavioural drivers. Fiber-optic customers churn at "
            "41.9%, compared with 19.0% for DSL and 7.4% for customers without internet service. "
            "Electronic-check customers churn at 45.3%, compared with 15.2% for automatic credit "
            "card and 16.7% for automatic bank transfer. Customers without technical support or "
            "online security also show higher churn. These patterns are consistent with the "
            "hypothesis that customers who feel unsupported or who have a more transactional "
            "payment relationship are more likely to leave."
        ),
    )
    figure(
        doc,
        DECK_FIGURES / "drivers.png",
        width=6.2,
        cap="Figure 10.4: Churn rate across internet service, payment method, technical support and online security",
    )

    section(doc, "10.3", "Model Comparison")
    body(
        doc,
        (
            "Table 10.1 reports the cross-validated ROC-AUC and the test-set metrics for the three "
            "models. Logistic Regression achieved the highest mean cross-validated ROC-AUC "
            "(0.8474) and was selected. Random Forest was extremely close (0.8457), while "
            "Gradient Boosting was lower (0.8267). The difference between the top two models is "
            "small relative to their fold-to-fold variation, but the selection rule was fixed in "
            "advance, so the result is not a post-hoc choice."
        ),
    )
    table(
        doc,
        ["Model", "CV ROC-AUC", "Test ROC-AUC", "Accuracy", "Precision", "Recall", "F1"],
        [
            [
                "Logistic Regression",
                f"{ALL['Logistic Regression']['cv_roc_auc_mean']:.4f} ± {ALL['Logistic Regression']['cv_roc_auc_std']:.4f}",
                f"{ALL['Logistic Regression']['test']['roc_auc']:.4f}",
                f"{ALL['Logistic Regression']['test']['accuracy']:.4f}",
                f"{ALL['Logistic Regression']['test']['precision']:.4f}",
                f"{ALL['Logistic Regression']['test']['recall']:.4f}",
                f"{ALL['Logistic Regression']['test']['f1']:.4f}",
            ],
            [
                "Random Forest",
                f"{ALL['Random Forest']['cv_roc_auc_mean']:.4f} ± {ALL['Random Forest']['cv_roc_auc_std']:.4f}",
                f"{ALL['Random Forest']['test']['roc_auc']:.4f}",
                f"{ALL['Random Forest']['test']['accuracy']:.4f}",
                f"{ALL['Random Forest']['test']['precision']:.4f}",
                f"{ALL['Random Forest']['test']['recall']:.4f}",
                f"{ALL['Random Forest']['test']['f1']:.4f}",
            ],
            [
                "Gradient Boosting",
                f"{ALL['Gradient Boosting']['cv_roc_auc_mean']:.4f} ± {ALL['Gradient Boosting']['cv_roc_auc_std']:.4f}",
                f"{ALL['Gradient Boosting']['test']['roc_auc']:.4f}",
                f"{ALL['Gradient Boosting']['test']['accuracy']:.4f}",
                f"{ALL['Gradient Boosting']['test']['precision']:.4f}",
                f"{ALL['Gradient Boosting']['test']['recall']:.4f}",
                f"{ALL['Gradient Boosting']['test']['f1']:.4f}",
            ],
        ],
        widths=[1.35, 1.15, 0.85, 0.8, 0.8, 0.75, 0.65],
        font_size=8.4,
        center_cols=[1, 2, 3, 4, 5, 6],
        first_col_bold=True,
        cap="Table 10.1: Cross-validation and test-set performance",
    )
    body(
        doc,
        (
            "The table reveals an important trade-off. Gradient Boosting has the highest accuracy "
            "(0.7807) and precision (0.6045) but the lowest recall (0.5027): it identifies only "
            "about half of the churners. Logistic Regression has the highest recall (0.7941) and "
            "the highest ROC-AUC on both cross-validation and the test set. For a retention use "
            "case, where missing a churner is usually more costly than contacting a customer who "
            "would have stayed, the higher recall is the more valuable property."
        ),
    )
    body(
        doc,
        (
            "Random Forest is a close second on ROC-AUC and has a slightly higher F1 (0.6288) "
            "because its precision is better balanced against recall. If the retention team were "
            "strictly limited in capacity and could tolerate missing more churners, Random Forest "
            "would be a reasonable alternative. The selection of Logistic Regression is therefore "
            "justified by the stated objective - ranking quality and recall - rather than by a "
            "claim that it dominates on every metric."
        ),
    )
    figure(
        doc,
        DECK_FIGURES / "compare.png",
        width=6.0,
        cap="Figure 10.5: Cross-validated ROC-AUC and test recall by model",
    )

    section(doc, "10.4", "Final Model Performance")
    body(
        doc,
        (
            f"On the held-out test set, the selected Logistic Regression model achieved a "
            f"**ROC-AUC of {BEST['roc_auc']:.3f}**, a **recall of {BEST['recall']:.1%}**, a "
            f"**precision of {BEST['precision']:.1%}**, an **F1 of {BEST['f1']:.3f}** and an "
            f"**accuracy of {BEST['accuracy']:.1%}**. The PR-AUC is {BEST['pr_auc']:.3f}. In "
            f"practical terms, the model correctly identified **297 of the 374 customers who "
            f"churned** and flagged 290 customers who stayed. The full classification report is "
            f"reproduced in Table 10.2."
        ),
    )
    table(
        doc,
        ["Class", "Precision", "Recall", "F1", "Support"],
        [
            ["Stayed", "0.91", "0.72", "0.80", "1,035"],
            ["Churned", "0.51", "0.79", "0.62", "374"],
            ["Accuracy", "", "", "0.740", "1,409"],
            ["Macro average", "0.71", "0.76", "0.71", "1,409"],
            ["Weighted average", "0.80", "0.74", "0.75", "1,409"],
        ],
        widths=[1.5, 1.1, 1.0, 0.9, 1.0],
        font_size=9.2,
        center_cols=[1, 2, 3, 4],
        first_col_bold=True,
        cap="Table 10.2: Classification report for the selected model",
    )
    body(
        doc,
        (
            "The asymmetry between the classes is visible in the table. The model is good at "
            "recognising stayers (precision 0.91) and good at catching churners (recall 0.79), but "
            "the precision on churners is only 0.51. This is the expected consequence of a 0.50 "
            "threshold on an imbalanced problem: to catch four out of five churners, the model "
            "must accept that about half of the customers it flags would have stayed."
        ),
    )

    section(doc, "10.5", "Confusion Matrix and Error Analysis")
    body(
        doc,
        (
            "The confusion matrix in Figure 10.6 makes the error structure explicit. Of 1,035 "
            "stayers, 745 were correctly left alone and 290 were flagged. Of 374 churners, 297 "
            "were correctly flagged and 77 were missed. The false negatives are the most expensive "
            "errors for a retention team because they represent lost customers who received no "
            "intervention."
        ),
    )
    figure(
        doc,
        DECK_FIGURES / "confusion.png",
        width=4.9,
        cap="Figure 10.6: Confusion matrix on the held-out test set",
    )
    body(
        doc,
        (
            "The 77 missed churners are likely to be customers whose profile resembles that of "
            "stayers: long tenure, a two-year contract or a service bundle that historically "
            "correlates with retention. Their departure may be driven by factors that the dataset "
            "does not capture, such as a competitor offer, a house move or a change in household "
            "circumstances. This is a fundamental limit of a model trained on account attributes "
            "alone."
        ),
    )
    body(
        doc,
        (
            "The 290 false positives are customers who were flagged but stayed. In a retention "
            "campaign they would receive an unnecessary contact or offer. This is not wasted in "
            "the same sense as a missed churner - a well-designed check-in can strengthen the "
            "relationship - but it consumes capacity and should be managed. A higher threshold "
            "would reduce false positives at the cost of more false negatives; the right balance "
            "depends on campaign economics."
        ),
    )

    section(doc, "10.6", "Ranking Quality")
    body(
        doc,
        (
            "Figure 10.7 shows the ROC curve. The curve rises steeply at low false-positive rates, "
            "which is the region that matters when a retention team can contact only a small "
            "fraction of the customer base. The area under the curve is 0.846, well above the "
            "random-ranking diagonal of 0.500. The PR-AUC of 0.653 is also substantially above the "
            "base churn rate of 0.265, which confirms that the model concentrates true churners "
            "near the top of the ranking."
        ),
    )
    figure(
        doc,
        DECK_FIGURES / "roc.png",
        width=5.3,
        cap="Figure 10.7: ROC curve for the selected model",
    )
    body(
        doc,
        (
            "The practical interpretation is a lift of approximately 1.9. If the team contacts the "
            "587 flagged customers, it reaches 297 true churners. A random sample of 587 customers "
            "would contain about 156 churners. The model therefore nearly doubles the number of "
            "at-risk customers reached for the same outreach cost."
        ),
    )

    section(doc, "10.7", "Feature Importance")
    body(
        doc,
        (
            "Figure 10.8 reports permutation importance on the test set. Tenure is the most "
            "important feature, followed by contract type, internet service, monthly charges and "
            "the new-customer indicator. The ordering is consistent with the exploratory analysis "
            "and with the business intuition that the length and type of the relationship matter "
            "more than demographic attributes."
        ),
    )
    figure(
        doc,
        DECK_FIGURES / "importance.png",
        width=6.0,
        cap="Figure 10.8: Permutation importance of the top ten features",
    )
    body(
        doc,
        (
            "The engineered features add modest but real value. `IsNewCustomer` is the fifth most "
            "important feature, which confirms that the early lifecycle is a distinct risk period "
            "rather than a simple linear effect of tenure. `NumServices` is sixth, suggesting that "
            "service breadth carries information beyond the individual service flags. "
            "`AvgMonthlySpend` does not appear in the top ten, which suggests that `MonthlyCharges` "
            "and `TotalCharges` already capture most of the spending signal."
        ),
    )
    body(
        doc,
        (
            "Permutation importance measures reliance, not causation. A feature can be important "
            "because it is a proxy for an unobserved cause. Contract type, for example, may partly "
            "reflect self-selection: customers who expect to stay are more likely to sign a long "
            "contract. The model is therefore best used to prioritise and to generate hypotheses, "
            "not to prescribe interventions without further evidence."
        ),
    )

    section(doc, "10.8", "Application Screenshots")
    body(
        doc,
        (
            "The model is deployed as a Streamlit application. Figure 10.9 shows the main "
            "prediction view. The sidebar contains the customer inputs, the main panel shows the "
            "risk band, the probability gauge and the recommended actions, and the factor chips "
            "explain which attributes push the risk up or down."
        ),
    )
    figure(
        doc,
        APP_SHOTS / "risk_assessment.jpg",
        width=6.35,
        cap="Figure 10.9: Risk assessment view of the Streamlit application",
    )
    body(
        doc,
        (
            "Figure 10.10 shows the what-if simulator. The user selects an alternative contract, "
            "payment method or service configuration and the application re-scores the customer. "
            "In this example, the estimated risk falls when the customer is moved to a longer "
            "contract or an automatic payment method, which illustrates how the model can support "
            "a retention conversation."
        ),
    )
    figure(
        doc,
        APP_SHOTS / "what_if.jpg",
        width=6.2,
        cap="Figure 10.10: What-if retention simulator",
    )
    body(
        doc,
        (
            "Figure 10.11 shows the model-performance tab. It presents the headline metrics, the "
            "confusion matrix and the feature importance in a single view so that a reviewer can "
            "assess the model without leaving the application. Figure 10.12 shows the data-insights "
            "tab, which summarises the exploratory findings that motivated the feature set."
        ),
    )
    figure(
        doc,
        APP_SHOTS / "performance_charts.png",
        width=6.3,
        cap="Figure 10.11: Model performance view",
    )
    figure(
        doc,
        APP_SHOTS / "insights_charts.png",
        width=6.3,
        cap="Figure 10.12: Data insights view",
    )

    section(doc, "10.9", "Comparison with a Baseline")
    body(
        doc,
        (
            "A majority-class baseline predicts *stay* for every customer. It achieves 73.5% "
            "accuracy, zero recall, zero precision on churners and an undefined F1. The selected "
            "model has almost the same accuracy (74.0%) but a recall of 79.4% and an F1 of 0.618. "
            "The comparison shows why accuracy alone is an inadequate summary: the baseline looks "
            "respectable while providing no retention value at all."
        ),
    )
    table(
        doc,
        ["Strategy", "Accuracy", "Recall (churn)", "Precision (churn)", "F1 (churn)"],
        [
            ["Predict everyone stays", "0.735", "0.000", "0.000", "0.000"],
            ["Logistic Regression (0.50)", "0.740", "0.794", "0.506", "0.618"],
            ["Random Forest (0.50)", "0.768", "0.741", "0.546", "0.629"],
            ["Gradient Boosting (0.50)", "0.781", "0.503", "0.605", "0.549"],
        ],
        widths=[2.0, 1.0, 1.15, 1.2, 0.95],
        font_size=9.2,
        center_cols=[1, 2, 3, 4],
        first_col_bold=True,
        cap="Table 10.3: Comparison with baseline strategies",
    )

    section(doc, "10.10", "Discussion")
    body(
        doc,
        (
            "The results support three conclusions. First, churn in this dataset is predictable "
            "to a useful degree: a compact linear model achieves a ROC-AUC of 0.846 and catches "
            "about four out of five churners. Second, the strongest signals are relational rather "
            "than demographic: tenure, contract type, internet service and monthly charges "
            "dominate the importance ranking. Third, the choice of model involves a genuine "
            "trade-off between recall and precision, and the right choice depends on the cost of "
            "each type of error."
        ),
    )
    body(
        doc,
        (
            "The results also show the limits of a single snapshot. The model cannot explain why a "
            "particular customer leaves, and it cannot predict the effect of an intervention. It "
            "is a prioritisation tool that should be combined with human judgement, A/B testing "
            "and continuous monitoring. Within those limits, it provides a substantial improvement "
            "over random outreach and a transparent basis for a retention strategy."
        ),
    )


# ---------------------------------------------------------------------------
# 11. CONCLUSION
# ---------------------------------------------------------------------------
def chapter_11(doc):
    chapter(doc, 11, "CONCLUSION")

    body(
        doc,
        (
            "This report has described the design, implementation and evaluation of a customer "
            "churn prediction system built during a 45-day Data Science internship. The project "
            "began with a business problem - identifying customers at risk of leaving - and ended "
            "with a deployed application that returns a risk score, explains the factors behind "
            "it and allows a what-if analysis of retention scenarios."
        ),
    )

    section(doc, "11.1", "Summary of the Work")
    body(
        doc,
        (
            "The IBM Telco Customer Churn dataset was cleaned, explored and enriched with three "
            "interpretable features. A leakage-free preprocessing pipeline was built with "
            "scikit-learn, and three classifiers were compared using stratified five-fold "
            "cross-validation. Logistic Regression achieved the highest cross-validated ROC-AUC "
            "(0.847) and was selected. On the held-out test set it achieved a ROC-AUC of 0.846, a "
            "recall of 79.4%, a precision of 50.6% and an F1 of 0.618, correctly identifying 297 "
            "of 374 churners. The model was deployed in a Streamlit application and documented in "
            "this report."
        ),
    )

    section(doc, "11.2", "Key Findings")
    numbered(
        doc,
        [
            "**Contract type is the strongest segmentation variable.** Month-to-month customers "
            "churn at 42.7%, compared with 11.3% for one-year and 2.8% for two-year contracts.",
            "**Tenure is the most important model feature.** Churners have a mean tenure of 18.0 "
            "months, compared with 37.6 months for stayers, and the new-customer indicator adds "
            "independent information.",
            "**Service and payment behaviour matter.** Fiber-optic customers and electronic-check "
            "customers show substantially higher churn than their alternatives.",
            "**Accuracy is the wrong headline metric.** A majority-class baseline is 73.5% "
            "accurate but catches no churners; the selected model has similar accuracy and a "
            "recall of 79.4%.",
            "**A simple model can be competitive.** Logistic Regression outperformed two "
            "tree-based ensembles on the selection metric while remaining interpretable and fast.",
            "**Deployment changes the conversation.** The interactive application makes the model "
            "usable by a non-technical audience and turns a probability into a retention "
            "workflow.",
        ],
        size=12,
        space_after=5,
    )

    section(doc, "11.3", "Limitations")
    body(
        doc,
        (
            "The study has several limitations. The dataset is a single cross-sectional snapshot, "
            "so the model cannot capture temporal drift or the effect of past interventions. The "
            "features are limited to account, service and billing attributes; call transcripts, "
            "network quality and competitor activity are absent. The model is evaluated at a "
            "single threshold and does not include a formal cost-benefit optimisation or "
            "probability calibration analysis. Fairness was considered qualitatively but not "
            "tested with group-level metrics. Finally, the application is a local demonstration "
            "rather than a production service with authentication, monitoring and audit logging."
        ),
    )

    section(doc, "11.4", "Future Work")
    body(doc, "Several extensions would strengthen the system:")
    bullet(
        doc,
        "**Temporal validation.** Train on earlier cohorts and test on later ones to estimate "
        "how performance decays over time and to support a retraining schedule.",
    )
    bullet(
        doc,
        "**Probability calibration.** Apply isotonic or Platt calibration and report reliability "
        "diagrams so that predicted probabilities can be used directly in financial planning.",
    )
    bullet(
        doc,
        "**Cost-sensitive thresholding.** Replace the fixed 0.50 threshold with an operating "
        "point derived from the cost of contact and the value of a retained customer.",
    )
    bullet(
        doc,
        "**Local explanations.** Add SHAP values to explain individual predictions more "
        "precisely than the current rule-based factor chips.",
    )
    bullet(
        doc,
        "**Fairness audit.** Evaluate performance and selection rates across gender and age "
        "groups, and document any disparities.",
    )
    bullet(
        doc,
        "**Production deployment.** Wrap the pipeline in a REST API, add authentication, "
        "logging, input validation and drift monitoring, and integrate the score into the "
        "retention team's workflow.",
    )
    bullet(
        doc,
        "**Causal evaluation.** Run a controlled experiment on a subset of flagged customers to "
        "measure the actual effect of each retention offer rather than relying on association.",
        space_after=8,
    )

    section(doc, "11.5", "Concluding Remarks")
    body(
        doc,
        (
            "The internship provided an opportunity to work through the complete lifecycle of a "
            "data science project: understanding a business problem, preparing messy data, "
            "selecting and validating a model, interpreting the results and delivering a usable "
            "application. The technical result - a model with a ROC-AUC of 0.846 and a recall of "
            "79.4% - is encouraging, but the more important outcome is the workflow behind it. "
            "The project demonstrates that a small, well-documented, reproducible pipeline can "
            "turn routine customer data into a decision-support tool with measurable value."
        ),
    )
    body(
        doc,
        (
            f"The work was carried out under the **{STUDENT['programme']}** at "
            f"**{STUDENT['organisation']}**, in association with **ZERO P4 Poverty**. The "
            f"experience reinforced the importance of clear communication, honest evaluation and "
            f"responsible use of data - lessons that will carry forward into professional "
            f"practice."
        ),
    )


# ---------------------------------------------------------------------------
# 12. BIBLIOGRAPHY AND REFERENCES
# ---------------------------------------------------------------------------
def chapter_12(doc):
    chapter(doc, 12, "BIBLIOGRAPHY AND REFERENCES")

    body(
        doc,
        (
            "The following sources were consulted during the project. References are listed in "
            "the order in which they are first relevant to the report, using a consistent "
            "author-title-year style."
        ),
    )

    references = [
        (
            "IBM. (2019). *Telco Customer Churn* [Data set]. IBM Cognos Analytics. "
            "https://www.ibm.com/analytics (accessed July 2026)."
        ),
        (
            "Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & "
            "Wirth, R. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*. SPSS Inc."
        ),
        (
            "Berry, M. J. A., & Linoff, G. S. (2004). *Data mining techniques: For marketing, "
            "sales, and customer relationship management* (2nd ed.). Wiley."
        ),
        (
            "Breiman, L. (2001). Random forests. *Machine Learning, 45*(1), 5–32. "
            "https://doi.org/10.1023/A:1010933404324"
        ),
        (
            "Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. "
            "*Annals of Statistics, 29*(5), 1189–1232. https://doi.org/10.1214/aos/1013203451"
        ),
        (
            "Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., "
            "et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine "
            "Learning Research, 12*, 2825–2830."
        ),
        (
            "McKinney, W. (2010). Data structures for statistical computing in Python. In "
            "*Proceedings of the 9th Python in Science Conference* (pp. 56–61)."
        ),
        (
            "Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., "
            "Cournapeau, D., et al. (2020). Array programming with NumPy. *Nature, 585*, "
            "357–362. https://doi.org/10.1038/s41586-020-2649-2"
        ),
        (
            "Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science "
            "& Engineering, 9*(3), 90–95."
        ),
        (
            "Waskom, M. L. (2021). Seaborn: Statistical data visualization. *Journal of Open "
            "Source Software, 6*(60), 3021. https://doi.org/10.21105/joss.03021"
        ),
        (
            "Streamlit. (2026). *Streamlit documentation*. https://docs.streamlit.io "
            "(accessed July 2026)."
        ),
        (
            "Neslin, S. A., Gupta, S., Kamakura, W., Lu, J., & Mason, C. H. (2006). Defection "
            "detection: Measuring and understanding the predictive accuracy of customer churn "
            "models. *Journal of Marketing Research, 43*(2), 204–211."
        ),
        (
            "Verbeke, W., Dejaeger, K., Martens, D., Hur, J., & Baesens, B. (2012). New insights "
            "into churn prediction in the telecommunication sector: A profit driven data mining "
            "approach. *European Journal of Operational Research, 218*(1), 211–229."
        ),
        (
            "Provost, F., & Fawcett, T. (2013). *Data science for business*. O'Reilly Media."
        ),
        (
            "Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The elements of statistical "
            "learning* (2nd ed.). Springer."
        ),
        (
            "James, G., Witten, D., Hastie, T., & Tibshirani, R. (2013). *An introduction to "
            "statistical learning*. Springer."
        ),
        (
            "Géron, A. (2022). *Hands-on machine learning with Scikit-Learn, Keras & TensorFlow* "
            "(3rd ed.). O'Reilly Media."
        ),
        (
            "Sculley, D., Holt, G., Golovin, D., Davydov, E., Phillips, T., Ebner, D., et al. "
            "(2015). Hidden technical debt in machine learning systems. In *Advances in Neural "
            "Information Processing Systems* (Vol. 28)."
        ),
        (
            "Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). \"Why should I trust you?\": "
            "Explaining the predictions of any classifier. In *Proceedings of the 22nd ACM "
            "SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. "
            "1135–1144)."
        ),
        (
            "Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model "
            "predictions. In *Advances in Neural Information Processing Systems* (Vol. 30)."
        ),
        (
            "Microsoft. (2026). *python-docx documentation*. https://python-docx.readthedocs.io "
            "(accessed July 2026)."
        ),
        (
            "Microsoft. (2026). *Field codes in Word*. https://support.microsoft.com "
            "(accessed July 2026)."
        ),
    ]

    for index, reference in enumerate(references, start=1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf = p.paragraph_format
        pf.left_indent = Inches(0.42)
        pf.first_line_indent = Inches(-0.42)
        pf.space_before = Pt(0)
        pf.space_after = Pt(10)
        pf.line_spacing = 1.15
        run = p.add_run(f"[{index}]  ")
        from report_style import _set_run_font, add_formatted_runs

        _set_run_font(run, size=10.5, bold=True, color=NAVY)
        add_formatted_runs(p, reference, size=10.5)
