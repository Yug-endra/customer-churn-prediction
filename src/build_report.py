"""Build the internship report DOCX.

Run from the project root:
    python src/build_report.py
"""

import sys
from pathlib import Path

from docx.shared import Pt

BASE = Path(__file__).resolve().parent.parent
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))
if str(BASE / "src") not in sys.path:
    sys.path.insert(0, str(BASE / "src"))

from report_config import DOCX_PATH, STUDENT  # noqa: E402
from report_chapters import build_chapters  # noqa: E402
from report_front import (  # noqa: E402
    build_abstract,
    build_acknowledgement,
    build_benefits,
    build_certificate,
    build_certification,
    build_cover,
    build_index,
    build_programmes,
    build_vision,
)
from report_style import setup_document  # noqa: E402


def build():
    doc = setup_document()

    props = doc.core_properties
    props.title = STUDENT["project_title"]
    props.author = STUDENT["name"]
    props.subject = "Internship Report"
    props.keywords = "customer churn, machine learning, logistic regression, Streamlit"
    props.comments = (
        f"{STUDENT['programme']} - {STUDENT['organisation']} - "
        f"{STUDENT['duration']}"
    )

    # Front matter
    build_cover(doc)
    build_certificate(doc)
    build_certification(doc)
    build_vision(doc)
    build_acknowledgement(doc)
    build_abstract(doc)
    build_programmes(doc)
    build_benefits(doc)
    build_index(doc)

    # Chapters 1-12
    build_chapters(doc)

    DOCX_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(DOCX_PATH)

    print(f"Saved: {DOCX_PATH}")
    print(f"Paragraphs: {len(doc.paragraphs)}")
    print(f"Tables: {len(doc.tables)}")
    print(f"Inline images: {len(doc.inline_shapes)}")
    return DOCX_PATH


if __name__ == "__main__":
    build()
