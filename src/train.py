"""
Customer Churn Prediction - end-to-end training script.

What this script does, in order:
  1. Loads the raw Telco Customer Churn dataset.
  2. Cleans it (fixes TotalCharges, converts the target to 0/1).
  3. Creates a few business-friendly engineered features.
  4. Explores the data and saves presentation-ready charts.
  5. Trains and compares three models with 5-fold cross-validation.
  6. Evaluates the best model on a held-out test set.
  7. Saves the model, metrics and charts for the Streamlit app and slides.

Run from the project root:
    python src/train.py
"""

import json
import warnings
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

warnings.filterwarnings("ignore")

RANDOM_STATE = 42
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Telco-Customer-Churn.csv"
FIGURE_DIR = BASE_DIR / "reports" / "figures"
MODEL_DIR = BASE_DIR / "models"
REPORT_DIR = BASE_DIR / "reports"

FIGURE_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.bbox"] = "tight"
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.titleweight"] = "bold"

NUMERIC_FEATURES = [
    "SeniorCitizen",
    "tenure",
    "MonthlyCharges",
    "TotalCharges",
    "NumServices",
    "AvgMonthlySpend",
    "IsNewCustomer",
]

CATEGORICAL_FEATURES = [
    "gender",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
]


# ---------------------------------------------------------------------------
# 1. Data loading and cleaning
# ---------------------------------------------------------------------------
def load_and_clean(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)

    # TotalCharges is stored as text and has 11 blank values, all for
    # brand-new customers with tenure = 0. Convert to numbers and fill
    # those blanks with their monthly charge (a sensible first bill).
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"])

    # Target: Yes -> 1 (churned), No -> 0 (stayed)
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

    # customerID is a random identifier with no predictive value.
    df = df.drop(columns=["customerID"])

    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add three simple features a business audience can understand."""
    df = df.copy()

    service_cols = [
        "PhoneService",
        "MultipleLines",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
    ]
    df["NumServices"] = (df[service_cols] == "Yes").sum(axis=1)
    df["AvgMonthlySpend"] = df["TotalCharges"] / df["tenure"].clip(lower=1)
    df["IsNewCustomer"] = (df["tenure"] <= 6).astype(int)

    return df


# ---------------------------------------------------------------------------
# 2. Exploratory data analysis
# ---------------------------------------------------------------------------
def save_eda_charts(df: pd.DataFrame) -> dict:
    insights = {}

    churn_rate = df["Churn"].mean()
    insights["overall_churn_rate"] = round(float(churn_rate) * 100, 1)

    # Chart 1: class balance
    fig, ax = plt.subplots(figsize=(6, 4))
    counts = df["Churn"].value_counts().sort_index()
    bars = ax.bar(["Stayed", "Churned"], counts.values, color=["#2E86AB", "#E4572E"])
    for bar, count in zip(bars, counts.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 60,
            f"{count:,}\n({count / len(df):.1%})",
            ha="center",
            va="bottom",
            fontweight="bold",
        )
    ax.set_title("Customer Churn Is Imbalanced: About 1 in 4 Leaves")
    ax.set_ylabel("Number of customers")
    ax.set_ylim(0, counts.max() * 1.22)
    sns.despine()
    fig.savefig(FIGURE_DIR / "01_churn_balance.png")
    plt.close(fig)

    # Chart 2: contract type is the strongest single signal
    contract = (
        df.groupby("Contract")["Churn"]
        .agg(["mean", "count"])
        .reindex(["Month-to-month", "One year", "Two year"])
    )
    insights["churn_by_contract"] = {
        k: round(float(v) * 100, 1) for k, v in contract["mean"].items()
    }
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(
        contract.index,
        contract["mean"] * 100,
        color=["#E4572E", "#F3A712", "#2E86AB"],
    )
    for bar, rate, n in zip(bars, contract["mean"] * 100, contract["count"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.2,
            f"{rate:.1f}%\n(n={n:,})",
            ha="center",
            fontweight="bold",
        )
    ax.set_title("Month-to-Month Customers Churn Far More Often")
    ax.set_ylabel("Churn rate (%)")
    ax.set_ylim(0, 55)
    sns.despine()
    fig.savefig(FIGURE_DIR / "02_churn_by_contract.png")
    plt.close(fig)

    # Chart 3: tenure distribution
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(
        data=df,
        x="tenure",
        hue="Churn",
        bins=30,
        palette={0: "#2E86AB", 1: "#E4572E"},
        alpha=0.65,
        ax=ax,
    )
    ax.set_title("New Customers Are the Highest-Risk Group")
    ax.set_xlabel("Tenure (months)")
    ax.set_ylabel("Number of customers")
    handles = [
        plt.Rectangle((0, 0), 1, 1, color="#2E86AB", alpha=0.65),
        plt.Rectangle((0, 0), 1, 1, color="#E4572E", alpha=0.65),
    ]
    ax.legend(handles, ["Stayed", "Churned"], title="Outcome", frameon=True)
    sns.despine()
    fig.savefig(FIGURE_DIR / "03_tenure_distribution.png")
    plt.close(fig)

    # Chart 4: monthly charges
    fig, ax = plt.subplots(figsize=(6.5, 4))
    sns.boxplot(
        data=df,
        x="Churn",
        y="MonthlyCharges",
        palette=["#2E86AB", "#E4572E"],
        width=0.5,
        ax=ax,
    )
    ax.set_xticklabels(["Stayed", "Churned"])
    ax.set_title("Churners Pay More per Month on Average")
    ax.set_xlabel("")
    ax.set_ylabel("Monthly charges (USD)")
    sns.despine()
    fig.savefig(FIGURE_DIR / "04_monthly_charges.png")
    plt.close(fig)

    # Chart 5: four drivers in one figure
    fig, axes = plt.subplots(2, 2, figsize=(12, 8.5))
    driver_specs = [
        ("InternetService", "Internet service"),
        ("PaymentMethod", "Payment method"),
        ("TechSupport", "Tech support"),
        ("OnlineSecurity", "Online security"),
    ]
    colors = ["#2E86AB", "#F3A712", "#E4572E", "#6A4C93"]
    for ax, (column, title), color in zip(axes.flat, driver_specs, colors):
        rates = df.groupby(column)["Churn"].mean().sort_values(ascending=False) * 100
        sns.barplot(
            x=rates.values,
            y=rates.index,
            ax=ax,
            color=color,
            orient="h",
        )
        for i, value in enumerate(rates.values):
            ax.text(value + 0.8, i, f"{value:.1f}%", va="center", fontweight="bold")
        ax.set_title(title)
        ax.set_xlabel("Churn rate (%)")
        ax.set_ylabel("")
        ax.set_xlim(0, max(rates.values) * 1.28)
    fig.suptitle("Behavioral Drivers of Churn", fontsize=15, fontweight="bold", y=1.01)
    fig.tight_layout()
    fig.savefig(FIGURE_DIR / "05_churn_drivers.png")
    plt.close(fig)

    # Chart 6: correlation heatmap of numeric features
    numeric_cols = [
        "SeniorCitizen",
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
        "NumServices",
        "AvgMonthlySpend",
        "IsNewCustomer",
        "Churn",
    ]
    fig, ax = plt.subplots(figsize=(8, 6.5))
    corr = df[numeric_cols].corr()
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="RdBu_r",
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
        ax=ax,
    )
    ax.set_title("Correlation Between Numeric Features")
    fig.savefig(FIGURE_DIR / "06_correlation_heatmap.png")
    plt.close(fig)

    # Save textual insights for the report
    insights["avg_tenure_churned"] = round(
        float(df.loc[df["Churn"] == 1, "tenure"].mean()), 1
    )
    insights["avg_tenure_stayed"] = round(
        float(df.loc[df["Churn"] == 0, "tenure"].mean()), 1
    )
    insights["avg_monthly_churned"] = round(
        float(df.loc[df["Churn"] == 1, "MonthlyCharges"].mean()), 2
    )
    insights["avg_monthly_stayed"] = round(
        float(df.loc[df["Churn"] == 0, "MonthlyCharges"].mean()), 2
    )
    insights["churn_by_internet"] = {
        k: round(float(v) * 100, 1)
        for k, v in df.groupby("InternetService")["Churn"].mean().items()
    }
    insights["churn_by_payment"] = {
        k: round(float(v) * 100, 1)
        for k, v in df.groupby("PaymentMethod")["Churn"].mean().items()
    }

    with open(REPORT_DIR / "eda_insights.json", "w", encoding="utf-8") as fh:
        json.dump(insights, fh, indent=2)

    return insights


# ---------------------------------------------------------------------------
# 3. Model building
# ---------------------------------------------------------------------------
def build_preprocessor() -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    return ColumnTransformer(
        [
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )


def build_models() -> dict:
    return {
        "Logistic Regression": LogisticRegression(
            max_iter=3000,
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=400,
            max_depth=10,
            min_samples_leaf=3,
            class_weight="balanced_subsample",
            n_jobs=-1,
            random_state=RANDOM_STATE,
        ),
        "Gradient Boosting": HistGradientBoostingClassifier(
            max_iter=300,
            learning_rate=0.08,
            max_leaf_nodes=31,
            random_state=RANDOM_STATE,
        ),
    }


def evaluate(model, X_test, y_test) -> dict:
    probabilities = model.predict_proba(X_test)[:, 1]
    predictions = (probabilities >= 0.5).astype(int)
    return {
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "precision": round(float(precision_score(y_test, predictions)), 4),
        "recall": round(float(recall_score(y_test, predictions)), 4),
        "f1": round(float(f1_score(y_test, predictions)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, probabilities)), 4),
        "pr_auc": round(float(average_precision_score(y_test, probabilities)), 4),
    }


# ---------------------------------------------------------------------------
# 4. Main pipeline
# ---------------------------------------------------------------------------
def main() -> None:
    print("[1/7] Loading and cleaning data...")
    raw = pd.read_csv(DATA_PATH)
    print(f"      Raw shape: {raw.shape[0]:,} rows x {raw.shape[1]} columns")

    df = load_and_clean(DATA_PATH)
    df = add_features(df)
    print(f"      Clean shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"      Churn rate: {df['Churn'].mean():.1%}")

    print("[2/7] Running EDA and saving charts...")
    insights = save_eda_charts(df)
    print(f"      Overall churn: {insights['overall_churn_rate']}%")
    print(f"      Month-to-month churn: {insights['churn_by_contract']['Month-to-month']}%")

    X = df.drop(columns=["Churn"])
    y = df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=RANDOM_STATE
    )
    print(f"[3/7] Train/test split: {len(X_train):,} train / {len(X_test):,} test")

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    models = build_models()
    results = {}
    fitted_models = {}

    print("[4/7] Training and cross-validating three models...")
    for name, estimator in models.items():
        pipeline = Pipeline(
            [("preprocessor", build_preprocessor()), ("model", estimator)]
        )
        auc_scores = cross_val_score(
            pipeline, X_train, y_train, cv=cv, scoring="roc_auc", n_jobs=-1
        )
        f1_scores = cross_val_score(
            pipeline, X_train, y_train, cv=cv, scoring="f1", n_jobs=-1
        )
        pipeline.fit(X_train, y_train)
        fitted_models[name] = pipeline
        results[name] = {
            "cv_roc_auc_mean": round(float(auc_scores.mean()), 4),
            "cv_roc_auc_std": round(float(auc_scores.std()), 4),
            "cv_f1_mean": round(float(f1_scores.mean()), 4),
            "test": evaluate(pipeline, X_test, y_test),
        }
        print(
            f"      {name:20s} CV ROC-AUC = {auc_scores.mean():.3f} "
            f"(+/- {auc_scores.std():.3f})"
        )

    # Pick the model with the best cross-validated ROC-AUC.
    best_name = max(results, key=lambda k: results[k]["cv_roc_auc_mean"])
    best_model = fitted_models[best_name]
    print(f"[5/7] Best model: {best_name}")

    # ROC curves for all models
    fig, ax = plt.subplots(figsize=(7, 5.5))
    colors = ["#2E86AB", "#E4572E", "#6A4C93"]
    for (name, model), color in zip(fitted_models.items(), colors):
        probs = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, probs)
        auc = results[name]["test"]["roc_auc"]
        ax.plot(fpr, tpr, label=f"{name} (AUC = {auc:.3f})", color=color, linewidth=2)
    ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="Random guess (AUC = 0.500)")
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.set_title("ROC Curves: All Three Models Beat Random Guessing")
    ax.legend(loc="lower right", frameon=True)
    sns.despine()
    fig.savefig(FIGURE_DIR / "07_roc_curves.png")
    plt.close(fig)

    # Model comparison bar chart
    fig, ax = plt.subplots(figsize=(8, 4.5))
    names = list(results.keys())
    x = np.arange(len(names))
    width = 0.36
    cv_aucs = [results[n]["cv_roc_auc_mean"] for n in names]
    test_f1s = [results[n]["test"]["f1"] for n in names]
    bars1 = ax.bar(x - width / 2, cv_aucs, width, label="CV ROC-AUC", color="#2E86AB")
    bars2 = ax.bar(x + width / 2, test_f1s, width, label="Test F1", color="#F3A712")
    for bars in (bars1, bars2):
        for bar in bars:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.012,
                f"{bar.get_height():.3f}",
                ha="center",
                fontsize=9,
                fontweight="bold",
            )
    ax.set_xticks(x)
    ax.set_xticklabels(names)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Score")
    ax.set_title("Model Comparison: ROC-AUC and F1 Score")
    ax.legend(frameon=True)
    sns.despine()
    fig.savefig(FIGURE_DIR / "08_model_comparison.png")
    plt.close(fig)

    # Confusion matrix for the best model
    probs = best_model.predict_proba(X_test)[:, 1]
    preds = (probs >= 0.5).astype(int)
    cm = confusion_matrix(y_test, preds)
    fig, ax = plt.subplots(figsize=(6.2, 5.0))
    sns.heatmap(
        cm,
        annot=True,
        fmt=",d",
        cmap="Blues",
        cbar=False,
        xticklabels=["Stayed", "Churned"],
        yticklabels=["Stayed", "Churned"],
        ax=ax,
        annot_kws={"size": 18, "fontweight": "bold"},
    )
    ax.set_title(f"Confusion Matrix - {best_name}", pad=12)
    ax.set_ylabel("Actual outcome", fontsize=12)
    ax.set_xlabel("Predicted outcome", fontsize=12)
    ax.tick_params(axis="both", labelsize=11)
    plt.setp(ax.get_yticklabels(), rotation=0, ha="right", va="center")
    fig.savefig(FIGURE_DIR / "09_confusion_matrix.png")
    plt.close(fig)

    # Permutation importance on the original features
    print("[6/7] Computing feature importance...")
    importance = permutation_importance(
        best_model,
        X_test,
        y_test,
        scoring="roc_auc",
        n_repeats=12,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    importance_df = pd.DataFrame(
        {
            "feature": X_test.columns,
            "importance": importance.importances_mean,
            "std": importance.importances_std,
        }
    ).sort_values("importance", ascending=False)

    top = importance_df.head(12).iloc[::-1]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(
        top["feature"],
        top["importance"],
        xerr=top["std"],
        color="#2E86AB",
        error_kw={"ecolor": "#555555", "capsize": 3},
    )
    ax.set_xlabel("Drop in ROC-AUC when the feature is shuffled")
    ax.set_title("What Drives the Model's Decisions?")
    sns.despine()
    fig.savefig(FIGURE_DIR / "10_feature_importance.png")
    plt.close(fig)

    # Probability distribution
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.histplot(
        probs[y_test == 0],
        bins=25,
        color="#2E86AB",
        alpha=0.6,
        label="Stayed",
        ax=ax,
    )
    sns.histplot(
        probs[y_test == 1],
        bins=25,
        color="#E4572E",
        alpha=0.6,
        label="Churned",
        ax=ax,
    )
    ax.axvline(0.5, color="black", linestyle="--", linewidth=1.5, label="Decision threshold")
    ax.set_xlabel("Predicted churn probability")
    ax.set_ylabel("Number of customers")
    ax.set_title("Predicted Probabilities Separate the Two Groups")
    ax.legend(frameon=True)
    sns.despine()
    fig.savefig(FIGURE_DIR / "11_probability_distribution.png")
    plt.close(fig)

    # Persist the winning pipeline (preprocessing + model in one object)
    model_path = MODEL_DIR / "churn_model.joblib"
    joblib.dump(
        {
            "model": best_model,
            "model_name": best_name,
            "features": list(X.columns),
            "metrics": results,
        },
        model_path,
    )

    summary = {
        "best_model": best_name,
        "best_model_metrics": results[best_name]["test"],
        "best_model_cv_roc_auc": results[best_name]["cv_roc_auc_mean"],
        "all_models": results,
        "dataset": {
            "rows": int(len(df)),
            "columns_after_feature_engineering": int(df.shape[1]),
            "churn_rate_pct": round(float(y.mean()) * 100, 1),
            "train_rows": int(len(X_train)),
            "test_rows": int(len(X_test)),
        },
        "top_features": importance_df.head(10).to_dict(orient="records"),
        "eda": insights,
    }
    with open(REPORT_DIR / "metrics.json", "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, default=float)

    # Human-readable report
    report_lines = [
        "CUSTOMER CHURN PREDICTION - MODEL REPORT",
        "=" * 42,
        f"Dataset: Telco Customer Churn ({len(df):,} customers, {y.mean():.1%} churn)",
        f"Train/test: {len(X_train):,} / {len(X_test):,} (stratified 80/20 split)",
        f"Best model: {best_name}",
        "",
        "TEST SET METRICS (threshold = 0.50)",
    ]
    for key, value in results[best_name]["test"].items():
        report_lines.append(f"  {key:12s}: {value:.3f}")
    report_lines += [
        "",
        "ALL MODELS (cross-validated ROC-AUC)",
    ]
    for name, result in results.items():
        report_lines.append(
            f"  {name:20s}: {result['cv_roc_auc_mean']:.3f} "
            f"+/- {result['cv_roc_auc_std']:.3f}"
        )
    report_lines += [
        "",
        "TOP 10 FEATURES (permutation importance)",
    ]
    for row in importance_df.head(10).itertuples():
        report_lines.append(f"  {row.feature:20s}: {row.importance:.4f}")
    report_lines += [
        "",
        "CLASSIFICATION REPORT (best model, test set)",
        classification_report(y_test, preds, target_names=["Stayed", "Churned"]),
    ]
    (REPORT_DIR / "model_report.txt").write_text(
        "\n".join(report_lines), encoding="utf-8"
    )

    print("[7/7] Saving artifacts...")
    print(f"      Model  -> {model_path}")
    print(f"      Charts -> {FIGURE_DIR}")
    print(f"      Report -> {REPORT_DIR / 'model_report.txt'}")
    print("")
    print("Done. Test metrics for the best model:")
    for key, value in results[best_name]["test"].items():
        print(f"  {key:12s}: {value:.3f}")


if __name__ == "__main__":
    main()
