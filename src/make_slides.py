"""
Build the professional 18-slide internship review deck.

Run from the project root:
    python src/make_slides.py

Output:
    slides/Customer_Churn_Prediction_Review.pptx
"""

import json
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

BASE_DIR = Path(__file__).resolve().parent.parent
DECK_FIG = BASE_DIR / "reports" / "deck_figures"
APP_SHOTS = BASE_DIR / "reports" / "app_screens"
OUT = BASE_DIR / "slides" / "Customer_Churn_Prediction_Review.pptx"

with open(BASE_DIR / "reports" / "metrics.json", "r", encoding="utf-8") as fh:
    METRICS = json.load(fh)

# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------
NAVY = RGBColor(0x0B, 0x25, 0x45)
NAVY_DARK = RGBColor(0x07, 0x18, 0x30)
TEAL = RGBColor(0x1B, 0x7F, 0x79)
TEAL_LIGHT = RGBColor(0xD9, 0xEF, 0xEC)
CORAL = RGBColor(0xD9, 0x5D, 0x39)
CORAL_LIGHT = RGBColor(0xF9, 0xE4, 0xDD)
GOLD = RGBColor(0xC9, 0x96, 0x2C)
GOLD_LIGHT = RGBColor(0xF7, 0xED, 0xD8)
DARK = RGBColor(0x1B, 0x2A, 0x38)
GRAY = RGBColor(0x5F, 0x6B, 0x7A)
LIGHT_GRAY = RGBColor(0xF4, 0xF6, 0xF8)
MID_GRAY = RGBColor(0xD5, 0xDE, 0xE6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TITLE_FONT = "Georgia"
BODY_FONT = "Calibri"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def add_slide(background=WHITE):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = background
    return slide


def add_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text.strip()


def add_text(slide, x, y, w, h, text, size=18, bold=False, color=DARK,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False,
             font=BODY_FONT, spacing=None, line_spacing=None):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    if spacing:
        p.space_after = Pt(spacing)
    if line_spacing:
        p.line_spacing = line_spacing
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return box


def add_bullets(slide, x, y, w, h, items, size=17, color=DARK, spacing=8,
                bullet_color=CORAL, bullet_char="•"):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for index, item in enumerate(items):
        p = tf.paragraphs[0] if index == 0 else tf.add_paragraph()
        p.space_after = Pt(spacing)
        p.line_spacing = 1.12
        bullet = p.add_run()
        bullet.text = bullet_char + "  "
        bullet.font.name = BODY_FONT
        bullet.font.size = Pt(size)
        bullet.font.bold = True
        bullet.font.color.rgb = bullet_color
        run = p.add_run()
        run.text = item
        run.font.name = BODY_FONT
        run.font.size = Pt(size)
        run.font.color.rgb = color
    return box


def add_rect(slide, x, y, w, h, fill, line=None, radius=0.08,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(1)
    try:
        shp.shadow.inherit = False
    except Exception:
        pass
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            shp.adjustments[0] = radius
        except Exception:
            pass
    return shp


def add_header(slide, kicker, title, subtitle=None, kicker_color=CORAL):
    add_rect(slide, 0.7, 0.42, 0.55, 0.06, kicker_color, shape=MSO_SHAPE.RECTANGLE)
    add_text(slide, 0.7, 0.55, 8.0, 0.3, kicker.upper(), size=11, bold=True,
             color=kicker_color, font=BODY_FONT)
    add_text(slide, 0.7, 0.83, 12.0, 0.55, title, size=28, bold=True,
             color=NAVY, font=TITLE_FONT)
    if subtitle:
        add_text(slide, 0.7, 1.42, 12.0, 0.35, subtitle, size=13.5, color=GRAY)


def add_footer(slide, number, total=18):
    add_text(slide, 0.7, 7.12, 9.0, 0.22,
             "Customer Churn Prediction  |  Internship Project Review", size=9, color=GRAY)
    add_text(slide, 12.0, 7.12, 0.7, 0.22, f"{number} / {total}", size=9,
             color=GRAY, align=PP_ALIGN.RIGHT)


def add_kpi(slide, x, y, w, h, value, label, color=NAVY, fill=LIGHT_GRAY,
            value_size=26):
    add_rect(slide, x, y, w, h, fill, radius=0.1)
    add_text(slide, x + 0.2, y + 0.12, w - 0.4, 0.5, value, size=value_size,
             bold=True, color=color, font=TITLE_FONT)
    add_text(slide, x + 0.2, y + 0.62, w - 0.4, 0.35, label, size=10.5, color=GRAY)


def add_image_fit(slide, path, x, y, w, h, radius=0.06):
    with Image.open(path) as img:
        iw, ih = img.size
    scale = min((w * 96) / iw, (h * 96) / ih)
    nw = iw * scale / 96
    nh = ih * scale / 96
    left = x + (w - nw) / 2
    top = y + (h - nh) / 2
    pic = slide.shapes.add_picture(str(path), Inches(left), Inches(top),
                                  Inches(nw), Inches(nh))
    return pic


def add_tag(slide, x, y, w, text, fill=TEAL_LIGHT, color=TEAL):
    add_rect(slide, x, y, w, 0.3, fill, radius=0.5)
    add_text(slide, x, y + 0.04, w, 0.22, text, size=9.5, bold=True,
             color=color, align=PP_ALIGN.CENTER)


def add_callout(slide, x, y, w, h, title, body_text, fill=CORAL_LIGHT,
                title_color=CORAL):
    add_rect(slide, x, y, w, h, fill, radius=0.1)
    add_text(slide, x + 0.2, y + 0.12, w - 0.4, 0.3, title, size=12,
             bold=True, color=title_color)
    add_text(slide, x + 0.2, y + 0.42, w - 0.4, h - 0.5, body_text,
             size=11, color=DARK)


# ---------------------------------------------------------------------------
# SLIDE 1 - TITLE
# ---------------------------------------------------------------------------
slide = add_slide(NAVY)
add_rect(slide, 0, 0, 0.16, 7.5, CORAL, shape=MSO_SHAPE.RECTANGLE)
add_rect(slide, 9.0, 0, 4.333, 7.5, RGBColor(0x12, 0x35, 0x5A),
         shape=MSO_SHAPE.RECTANGLE)

add_text(slide, 0.85, 0.95, 7.5, 0.3, "DATA SCIENCE INTERNSHIP PROJECT",
         size=12, bold=True, color=GOLD)
add_text(slide, 0.85, 1.35, 8.4, 1.5, "Customer Churn\nPrediction", size=46,
         bold=True, color=WHITE, font=TITLE_FONT, line_spacing=1.0)
add_text(slide, 0.85, 3.0, 7.8, 0.75,
         "Using machine learning to find at-risk customers before they leave",
         size=20, color=RGBColor(0xD7, 0xE8, 0xF2), line_spacing=1.1)
add_rect(slide, 0.85, 3.95, 1.3, 0.05, CORAL, shape=MSO_SHAPE.RECTANGLE)
add_text(slide, 0.85, 4.15, 7.5, 0.3, "Presented by  P. Yugendra", size=15,
         bold=True, color=WHITE)
add_text(slide, 0.85, 4.5, 7.5, 0.3, "Regd. No.: 239Y1A05C2", size=12,
         color=RGBColor(0xB9, 0xD3, 0xE3))
add_text(slide, 0.85, 4.85, 7.5, 0.3,
         "45-Day Data Science Internship  |  Avishkarana Andhra Summer Internship",
         size=12, color=RGBColor(0xB9, 0xD3, 0xE3))
add_text(slide, 0.85, 5.2, 7.5, 0.3,
         "Bharat Care Life Line Foundation  (in association with ZERO P4 Poverty)",
         size=12, color=RGBColor(0xB9, 0xD3, 0xE3))
add_text(slide, 0.85, 5.55, 7.5, 0.3,
         "K.S.R.M. College of Engineering, Kadapa  |  2026 - 2027", size=11,
         color=RGBColor(0xB9, 0xD3, 0xE3))

add_tag(slide, 0.85, 6.25, 1.3, "Python", fill=RGBColor(0x1F, 0x55, 0x7E),
        color=WHITE)
add_tag(slide, 2.25, 6.25, 1.5, "scikit-learn", fill=RGBColor(0x1F, 0x55, 0x7E),
        color=WHITE)
add_tag(slide, 3.85, 6.25, 1.3, "Streamlit", fill=RGBColor(0x1F, 0x55, 0x7E),
        color=WHITE)

# Headline block
add_text(slide, 9.6, 1.35, 3.0, 0.3, "HEADLINE RESULT", size=10, bold=True,
         color=GOLD)
add_text(slide, 9.6, 1.7, 3.0, 1.0, "0.846", size=52, bold=True, color=WHITE,
         font=TITLE_FONT)
add_text(slide, 9.6, 2.75, 3.0, 0.3, "ROC-AUC on unseen customers", size=12,
         color=RGBColor(0xD7, 0xE8, 0xF2))
add_rect(slide, 9.6, 3.25, 2.8, 0.02, RGBColor(0x3F, 0x6F, 0x93),
         shape=MSO_SHAPE.RECTANGLE)
add_text(slide, 9.6, 3.5, 3.0, 0.7, "79.4%", size=34, bold=True, color=WHITE,
         font=TITLE_FONT)
add_text(slide, 9.6, 4.15, 3.0, 0.4, "of actual churners caught", size=11.5,
         color=RGBColor(0xD7, 0xE8, 0xF2))
add_rect(slide, 9.6, 4.7, 2.8, 0.02, RGBColor(0x3F, 0x6F, 0x93),
         shape=MSO_SHAPE.RECTANGLE)
add_text(slide, 9.6, 4.95, 3.0, 0.7, "7,043", size=34, bold=True, color=WHITE,
         font=TITLE_FONT)
add_text(slide, 9.6, 5.6, 3.0, 0.4, "customer records analysed", size=11.5,
         color=RGBColor(0xD7, 0xE8, 0xF2))

add_notes(slide, """
Good morning, everyone. I am Yugendra Pujari, and this is my 45-day Data Science internship
project on customer churn prediction. The goal is simple: can we identify customers who are
likely to leave before they actually do, and explain what to do about it?

I built the full pipeline - cleaning, exploration, feature engineering, model comparison,
evaluation, and a live web app. The headline result is a ROC-AUC of 0.846, and the model
catches about 79 percent of customers who actually churn.
""")

# ---------------------------------------------------------------------------
# SLIDE 2 - AGENDA
# ---------------------------------------------------------------------------
slide = add_slide()
add_header(slide, "Agenda", "What we will cover",
          "From the business question to a working demo, in six steps.")
items = [
    ("01", "The business problem", "Why churn matters and what we are trying to predict"),
    ("02", "The data", "7,043 telecom customers and their behaviour"),
    ("03", "Methodology", "Cleaning, features, models and validation"),
    ("04", "Key insights", "What the exploratory analysis revealed"),
    ("05", "Results", "Model performance and the accuracy trap"),
    ("06", "Demo & recommendations", "Turning predictions into retention actions"),
]
for idx, (number, title, desc) in enumerate(items):
    col = idx % 2
    row = idx // 2
    x = 0.7 + col * 6.15
    y = 1.95 + row * 1.6
    add_rect(slide, x, y, 5.8, 1.35, LIGHT_GRAY, radius=0.1)
    add_text(slide, x + 0.25, y + 0.18, 0.6, 0.5, number, size=24, bold=True,
             color=CORAL, font=TITLE_FONT)
    add_text(slide, x + 0.9, y + 0.18, 4.6, 0.35, title, size=16, bold=True,
             color=NAVY)
    add_text(slide, x + 0.9, y + 0.6, 4.6, 0.55, desc, size=11.5, color=GRAY)
add_footer(slide, 2)
add_notes(slide, """
Here is the plan. I will start with the business problem, then the data and methodology.
Then the key insights, the model results, and a live demo of the app. I will finish with
recommendations, limitations, and next steps.
""")

# ---------------------------------------------------------------------------
# SLIDE 3 - PROBLEM
# ---------------------------------------------------------------------------
slide = add_slide()
add_header(slide, "The business problem",
           "Every lost customer is revenue walking out the door",
           "Retention teams cannot call everyone. They need a ranked list of who is most at risk.")
add_bullets(slide, 0.7, 1.95, 7.1, 3.4, [
    "Acquiring a new customer usually costs more than retaining an existing one.",
    "In this dataset, about 1 in 4 customers churned - 26.5% of the customer base.",
    "Retention cannot be reactive: by the time a customer leaves, the revenue is gone.",
    "A churn model is useful only if it is early, explainable and tied to an action.",
    "So the project answers three questions: who is at risk, why, and what can we do?",
], size=16.5, spacing=12)
add_callout(slide, 8.3, 2.1, 4.3, 2.6, "The cost of inaction",
            "A retention team with capacity for a few hundred calls per week, applied at "
            "random, would reach about 156 of the 374 churners in the test set. The model "
            "reaches 297 - roughly double the yield for the same effort.",
            fill=CORAL_LIGHT, title_color=CORAL)
add_footer(slide, 3)
add_notes(slide, """
Telecom is highly competitive. Switching is easy and acquisition is expensive, so retention is
the priority. About one in four customers churned in this data. The value of the model is not
just a score: it is a ranked work queue plus an explanation of why, so the right intervention
can be chosen. Random outreach would catch about 156 of the 374 churners; the model catches
297 for the same effort.
""")

# ---------------------------------------------------------------------------
# SLIDE 4 - DATASET
# ---------------------------------------------------------------------------
slide = add_slide()
add_header(slide, "The data", "IBM Telco Customer Churn - 7,043 customers, 21 attributes",
           "A public, realistic benchmark combining demographics, services, contract and billing.")
add_kpi(slide, 0.7, 1.95, 2.6, 1.0, "7,043", "customers", color=NAVY)
add_kpi(slide, 3.45, 1.95, 2.6, 1.0, "26.5%", "churn rate", color=CORAL)
add_kpi(slide, 6.2, 1.95, 2.6, 1.0, "21", "raw columns", color=TEAL)
add_kpi(slide, 8.95, 1.95, 2.6, 1.0, "5,634", "training rows", color=GOLD)
add_bullets(slide, 0.7, 3.15, 6.0, 3.6, [
    "Demographics: gender, senior citizen, partner, dependents.",
    "Account: tenure, contract type, paperless billing, payment method.",
    "Services: phone, multiple lines, internet, security, backup, protection, support, streaming.",
    "Billing: monthly charges, total charges.",
    "Target: Churn (Yes / No).",
    "After cleaning and feature engineering: 22 predictors.",
], size=15, spacing=8)
add_callout(slide, 7.2, 3.15, 5.4, 3.6, "Why this dataset",
            "Small enough to train on a laptop, rich enough to demonstrate a complete machine "
            "learning workflow, and widely used so results can be compared with other studies. "
            "It is synthetic but realistic, which is ideal for a teaching and internship project.",
            fill=TEAL_LIGHT, title_color=TEAL)
add_footer(slide, 4)
add_notes(slide, """
The dataset has 7,043 customers and 21 columns. Each row is one customer at the snapshot date.
It is imbalanced: 26.5 percent churned. The columns group into demographics, account, services,
billing and the target. After cleaning and feature engineering we have 22 predictors. The
dataset is a public IBM sample, realistic and small enough to run on a laptop.
""")

# ---------------------------------------------------------------------------
# SLIDE 5 - INSIGHTS 1
# ---------------------------------------------------------------------------
slide = add_slide()
add_header(slide, "Key insight 1", "Contract and tenure are the strongest signals",
           "Month-to-month customers churn far more often, and new customers are the highest-risk group.")
add_image_fit(slide, DECK_FIG / "contract.png", 0.7, 1.9, 6.0, 4.9)
add_image_fit(slide, DECK_FIG / "tenure.png", 6.85, 1.9, 5.8, 4.9)
add_footer(slide, 5)
add_notes(slide, """
Two findings dominate. First, contract type: 42.7 percent of month-to-month customers churn,
versus 11.3 percent on one-year and 2.8 percent on two-year contracts. Second, tenure: churners
have a mean tenure of 18 months against 37.6 for stayers. The first year is the critical retention
window. These are associations, not proof of causation, but they motivate both the features and
the retention strategy.
""")

# ---------------------------------------------------------------------------
# SLIDE 6 - INSIGHTS 2
# ---------------------------------------------------------------------------
slide = add_slide()
add_header(slide, "Key insight 2", "Service and payment behaviour also matter",
           "Fiber-optic customers and electronic-check customers churn at roughly double the rate.")
add_image_fit(slide, DECK_FIG / "drivers.png", 0.7, 1.9, 7.0, 5.0)
add_callout(slide, 8.0, 2.1, 4.6, 2.0, "Fiber optic", "41.9% churn vs 19.0% DSL and 7.4% no internet",
            fill=CORAL_LIGHT, title_color=CORAL)
add_callout(slide, 8.0, 4.3, 4.6, 2.0, "Electronic check", "45.3% churn vs 16.7% bank transfer and 15.2% credit card",
            fill=GOLD_LIGHT, title_color=GOLD)
add_footer(slide, 6)
add_notes(slide, """
Fiber-optic customers churn at 41.9 percent, compared with 19 percent for DSL and 7.4 percent
for customers without internet. Electronic-check customers churn at 45.3 percent, versus about
15 to 17 percent for automatic payments. Customers without technical support or online security
also show higher churn. These patterns are prompts for investigation, not causal conclusions.
""")

# ---------------------------------------------------------------------------
# SLIDE 7 - METHODOLOGY
# ---------------------------------------------------------------------------
slide = add_slide()
add_header(slide, "Methodology", "A leakage-free, reproducible pipeline",
           "CRISP-DM adapted to a 45-day internship: business, data, preparation, modelling, evaluation, deployment.")
add_image_fit(slide, BASE_DIR / "reports" / "figures" / "12_architecture.png", 0.7, 1.9, 12.0, 5.0)
add_footer(slide, 7)
add_notes(slide, """
The workflow has eight stages: acquisition, cleaning, feature engineering, splitting,
preprocessing, training and selection, evaluation, and packaging. The key discipline is that the
test set is created once and never touched during model selection. All preprocessing lives inside
the saved pipeline, so training and serving use identical transformations.
""")

# ---------------------------------------------------------------------------
# SLIDE 8 - FEATURE ENGINEERING
# ---------------------------------------------------------------------------
slide = add_slide()
add_header(slide, "Feature engineering", "Three interpretable features added to the raw data",
           "Chosen because they are computable at prediction time and motivated by the EDA.")
add_bullets(slide, 0.7, 1.95, 6.0, 4.6, [
    "NumServices: count of the eight service columns equal to Yes.",
    "  Captures how embedded the customer is in the service portfolio.",
    "AvgMonthlySpend: TotalCharges divided by tenure.",
    "  Separates high spenders from long-tenured customers.",
    "IsNewCustomer: 1 if tenure is six months or less.",
    "  Captures the high-risk early lifecycle.",
], size=15, spacing=6, bullet_char="•")
add_callout(slide, 7.2, 2.1, 5.4, 2.4, "Preprocessing",
            "Numeric: median imputation and standardisation. Categorical: most-frequent "
            "imputation and one-hot encoding with unknown-category tolerance. All fitted inside "
            "each cross-validation fold.",
            fill=TEAL_LIGHT, title_color=TEAL)
add_callout(slide, 7.2, 4.7, 5.4, 2.0, "Validation",
            "Stratified 80/20 split: 5,634 training and 1,409 test customers. Stratified "
            "five-fold cross-validation on the training set only.",
            fill=GOLD_LIGHT, title_color=GOLD)
add_footer(slide, 8)
add_notes(slide, """
Three features were engineered. NumServices counts active services. AvgMonthlySpend normalises
total charges by tenure. IsNewCustomer flags the first six months, which the tenure distribution
showed to be the highest-risk period. Preprocessing uses median imputation and standardisation
for numeric features, and most-frequent imputation plus one-hot encoding for categorical ones,
all fitted inside each fold to prevent leakage.
""")

# ---------------------------------------------------------------------------
# SLIDE 9 - MODEL COMPARISON
# ---------------------------------------------------------------------------
slide = add_slide()
add_header(slide, "Model comparison", "Three classifiers, one selection rule",
           "Stratified five-fold cross-validation on the training set; test set untouched.")
# Table-like KPIs
models = [
    ("Logistic Regression", "0.8474", "0.8458", "0.7941", "0.5060", "0.6181", True),
    ("Random Forest", "0.8457", "0.8406", "0.7406", "0.5464", "0.6288", False),
    ("Gradient Boosting", "0.8267", "0.8255", "0.5027", "0.6045", "0.5489", False),
]
# header
hdr_y = 1.95
headers = ["Model", "CV ROC-AUC", "Test ROC-AUC", "Recall", "Precision", "F1"]
widths = [2.4, 1.7, 1.7, 1.3, 1.6, 1.2]
x = 0.7
for i, h in enumerate(headers):
    add_text(slide, x, hdr_y, widths[i], 0.3, h, size=11, bold=True, color=WHITE)
    x += widths[i]
add_rect(slide, 0.7, hdr_y - 0.05, sum(widths), 0.35, NAVY, radius=0.05)
# re-add header text on top
x = 0.7
for i, h in enumerate(headers):
    add_text(slide, x + 0.05, hdr_y, widths[i] - 0.1, 0.3, h, size=11, bold=True,
             color=WHITE)
    x += widths[i]
row_y = 2.35
for name, cv, test, rec, prec, f1, selected in models:
    fill = TEAL_LIGHT if selected else LIGHT_GRAY
    add_rect(slide, 0.7, row_y, sum(widths), 0.55, fill, radius=0.06)
    vals = [name, cv, test, rec, prec, f1]
    x = 0.7
    for i, v in enumerate(vals):
        col = NAVY if i == 0 else DARK
        bold = i == 0
        add_text(slide, x + 0.05, row_y + 0.12, widths[i] - 0.1, 0.3, v,
                 size=12 if i == 0 else 12, bold=bold, color=col)
        x += widths[i]
    if selected:
        add_text(slide, 0.7 + sum(widths) + 0.15, row_y + 0.12, 1.6, 0.3,
                 "Selected", size=11, bold=True, color=TEAL)
    row_y += 0.62
add_text(slide, 0.7, 4.35, 12.0, 0.45,
         "Logistic Regression wins on cross-validated ROC-AUC (0.847) and has the highest "
         "recall (79.4%). Gradient Boosting has higher accuracy but catches only half the "
         "churners. The choice follows the stated objective: ranking quality and recall.",
         size=13, color=DARK)
add_image_fit(slide, DECK_FIG / "compare.png", 0.7, 4.85, 5.6, 2.3)
add_image_fit(slide, DECK_FIG / "roc.png", 7.0, 4.85, 5.6, 2.3)
add_footer(slide, 9)
add_notes(slide, """
Three models were compared. Logistic Regression achieved the highest cross-validated ROC-AUC
at 0.847, with Random Forest extremely close at 0.846 and Gradient Boosting lower at 0.827.
The difference between the top two is small relative to fold variation, but the selection rule was
fixed in advance. Gradient Boosting has the highest accuracy and precision but the lowest recall,
catching only about half the churners. For retention, missing a churner is usually more costly
than a false alarm, so recall wins.
""")

# ---------------------------------------------------------------------------
# SLIDE 10 - RESULTS
# ---------------------------------------------------------------------------
slide = add_slide()
add_header(slide, "Final model results", "Logistic Regression on the held-out test set",
           "Evaluated once, after model selection, on 1,409 unseen customers.")
add_kpi(slide, 0.7, 1.95, 2.3, 1.0, "0.846", "ROC-AUC", color=NAVY)
add_kpi(slide, 3.15, 1.95, 2.3, 1.0, "79.4%", "Recall", color=CORAL)
add_kpi(slide, 5.6, 1.95, 2.3, 1.0, "50.6%", "Precision", color=TEAL)
add_kpi(slide, 8.05, 1.95, 2.3, 1.0, "0.618", "F1 score", color=GOLD)
add_kpi(slide, 10.5, 1.95, 2.3, 1.0, "74.0%", "Accuracy", color=GRAY)
add_text(slide, 0.7, 3.1, 12.0, 0.4,
         "297 of the 374 churners were caught; 290 stayers were flagged; 77 churners were missed.",
         size=14, bold=True, color=DARK)
add_image_fit(slide, DECK_FIG / "confusion.png", 0.7, 3.6, 4.6, 3.4)
add_image_fit(slide, DECK_FIG / "importance.png", 5.5, 3.6, 7.1, 3.4)
add_footer(slide, 10)
add_notes(slide, """
On the held-out test set the model reached a ROC-AUC of 0.846, recall of 79.4 percent, precision
of 50.6 percent, F1 of 0.618 and accuracy of 74.0 percent. It caught 297 of the 374 churners
and flagged 290 customers who would have stayed. The confusion matrix shows the trade-off
clearly. The importance chart shows tenure, contract and internet service at the top.
""")

# ---------------------------------------------------------------------------
# SLIDE 11 - CONFUSION / ERRORS
# ---------------------------------------------------------------------------
slide = add_slide()
add_header(slide, "Error analysis", "What the model gets wrong, and why",
           "False negatives are the costly errors; false positives are the manageable ones.")
add_bullets(slide, 0.7, 1.95, 6.0, 4.6, [
    "77 missed churners (false negatives).",
    "  Likely customers whose profile resembles stayers: long tenure, two-year contract.",
    "  Their departure may be driven by factors the dataset does not capture.",
    "290 false positives.",
    "  Customers flagged who stayed. In a campaign this is an unnecessary contact, but a ",
    "  well-designed check-in can still strengthen the relationship.",
    "Threshold is a business decision.",
    "  A lower threshold catches more churners but costs more outreach.",
], size=15, spacing=6)
add_callout(slide, 7.2, 2.1, 5.4, 2.4, "Lift",
            "Contacting the 587 flagged customers reaches 297 true churners. A random sample "
            "of the same size would reach about 156. The model roughly doubles the yield.",
            fill=TEAL_LIGHT, title_color=TEAL)
add_callout(slide, 7.2, 4.7, 5.4, 2.0, "Baseline comparison",
            "Predicting 'everyone stays' is 73.5% accurate and catches zero churners. The model "
            "has similar accuracy but a recall of 79.4%.",
            fill=CORAL_LIGHT, title_color=CORAL)
add_footer(slide, 11)
add_notes(slide, """
The 77 missed churners are likely customers whose profile resembles stayers. Their departure
may be driven by factors outside the dataset, such as a competitor offer or a life event. The 290
false positives are manageable: a well-designed check-in can strengthen the relationship. The
threshold is a business decision. The lift is about 1.9: the model reaches 297 churners where
random outreach would reach about 156.
""")

# ---------------------------------------------------------------------------
# SLIDE 12 - APP DEMO 1
# ---------------------------------------------------------------------------
slide = add_slide()
add_header(slide, "The application", "Live risk score, factor explanation, recommended actions",
           "A Streamlit app that turns the model into a usable retention tool.")
add_image_fit(slide, APP_SHOTS / "risk_assessment.jpg", 0.7, 1.9, 7.6, 5.0)
add_bullets(slide, 8.5, 2.1, 4.1, 4.6, [
    "Sidebar collects all customer inputs.",
    "Risk band: low, medium or high.",
    "Probability gauge and percentage.",
    "Factor chips: risk-increasing vs risk-reducing.",
    "Recommended retention actions.",
    "Model loads from the saved artifact.",
], size=14, spacing=8)
add_footer(slide, 12)
add_notes(slide, """
The application is a Streamlit app. The sidebar collects the customer details. The main panel
shows a risk band, a probability gauge, and factor chips explaining which attributes push the
risk up or down, plus recommended actions. The model is loaded from the saved artifact, so the
displayed performance matches the report exactly.
""")

# ---------------------------------------------------------------------------
# SLIDE 13 - WHAT-IF
# ---------------------------------------------------------------------------
slide = add_slide()
add_header(slide, "What-if simulator", "Test retention scenarios before making an offer",
           "Re-score the customer under alternative contract, payment and service settings.")
add_image_fit(slide, APP_SHOTS / "what_if.jpg", 0.7, 1.9, 7.6, 5.0)
add_bullets(slide, 8.5, 2.1, 4.1, 4.6, [
    "Change contract type and see the effect.",
    "Switch payment method to automatic.",
    "Add services such as tech support.",
    "Shows original, new and difference.",
    "Supports a retention conversation.",
    "No retraining required.",
], size=14, spacing=8)
add_footer(slide, 13)
add_notes(slide, """
The what-if simulator reuses the same inference function with modified inputs. A retention
manager can test a proposed offer - a longer contract, automatic payment, added support -
and see the estimated effect before making it. This turns a probability into a concrete
retention playbook.
""")

# ---------------------------------------------------------------------------
# SLIDE 14 - APP TABS
# ---------------------------------------------------------------------------
slide = add_slide()
add_header(slide, "Application views", "Performance and insights, built in",
           "The same app reports model performance and the exploratory findings.")
add_image_fit(slide, APP_SHOTS / "performance_charts.png", 0.7, 1.9, 6.0, 5.0)
add_image_fit(slide, APP_SHOTS / "insights_charts.png", 6.85, 1.9, 5.8, 5.0)
add_footer(slide, 14)
add_notes(slide, """
The model-performance tab shows the headline metrics, confusion matrix and feature importance.
The data-insights tab summarises the exploratory findings that motivated the feature set. Both
read from the saved artifacts, so the application stays consistent with the report.
""")

# ---------------------------------------------------------------------------
# SLIDE 15 - ADVANTAGES
# ---------------------------------------------------------------------------
slide = add_slide()
add_header(slide, "Strengths", "What the system does well",
           "Practical benefits for a retention team with limited capacity.")
add_bullets(slide, 0.7, 1.95, 6.0, 4.6, [
    "Ranked work queue: roughly double the yield of random outreach.",
    "Early warning: moves the observation point before the customer leaves.",
    "Explainable: factor chips and global importance support decisions.",
    "Consistent and auditable: same logic for every customer.",
    "Low cost: open source, trains in seconds on a laptop.",
    "Extensible: same pattern applies to other binary outcomes.",
], size=15, spacing=8, bullet_color=TEAL)
add_callout(slide, 7.2, 2.1, 5.4, 2.4, "Limitations",
            "Observational data, not causal. Single snapshot, no temporal validation. "
            "Class imbalance means 290 false positives. No fairness audit. Demo, not "
            "production.",
            fill=CORAL_LIGHT, title_color=CORAL)
add_callout(slide, 7.2, 4.7, 5.4, 2.0, "Mitigations",
            "Fixed train/test split, stratified CV, pipeline-stored preprocessing, "
            "permutation importance, probability rather than verdict.",
            fill=GOLD_LIGHT, title_color=GOLD)
add_footer(slide, 15)
add_notes(slide, """
Strengths: a ranked queue that roughly doubles yield, early warning, explainability, consistency,
low cost and extensibility. Limitations: observational not causal data, a single snapshot, 290
false positives, no fairness audit, and a demo rather than a production service. Mitigations
include a fixed split, stratified CV, stored preprocessing, permutation importance, and presenting
a probability rather than a verdict.
""")

# ---------------------------------------------------------------------------
# SLIDE 16 - CONCLUSION
# ---------------------------------------------------------------------------
slide = add_slide()
add_header(slide, "Conclusion", "A complete, reproducible data science workflow",
           "From a business problem to a deployed, explainable application.")
add_bullets(slide, 0.7, 1.95, 6.0, 4.6, [
    "Cleaned and enriched 7,043 customer records with three engineered features.",
    "Compared three models under stratified cross-validation.",
    "Selected Logistic Regression: ROC-AUC 0.846, recall 79.4%.",
    "Deployed in Streamlit with risk score, explanation and what-if.",
    "Documented methodology, results and limitations.",
], size=15, spacing=8)
add_bullets(slide, 7.2, 1.95, 5.4, 4.6, [
    "Key findings:",
    "Contract and tenure dominate risk.",
    "Service and payment behaviour matter.",
    "Accuracy is the wrong headline metric.",
    "A simple model can be competitive.",
    "Deployment changes the conversation.",
], size=15, spacing=8, bullet_color=GOLD)
add_footer(slide, 16)
add_notes(slide, """
The project covered the full lifecycle: understanding the problem, preparing data, selecting and
validating a model, interpreting results, and delivering a usable application. The technical
result is encouraging, but the more important outcome is the reproducible workflow behind it.
""")

# ---------------------------------------------------------------------------
# SLIDE 17 - FUTURE WORK
# ---------------------------------------------------------------------------
slide = add_slide()
add_header(slide, "Future work", "What would make this production-ready",
           "Extensions that address the main limitations of the current study.")
add_bullets(slide, 0.7, 1.95, 6.0, 4.6, [
    "Temporal validation on later cohorts.",
    "Probability calibration and reliability diagrams.",
    "Cost-sensitive threshold from campaign economics.",
    "SHAP values for local explanations.",
    "Fairness audit across demographic groups.",
], size=15, spacing=8, bullet_color=TEAL)
add_bullets(slide, 7.2, 1.95, 5.4, 4.6, [
    "Production deployment:",
    "REST API, authentication, logging.",
    "Input validation and drift monitoring.",
    "Integration into the retention workflow.",
    "A/B test of retention offers.",
    "Causal evaluation of interventions.",
], size=15, spacing=8, bullet_color=CORAL)
add_footer(slide, 17)
add_notes(slide, """
Future work: temporal validation, probability calibration, a cost-sensitive threshold, SHAP
explanations, a fairness audit, production deployment with monitoring, and a controlled
experiment to measure the actual effect of retention offers.
""")

# ---------------------------------------------------------------------------
# SLIDE 18 - THANK YOU
# ---------------------------------------------------------------------------
slide = add_slide(NAVY)
add_rect(slide, 0, 0, 0.16, 7.5, CORAL, shape=MSO_SHAPE.RECTANGLE)
add_text(slide, 0.85, 1.6, 11.0, 0.9, "Thank You", size=56, bold=True,
         color=WHITE, font=TITLE_FONT, align=PP_ALIGN.CENTER)
add_text(slide, 0.85, 2.7, 11.0, 0.5, "Questions and Discussion", size=22,
         color=RGBColor(0xD7, 0xE8, 0xF2), align=PP_ALIGN.CENTER)
add_rect(slide, 5.4, 3.45, 2.5, 0.05, CORAL, shape=MSO_SHAPE.RECTANGLE)
add_text(slide, 0.85, 3.75, 11.0, 0.4, "P. Yugendra", size=17, bold=True,
         color=WHITE, align=PP_ALIGN.CENTER)
add_text(slide, 0.85, 4.15, 11.0, 0.3, "45-Day Data Science Internship", size=13,
         color=RGBColor(0xB9, 0xD3, 0xE3), align=PP_ALIGN.CENTER)
add_text(slide, 0.85, 4.5, 11.0, 0.3,
         "Avishkarana Andhra Summer Internship  |  Bharat Care Life Line Foundation",
         size=12, color=RGBColor(0xB9, 0xD3, 0xE3), align=PP_ALIGN.CENTER)
add_text(slide, 0.85, 4.85, 11.0, 0.3, "in association with ZERO P4 Poverty",
         size=12, color=RGBColor(0xB9, 0xD3, 0xE3), align=PP_ALIGN.CENTER)
add_text(slide, 0.85, 5.2, 11.0, 0.3,
         "K.S.R.M. College of Engineering, Kadapa  |  2026 - 2027", size=11,
         color=RGBColor(0xB9, 0xD3, 0xE3), align=PP_ALIGN.CENTER)
add_text(slide, 0.85, 6.6, 11.0, 0.3, "Customer Churn Prediction  |  ROC-AUC 0.846  |  Recall 79.4%",
         size=10, color=RGBColor(0x8F, 0xB7, 0xD1), align=PP_ALIGN.CENTER)
add_notes(slide, """
Thank you for your attention. I am happy to take questions on the methodology, the results, the
application, or the limitations of the study.
""")

prs.save(OUT)
print(f"Saved: {OUT}")
print(f"Slides: {len(prs.slides)}")
