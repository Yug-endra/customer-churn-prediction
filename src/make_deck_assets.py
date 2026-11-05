"""
Build presentation-quality charts and the system architecture diagram.

Outputs:
    reports/deck_figures/*.png
    reports/figures/12_architecture.png
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from matplotlib.patheffects import SimplePatchShadow

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data" / "Telco-Customer-Churn.csv"
METRICS = BASE / "reports" / "metrics.json"
OUT = BASE / "reports" / "deck_figures"
OUT.mkdir(parents=True, exist_ok=True)

NAVY = "#0B2545"
TEAL = "#1B7F79"
TEAL_LIGHT = "#DCEFEC"
CORAL = "#D95D39"
CORAL_LIGHT = "#F9E4DD"
GOLD = "#C9962C"
GOLD_LIGHT = "#F7EDD8"
GRAY = "#5F6B7A"
LIGHT = "#EDF1F5"
BORDER = "#D5DEE6"
WHITE = "#FFFFFF"

plt.rcParams.update(
    {
        "font.family": "Segoe UI",
        "font.size": 12,
        "axes.titlesize": 15,
        "axes.titleweight": "bold",
        "axes.labelsize": 12.5,
        "axes.labelcolor": GRAY,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "axes.edgecolor": BORDER,
        "axes.linewidth": 0.9,
        "figure.facecolor": WHITE,
        "axes.facecolor": WHITE,
        "savefig.facecolor": WHITE,
        "savefig.bbox": "tight",
        "savefig.dpi": 220,
        "axes.unicode_minus": False,
    }
)


def style(ax, grid_axis="y"):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(BORDER)
    ax.spines["bottom"].set_color(BORDER)
    ax.grid(axis=grid_axis, color="#E7ECF1", linewidth=0.8)
    ax.set_axisbelow(True)


with open(METRICS, "r", encoding="utf-8") as fh:
    metrics = json.load(fh)

df = pd.read_csv(DATA)
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# ---------------------------------------------------------------------------
# 1. Class balance donut
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5.2, 4.2))
counts = df["Churn"].value_counts().sort_index()
values = [counts[0], counts[1]]
colors = [NAVY, CORAL]
wedges, _ = ax.pie(
    values,
    colors=colors,
    startangle=90,
    counterclock=False,
    wedgeprops={"width": 0.34, "edgecolor": WHITE, "linewidth": 2},
)
ax.text(0, 0.1, "26.5%", ha="center", va="center", fontsize=30, fontweight="bold", color=CORAL)
ax.text(0, -0.2, "churned", ha="center", va="center", fontsize=12.5, color=GRAY)
ax.text(
    0,
    -1.28,
    "73.5% stayed  ·  1,869 of 7,043 customers",
    ha="center",
    va="center",
    fontsize=11.5,
    color=GRAY,
)
ax.set_aspect("equal")
fig.savefig(OUT / "balance.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 2. Churn by contract
# ---------------------------------------------------------------------------
contract = (
    df.groupby("Contract")["Churn"]
    .agg(["mean", "count"])
    .reindex(["Month-to-month", "One year", "Two year"])
)
fig, ax = plt.subplots(figsize=(7.2, 4.2))
bars = ax.bar(
    ["Month-to-month", "One year", "Two year"],
    contract["mean"] * 100,
    color=[CORAL, GOLD, TEAL],
    width=0.56,
    zorder=3,
)
for bar, rate, n in zip(bars, contract["mean"] * 100, contract["count"]):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1.4,
        f"{rate:.1f}%",
        ha="center",
        va="bottom",
        fontsize=16,
        fontweight="bold",
        color=NAVY,
    )
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() / 2,
        f"n = {n:,}",
        ha="center",
        va="center",
        fontsize=10.5,
        color=WHITE,
        fontweight="600",
    )
ax.set_ylim(0, 52)
ax.set_ylabel("Churn rate (%)")
ax.set_xlabel("")
style(ax)
fig.savefig(OUT / "contract.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 3. Tenure distribution
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.4, 4.2))
bins = np.arange(0, 78, 3)
ax.hist(
    df.loc[df["Churn"] == 0, "tenure"],
    bins=bins,
    color=NAVY,
    alpha=0.78,
    label="Stayed",
    zorder=3,
)
ax.hist(
    df.loc[df["Churn"] == 1, "tenure"],
    bins=bins,
    color=CORAL,
    alpha=0.82,
    label="Churned",
    zorder=4,
)
ax.axvline(37.6, color=NAVY, linestyle="--", linewidth=1.6, zorder=5)
ax.axvline(18.0, color=CORAL, linestyle="--", linewidth=1.6, zorder=5)
ax.text(38.4, ax.get_ylim()[1] * 0.92, "Stayers\n37.6 months", color=NAVY, fontsize=10.5, fontweight="bold")
ax.text(9.0, ax.get_ylim()[1] * 0.92, "Churners\n18.0 months", color=CORAL, fontsize=10.5, fontweight="bold")
ax.set_xlabel("Tenure (months)")
ax.set_ylabel("Number of customers")
ax.legend(frameon=False, loc="upper center", ncol=2, bbox_to_anchor=(0.5, 1.02))
style(ax)
fig.savefig(OUT / "tenure.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 4. Four behavioral drivers
# ---------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(12.2, 7.4))
specs = [
    ("InternetService", "Internet service", TEAL),
    ("PaymentMethod", "Payment method", GOLD),
    ("TechSupport", "Tech support", CORAL),
    ("OnlineSecurity", "Online security", NAVY),
]
for ax, (column, title, color) in zip(axes.flat, specs):
    rates = df.groupby(column)["Churn"].mean().sort_values(ascending=False) * 100
    labels = [str(x).replace(" (automatic)", "\n(automatic)") for x in rates.index]
    bars = ax.barh(labels, rates.values, color=color, height=0.58, zorder=3)
    for bar, value in zip(bars, rates.values):
        ax.text(
            value + 1.0,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}%",
            va="center",
            fontsize=12,
            fontweight="bold",
            color=NAVY,
        )
    ax.set_title(title, loc="left", color=NAVY, fontsize=14, pad=10)
    ax.set_xlim(0, max(rates.values) * 1.22)
    ax.set_xlabel("Churn rate (%)", fontsize=10.5)
    ax.invert_yaxis()
    style(ax, grid_axis="x")
fig.tight_layout(h_pad=2.2, w_pad=2.4)
fig.savefig(OUT / "drivers.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 5. ROC curve for the selected model
# ---------------------------------------------------------------------------
from sklearn.metrics import roc_curve
from sklearn.model_selection import train_test_split
import joblib

artifact = joblib.load(BASE / "models" / "churn_model.joblib")
model = artifact["model"]

# Rebuild the exact test split used during training.
clean = df.copy()
clean["TotalCharges"] = pd.to_numeric(clean["TotalCharges"], errors="coerce")
clean["TotalCharges"] = clean["TotalCharges"].fillna(clean["MonthlyCharges"])
service_cols = [
    "PhoneService", "MultipleLines", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
]
clean["NumServices"] = (clean[service_cols] == "Yes").sum(axis=1)
clean["AvgMonthlySpend"] = clean["TotalCharges"] / clean["tenure"].clip(lower=1)
clean["IsNewCustomer"] = (clean["tenure"] <= 6).astype(int)
clean = clean.drop(columns=["customerID"])
X = clean.drop(columns=["Churn"])
y = clean["Churn"]
_, X_test, _, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=42
)

fig, ax = plt.subplots(figsize=(6.6, 5.1))
probs = model.predict_proba(X_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, probs)
auc = metrics["best_model_metrics"]["roc_auc"]
ax.plot(fpr, tpr, color=NAVY, linewidth=2.8, label=f"Logistic Regression  ·  AUC {auc:.3f}")
ax.plot([0, 1], [0, 1], color=GRAY, linestyle="--", linewidth=1.2, label="Random guess  ·  0.500")
ax.fill_between([0, 1], [0, 1], color=LIGHT, alpha=0.55, zorder=0)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.02)
ax.set_xlabel("False positive rate")
ax.set_ylabel("True positive rate")
ax.legend(frameon=False, loc="lower right", fontsize=10.5)
style(ax, grid_axis="both")
fig.savefig(OUT / "roc.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 6. Model comparison
# ---------------------------------------------------------------------------
names = list(metrics["all_models"].keys())
short = ["Logistic\nRegression", "Random\nForest", "Gradient\nBoosting"]
cv = [metrics["all_models"][n]["cv_roc_auc_mean"] for n in names]
recall = [metrics["all_models"][n]["test"]["recall"] for n in names]
fig, ax = plt.subplots(figsize=(8.2, 4.3))
x = np.arange(len(names))
w = 0.34
b1 = ax.bar(x - w / 2, cv, w, color=NAVY, label="CV ROC-AUC", zorder=3)
b2 = ax.bar(x + w / 2, recall, w, color=TEAL, label="Test recall", zorder=3)
for bars in (b1, b2):
    for bar in bars:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.022,
            f"{bar.get_height():.3f}" if bar.get_height() < 1 else f"{bar.get_height():.1%}",
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
            color=NAVY,
        )
ax.set_xticks(x)
ax.set_xticklabels(short)
ax.set_ylim(0, 1.05)
ax.set_ylabel("Score")
ax.legend(frameon=False, ncol=2, loc="upper right")
style(ax)
fig.savefig(OUT / "compare.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 7. Confusion matrix
# ---------------------------------------------------------------------------
best_probs = model.predict_proba(X_test)[:, 1]
best_pred = (best_probs >= 0.5).astype(int)
from sklearn.metrics import confusion_matrix

matrix = confusion_matrix(y_test, best_pred)
fig, ax = plt.subplots(figsize=(5.3, 4.5))
cell_colors = [[TEAL_LIGHT, CORAL_LIGHT], [CORAL_LIGHT, TEAL]]
labels = [["TN", "FP"], ["FN", "TP"]]
for i in range(2):
    for j in range(2):
        ax.add_patch(
            plt.Rectangle((j, 1 - i), 1, 1, facecolor=cell_colors[i][j], edgecolor=WHITE, linewidth=4)
        )
        text_color = WHITE if (i == 1 and j == 1) else NAVY
        ax.text(j + 0.5, 1 - i + 0.58, f"{matrix[i, j]:,}", ha="center", va="center", fontsize=24, fontweight="bold", color=text_color)
        ax.text(j + 0.5, 1 - i + 0.28, labels[i][j], ha="center", va="center", fontsize=10.5, color=text_color, alpha=0.9)
ax.set_xlim(0, 2)
ax.set_ylim(0, 2)
ax.set_xticks([0.5, 1.5])
ax.set_yticks([1.5, 0.5])
ax.set_xticklabels(["Predicted stay", "Predicted churn"], fontsize=11)
ax.set_yticklabels(["Actually stayed", "Actually churned"], fontsize=11)
ax.tick_params(length=0)
for spine in ax.spines.values():
    spine.set_visible(False)
fig.savefig(OUT / "confusion.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 8. Permutation importance
# ---------------------------------------------------------------------------
top = pd.DataFrame(metrics["top_features"]).head(10).iloc[::-1]
fig, ax = plt.subplots(figsize=(8.4, 5.4))
bars = ax.barh(top["feature"], top["importance"], color=TEAL, height=0.6, zorder=3)
ax.errorbar(
    top["importance"],
    np.arange(len(top)),
    xerr=top["std"],
    fmt="none",
    ecolor=GRAY,
    capsize=3,
    linewidth=1,
    zorder=4,
)
for bar, value in zip(bars, top["importance"]):
    ax.text(value + 0.0012, bar.get_y() + bar.get_height() / 2, f"{value:.3f}", va="center", fontsize=10.5, color=GRAY)
ax.set_xlabel("Drop in ROC-AUC when the feature is shuffled")
ax.set_xlim(0, max(top["importance"]) * 1.18)
style(ax, grid_axis="x")
fig.savefig(OUT / "importance.png")
plt.close(fig)

# ---------------------------------------------------------------------------
# 9. System architecture
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13.0, 5.9))
ax.set_xlim(0, 13.0)
ax.set_ylim(0, 5.9)
ax.axis("off")

stages = [
    # x, y, number, title, detail, face, edge, text
    (0.55, 3.65, "01", "Raw data", "IBM Telco Customer Churn\n7,043 customers · 21 columns", "#F1F4F7", BORDER, NAVY),
    (4.73, 3.65, "02", "Data preparation", "Clean blanks · encode target\n3 engineered features", TEAL_LIGHT, TEAL, NAVY),
    (8.91, 3.65, "03", "Train / test split", "Stratified 80 / 20\n5,634 train · 1,409 test", "#E4EDF7", NAVY, NAVY),
    (8.91, 1.05, "04", "Model training", "Logistic Regression · Random Forest\nGradient Boosting · 5-fold CV", NAVY, NAVY, WHITE),
    (4.73, 1.05, "05", "Evaluation", "ROC-AUC · recall · precision · F1\nConfusion matrix", CORAL, CORAL, WHITE),
    (0.55, 1.05, "06", "Deployment", "Saved pipeline + Streamlit\nrisk score · what-if simulator", GOLD, GOLD, WHITE),
]
w, h = 3.55, 1.55
for x, y, number, title, detail, face, edge, text in stages:
    shadow = FancyBboxPatch(
        (x + 0.035, y - 0.045),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.14",
        facecolor="#DCE3EA",
        edgecolor="none",
        alpha=0.55,
        zorder=1,
    )
    ax.add_patch(shadow)
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.14",
        facecolor=face,
        edgecolor=edge,
        linewidth=1.2,
        zorder=2,
    )
    ax.add_patch(box)
    ax.text(x + 0.22, y + h - 0.22, number, fontsize=10, fontweight="bold", color=text, alpha=0.65, va="top")
    ax.text(x + 0.22, y + h - 0.52, title, fontsize=15, fontweight="bold", color=text, va="top")
    ax.text(x + 0.22, y + 0.26, detail, fontsize=10.2, color=text, va="bottom", linespacing=1.45, alpha=0.92)


def arrow(x1, y1, x2, y2, label=None):
    arr = FancyArrowPatch(
        (x1, y1),
        (x2, y2),
        arrowstyle="-|>",
        mutation_scale=18,
        linewidth=1.6,
        color=GRAY,
        shrinkA=0,
        shrinkB=0,
        zorder=3,
    )
    ax.add_patch(arr)


# Row 1 horizontal arrows
arrow(4.12, 4.42, 4.70, 4.42)
arrow(8.30, 4.42, 8.88, 4.42)
# Down from split to training
arrow(10.68, 3.62, 10.68, 2.66)
# Row 2 right-to-left
arrow(8.88, 1.82, 8.30, 1.82)
arrow(4.70, 1.82, 4.12, 1.82)

# Bottom artifact strip
strip = FancyBboxPatch(
    (0.55, 0.12),
    11.91,
    0.5,
    boxstyle="round,pad=0.01,rounding_size=0.08",
    facecolor="#F7F9FB",
    edgecolor=BORDER,
    linewidth=0.9,
    zorder=2,
)
ax.add_patch(strip)
ax.text(
    0.8,
    0.37,
    "Artifacts:  churn_model.joblib  ·  metrics.json  ·  model_report.txt  ·  reports/figures/  ·  Streamlit app",
    fontsize=10.2,
    color=GRAY,
    va="center",
)
fig.savefig(BASE / "reports" / "figures" / "12_architecture.png", dpi=220)
plt.close(fig)

print("Deck charts:", len(list(OUT.glob('*.png'))))
print("Architecture:", BASE / "reports" / "figures" / "12_architecture.png")
