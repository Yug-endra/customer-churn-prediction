"""Shared configuration and data for the internship report."""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
REPORTS = BASE / "reports"
ASSETS = REPORTS / "assets"
FIGURES = REPORTS / "figures"
DECK_FIGURES = REPORTS / "deck_figures"
APP_SHOTS = REPORTS / "app_screens"

DOCX_PATH = REPORTS / "Customer_Churn_Prediction_Internship_Report.docx"
PDF_PATH = REPORTS / "Customer_Churn_Prediction_Internship_Report.pdf"
TOC_PATH = REPORTS / "toc_pages.json"

with open(REPORTS / "metrics.json", "r", encoding="utf-8") as fh:
    METRICS = json.load(fh)

with open(REPORTS / "eda_insights.json", "r", encoding="utf-8") as fh:
    EDA = json.load(fh)

STUDENT = {
    "name": "P. Yugendra",
    "reg_no": "239Y1A05C2",
    "degree": "BACHELOR OF TECHNOLOGY",
    "branch": "COMPUTER SCIENCE AND ENGINEERING",
    "college": "K.S.R.M. COLLEGE OF ENGINEERING",
    "college_short": "K.S.R.M. College of Engineering",
    "department": "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING",
    "address": "KADAPA, ANDHRA PRADESH",
    "academic_year": "2026 – 2027",
    "programme": "AVISHKARANA ANDHRA SUMMER INTERNSHIP",
    "organisation": "BHARAT CARE LIFE LINE FOUNDATION",
    "partner": "in association with ZERO P4 POVERTY",
    "duration": "45-Day Internship, Summer 2026",
    "issue_date": "15 August 2026",
    "coordinator": "A. Vamsi Reddy",
    "coordinator_role": "Coordinator, Bharat Care Life Line Foundation",
    "hod": "Dr. P. V. Kishore",
    "hod_role": "Associate Professor & HoD, CSE",
    "college_coordinator": "Dr. V. Lokeswara Reddy",
    "college_coordinator_role": "Professor & Internship Coordinator, CSE",
    "project_title": "Customer Churn Prediction Using Machine Learning",
    "project_short": "Customer Churn Prediction",
}

# Chapter titles used in the index and for page detection.
CHAPTERS = [
    (1, "INTRODUCTION"),
    (2, "HISTORY"),
    (3, "DEFINITION"),
    (4, "SYSTEM ARCHITECTURE"),
    (5, "APPLICATIONS"),
    (6, "TECHNOLOGIES USED"),
    (7, "ADVANTAGES AND DISADVANTAGES"),
    (8, "REQUIREMENTS"),
    (9, "METHODOLOGY AND SOURCE CODE"),
    (10, "RESULTS AND OUTPUT SCREENSHOTS"),
    (11, "CONCLUSION"),
    (12, "BIBLIOGRAPHY AND REFERENCES"),
]

INDEX_TITLES = {
    1: "Introduction",
    2: "History",
    3: "Definition",
    4: "System Architecture",
    5: "Applications",
    6: "Technologies Used",
    7: "Advantages and Disadvantages",
    8: "Requirements",
    9: "Methodology and Source Code",
    10: "Results and Output Screenshots",
    11: "Conclusion",
    12: "Bibliography and References",
}
