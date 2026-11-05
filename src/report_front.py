"""Front matter: cover, certificate, vision, acknowledgement, abstract, index."""

import json

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

from report_config import (
    ASSETS,
    CHAPTERS,
    INDEX_TITLES,
    STUDENT,
    TOC_PATH,
)
from report_style import (
    BLUE,
    DARK_RED,
    GRAY,
    NAVY,
    RED,
    WHITE,
    body,
    bullet,
    caption,
    chapter,
    figure,
    page_break,
    rich_paragraph,
    section,
    table,
)


def _cover_line(doc, text, size=11, bold=False, italic=False, color=None, after=1.5, before=0):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    from report_style import _set_run_font

    _set_run_font(run, size=size, bold=bold, italic=italic, color=color)
    return p


def build_cover(doc):
    _cover_line(doc, "INTERNSHIP REPORT", size=22, bold=True, color=RED, before=2, after=8)
    _cover_line(
        doc,
        "A report submitted in partial fulfillment of the requirements for the Award of",
        size=10.5,
        italic=True,
        after=1,
    )
    _cover_line(doc, "Degree of", size=10.5, italic=True, after=4)
    _cover_line(doc, "BACHELOR OF TECHNOLOGY", size=13.5, bold=True, color=BLUE, after=3)
    _cover_line(doc, "In", size=10.5, italic=True, after=3)
    _cover_line(doc, "COMPUTER SCIENCE AND ENGINEERING", size=13.5, bold=True, color=BLUE, after=8)
    _cover_line(doc, "By", size=10.5, bold=True, after=3)
    _cover_line(doc, STUDENT["name"].upper(), size=14, bold=True, color=DARK_RED, after=2)
    _cover_line(doc, f"Regd. No.: {STUDENT['reg_no']}", size=10.5, after=8)
    _cover_line(doc, "Under Supervision of", size=10.5, bold=True, after=3)
    _cover_line(
        doc,
        STUDENT["organisation"],
        size=11.5,
        bold=True,
        color=DARK_RED,
        after=1,
    )
    _cover_line(doc, STUDENT["partner"], size=9.5, italic=True, color=GRAY, after=7)
    _cover_line(
        doc,
        f"Project Title: {STUDENT['project_title']}",
        size=11,
        bold=True,
        color=DARK_RED,
        after=2,
    )
    _cover_line(
        doc,
        f"(Duration: {STUDENT['duration']})",
        size=10,
        bold=True,
        color=DARK_RED,
        after=8,
    )

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(8)
    p.add_run().add_picture(str(ASSETS / "college_logo.jpeg"), width=Inches(1.5))

    _cover_line(doc, STUDENT["department"], size=11.5, bold=True, color=BLUE, after=3)
    _cover_line(doc, STUDENT["college"], size=17, bold=True, color=DARK_RED, after=3)
    _cover_line(doc, "(An Autonomous Institution)", size=10.5, after=2)
    _cover_line(
        doc,
        "Approved by AICTE, New Delhi & Affiliated to JNTUA, Ananthapuramu",
        size=9.5,
        after=1,
    )
    _cover_line(
        doc,
        "Accredited by NAAC with A+ Grade & B.Tech (EEE, ECE, CSE, CE and ME) Programs by NBA",
        size=9.5,
        after=3,
    )
    _cover_line(doc, STUDENT["address"], size=10.5, bold=True, after=3)
    _cover_line(doc, STUDENT["academic_year"], size=10.5, after=0)


def build_certificate(doc):
    page_break(doc)
    _cover_line(doc, STUDENT["department"], size=11.5, bold=True, after=3)
    _cover_line(doc, STUDENT["college"], size=11.5, bold=True, after=2)
    _cover_line(doc, "(An Autonomous Institution)", size=10.5, after=1)
    _cover_line(doc, "KADAPA", size=11, bold=True, after=8)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4)
    p.add_run().add_picture(str(ASSETS / "college_logo.jpeg"), width=Inches(1.25))

    _cover_line(doc, "CERTIFICATE", size=16, bold=True, italic=True, after=14)

    body(
        doc,
        (
            f'This is to certify that the Internship Report entitled **"{STUDENT["project_title"]}"** '
            f"submitted by **{STUDENT['name']}** (Regd. No.: {STUDENT['reg_no']}) is a record of "
            "work carried out during the **45-Day Data Science Internship** conducted under the "
            f"**{STUDENT['programme']}** by **{STUDENT['organisation']}**, in association with "
            f"**ZERO P4 Poverty**, from the summer of 2026, and submitted during the "
            f"**{STUDENT['academic_year']}** academic year, in partial fulfillment of the requirements "
            "for the award of the degree of **BACHELOR OF TECHNOLOGY** in **COMPUTER SCIENCE AND "
            f"ENGINEERING** at **{STUDENT['college']}, KADAPA**."
        ),
        size=11.5,
        first_indent=0.4,
        line_spacing=1.35,
        space_after=8,
    )
    body(
        doc,
        (
            f"The internship was completed under the guidance of **{STUDENT['coordinator']}**, "
            f"{STUDENT['coordinator_role']}. The certificate of achievement was issued on "
            f"**{STUDENT['issue_date']}**."
        ),
        size=11.5,
        first_indent=0.4,
        line_spacing=1.35,
        space_after=18,
    )

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)

    sig = doc.add_table(rows=3, cols=3)
    sig.autofit = False
    widths = [2.2, 2.2, 2.2]
    for i, w in enumerate(widths):
        sig.columns[i].width = Inches(w)
    data = [
        ("Internship Coordinator", "External Examiners", "Head of the Department"),
        (STUDENT["coordinator"], "", STUDENT["hod"]),
        (STUDENT["coordinator_role"], "", STUDENT["hod_role"]),
    ]
    for r, row in enumerate(data):
        for c, value in enumerate(row):
            cell = sig.cell(r, c)
            cell.width = Inches(widths[c])
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.0
            run = p.add_run(value)
            from report_style import _set_run_font

            _set_run_font(run, size=9.5, bold=(r == 0))


def build_certification(doc):
    page_break(doc)
    _cover_line(doc, "CERTIFICATION", size=16, bold=True, after=6)
    p = doc.paragraphs[-1]
    from report_style import _paragraph_border

    _paragraph_border(p, "bottom", "0B2545", 6, 2)

    body(
        doc,
        (
            "The following certificate of achievement was issued to the candidate by "
            f"**{STUDENT['organisation']}** on **{STUDENT['issue_date']}** for the successful "
            "completion of the 45-Day Internship in Data Science under the Avishkarana Andhra "
            "Summer Internship programme."
        ),
        size=11.5,
        first_indent=0.4,
        line_spacing=1.3,
        space_after=10,
    )
    figure(
        doc,
        ASSETS / "internship_certificate.jpeg",
        width=6.45,
        cap="Certificate of Achievement – 45-Day Internship in Data Science",
    )
    body(
        doc,
        (
            "The certificate is reproduced here as documentary evidence of the internship. "
            "The original document is available for verification."
        ),
        size=10.5,
        first_indent=0.4,
        line_spacing=1.2,
        color=GRAY,
    )


def build_vision(doc):
    page_break(doc)
    _cover_line(doc, STUDENT["college"], size=16, bold=True, color=RED, before=4, after=2)
    _cover_line(
        doc,
        "(An Autonomous Institution Affiliated to JNTUA, Ananthapuramu)",
        size=10,
        bold=True,
        after=1,
    )
    _cover_line(doc, "Kadapa, Andhra Pradesh, India – 516 005", size=10, bold=True, after=14)

    _cover_line(doc, "VISION", size=12, bold=True, color=RED, after=4)
    body(
        doc,
        (
            "To emerge as a centre of excellence in technical education and research, nurturing "
            "psychologically strong, socially responsible and globally competent professionals "
            "for sustainable development."
        ),
        size=11.5,
        first_indent=0,
        line_spacing=1.25,
        space_after=12,
        align=WD_ALIGN_PARAGRAPH.JUSTIFY,
    )

    _cover_line(doc, "MISSION", size=12, bold=True, color=RED, after=4)

    mission_rows = [
        (
            "M1:",
            "To provide multidisciplinary education through enriched curricula, emerging "
            "technologies and effective pedagogical practices.",
        ),
        (
            "M2:",
            "To foster research, innovation and entrepreneurship through industry–academia "
            "linkage.",
        ),
        (
            "M3:",
            "To instill leadership skills and ethical values among professionals through "
            "community engagement, contributing to the development of society and the nation.",
        ),
    ]
    for label, text in mission_rows:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.7)
        p.paragraph_format.first_line_indent = Inches(-0.4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.2
        run = p.add_run(label + "  ")
        from report_style import _set_run_font

        _set_run_font(run, size=11.5, bold=True)
        run = p.add_run(text)
        _set_run_font(run, size=11.5)

    _cover_line(
        doc,
        "DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING",
        size=12,
        bold=True,
        color=BLUE,
        before=16,
        after=8,
    )
    _cover_line(doc, "Vision", size=12, bold=True, color=RED, after=3)
    body(
        doc,
        (
            "To emerge as a centre of excellence in Computer Science and allied fields, producing "
            "technically competent professionals imbued with ethical values who drive sustainable "
            "digital transformation."
        ),
        size=11.5,
        first_indent=0,
        line_spacing=1.2,
        space_after=8,
    )
    _cover_line(doc, "Mission", size=12, bold=True, color=RED, after=3)
    dept_missions = [
        (
            "M1:",
            "To empower learners through student-centred teaching, cutting-edge technologies, and "
            "a curriculum aligned with industry needs.",
        ),
        (
            "M2:",
            "To nurture a culture of research, innovation, and entrepreneurship, and to strengthen "
            "industry–academia partnerships that address real-world and societal challenges.",
        ),
        (
            "M3:",
            "To produce technically competent graduates with strong ethical values, a sense of "
            "social responsibility, and leadership capabilities, who continue to learn and "
            "contribute to sustainable digital transformation.",
        ),
    ]
    for label, text in dept_missions:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.55)
        p.paragraph_format.first_line_indent = Inches(-0.4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.2
        run = p.add_run(label + "  ")
        _set_run_font(run, size=11.5, bold=True)
        run = p.add_run(text)
        _set_run_font(run, size=11.5)


def build_acknowledgement(doc):
    page_break(doc)
    _cover_line(doc, "ACKNOWLEDGEMENT", size=14, bold=True, before=2, after=12)

    paragraphs = [
        (
            "First and foremost, I would like to express my sincere gratitude to "
            f"**{STUDENT['organisation']}** and the **{STUDENT['programme']}** for providing me "
            "with the opportunity to undertake a 45-day internship in Data Science and to gain "
            f'practical experience through the project titled **"{STUDENT["project_title"]}."**'
        ),
        (
            "I am thankful to the ZERO P4 Poverty initiative for supporting the programme and for "
            "creating an environment in which students can apply classroom knowledge to real "
            "social and business problems."
        ),
        (
            f"I am deeply grateful to **{STUDENT['coordinator']}**, {STUDENT['coordinator_role']}, "
            "for his constant guidance, patient reviews and constructive feedback throughout the "
            "internship. His suggestions shaped both the analytical work and the final report."
        ),
        (
            "I am extremely thankful to our beloved Managing Director and Vice Chairman, "
            "**Dr. K. Chandra Obul Reddy Garu**, for his encouragement and support."
        ),
        (
            "I am highly indebted to our Principal, **Dr. T. Nageswara Prasad**, for providing the "
            "necessary facilities and support to accomplish this internship."
        ),
        (
            f"I would like to express my sincere thanks to **{STUDENT['hod']}**, Associate Professor "
            "and Head of the Department of CSE, for his constant encouragement and support "
            "throughout my academic work."
        ),
        (
            f"I am also grateful to **{STUDENT['college_coordinator']}**, Professor and Internship "
            "Coordinator, Department of CSE, for his valuable guidance in obtaining and completing "
            "this internship."
        ),
        (
            "I extend my sincere thanks to all the faculty members of the Department of Computer "
            "Science and Engineering, my friends and my family for their encouragement and help "
            "throughout the internship."
        ),
        (
            "Finally, I would like to thank everyone who directly or indirectly contributed to the "
            "successful completion of this internship."
        ),
    ]
    for text in paragraphs:
        body(
            doc,
            text,
            size=11.5,
            first_indent=0.4,
            line_spacing=1.35,
            space_after=7,
        )

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(f"Name: {STUDENT['name']}")
    from report_style import _set_run_font

    _set_run_font(run, size=11.5, bold=True)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(f"Regd. No.: {STUDENT['reg_no']}")
    _set_run_font(run, size=11.5, bold=True)


def build_abstract(doc):
    page_break(doc)
    _cover_line(doc, "ABSTRACT", size=14, bold=True, before=2, after=12)

    paragraphs = [
        (
            "Customer churn is the loss of customers who stop using a company's product or "
            "service. In subscription-based industries such as telecommunications, churn directly "
            "reduces recurring revenue and increases the cost of replacing lost customers. "
            "Retention teams, however, cannot contact every customer. They need a ranked list of "
            "who is most likely to leave, an explanation of why, and a practical way to test "
            "retention options."
        ),
        (
            "This project develops a complete machine learning system for customer churn "
            "prediction using the publicly available IBM Telco Customer Churn dataset, which "
            "contains 7,043 customers and 21 attributes covering demographics, subscribed "
            "services, contract details, billing and tenure. The data is cleaned, explored and "
            "enriched with three engineered features: the number of active services, average "
            "monthly spend and a new-customer flag. Three classification models—Logistic "
            "Regression, Random Forest and Histogram Gradient Boosting—are compared using "
            "stratified five-fold cross-validation."
        ),
        (
            "Logistic Regression achieves the best cross-validated ROC-AUC (0.847) and is selected "
            "as the final model. On a held-out test set of 1,409 customers, it reaches a ROC-AUC of "
            "0.846, a recall of 79.4%, a precision of 50.6% and an F1 score of 0.618. In practical "
            "terms, the model catches 297 of the 374 customers who actually churn. The results also "
            "show that contract type and tenure are the strongest signals: month-to-month customers "
            "churn at 42.7%, compared with 2.8% on two-year contracts."
        ),
        (
            "The selected model is deployed in an interactive Streamlit application. The application "
            "shows a customer's churn probability, explains the factors behind the score, and "
            "re-scores the customer under alternative contract, payment and service scenarios. The "
            "project demonstrates a reproducible end-to-end data science workflow—from data "
            "preparation and model selection to evaluation, interpretation and deployment—and "
            "provides a practical decision-support tool for retention planning."
        ),
    ]
    for text in paragraphs:
        body(
            doc,
            text,
            size=11.5,
            first_indent=0.4,
            line_spacing=1.4,
            space_after=8,
        )

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    run = p.add_run("Keywords: ")
    from report_style import _set_run_font

    _set_run_font(run, size=10.5, bold=True, color=NAVY)
    run = p.add_run(
        "customer churn; telecommunications; machine learning; logistic regression; "
        "ROC-AUC; recall; Streamlit; retention analytics."
    )
    _set_run_font(run, size=10.5, italic=True, color=GRAY)


def build_programmes(doc):
    page_break(doc)
    _cover_line(doc, "Programmes and Opportunities", size=13, bold=True, before=2, after=8, color=NAVY)

    body(
        doc,
        (
            "The **Avishkarana Andhra Summer Internship** is a structured summer programme that "
            "connects undergraduate students with industry and social-sector organisations for "
            "mentored, project-based learning. It gives students an opportunity to work on real "
            "problems, apply technical skills in a professional setting and understand how "
            "organisations use data to make decisions."
        ),
        size=11.5,
        first_indent=0.4,
        line_spacing=1.35,
        space_after=8,
    )
    body(
        doc,
        (
            "The 45-day Data Science internship was hosted by **Bharat Care Life Line Foundation** "
            "in association with **ZERO P4 Poverty**. The programme combined independent project "
            "work with periodic reviews, giving the intern experience in data preparation, "
            "analysis, machine learning and communication of results."
        ),
        size=11.5,
        first_indent=0.4,
        line_spacing=1.35,
        space_after=8,
    )

    _cover_line(doc, "Organization Information", size=13, bold=True, before=12, after=8, color=NAVY)
    body(
        doc,
        (
            "**Bharat Care Life Line Foundation** is a social-purpose organisation that works on "
            "community welfare, skills development and livelihood initiatives. Through its "
            "collaboration with **ZERO P4 Poverty**, it supports programmes that use education, "
            "technology and enterprise to reduce poverty and expand opportunity."
        ),
        size=11.5,
        first_indent=0.4,
        line_spacing=1.35,
        space_after=8,
    )
    body(
        doc,
        (
            "As part of the Avishkarana Andhra Summer Internship, the foundation provided the "
            "internship framework, mentorship and project review. The Data Science project "
            "described in this report was completed within that framework."
        ),
        size=11.5,
        first_indent=0.4,
        line_spacing=1.35,
        space_after=12,
    )

    _cover_line(doc, "Internship at a Glance", size=12, bold=True, before=8, after=6, color=NAVY)
    table(
        doc,
        ["Item", "Details"],
        [
            ["Programme", "Avishkarana Andhra Summer Internship"],
            ["Host organisation", "Bharat Care Life Line Foundation"],
            ["In association with", "ZERO P4 Poverty"],
            ["Domain", "Data Science"],
            ["Duration", "45 days (Summer 2026)"],
            ["Project", STUDENT["project_title"]],
            ["Coordinator", STUDENT["coordinator"]],
            ["Certificate issued", STUDENT["issue_date"]],
        ],
        widths=[1.8, 4.5],
        font_size=10,
        center_cols=[],
        first_col_bold=True,
        cap="Table F.1: Internship details",
    )


def build_benefits(doc):
    page_break(doc)
    _cover_line(
        doc,
        "Benefits to the Institution and the Host Organisation",
        size=13,
        bold=True,
        before=2,
        after=8,
        color=NAVY,
    )
    body(
        doc,
        (
            "The project offers practical value to both the host organisation and the institution. "
            "For the host organisation, it demonstrates how routinely collected customer data can "
            "be converted into a ranked retention list, an explanation of risk drivers and a "
            "simple what-if tool for planning retention offers. The same workflow can be adapted "
            "to other programmes that need to identify participants or beneficiaries at risk of "
            "disengagement."
        ),
        size=11.5,
        first_indent=0.4,
        line_spacing=1.35,
        space_after=8,
    )
    body(
        doc,
        (
            "For the institution, the report documents a complete applied data science workflow "
            "that can serve as a reference for future internships and student projects. It shows "
            "how statistical reasoning, software engineering and communication are combined in a "
            "real deliverable rather than an isolated classroom exercise."
        ),
        size=11.5,
        first_indent=0.4,
        line_spacing=1.35,
        space_after=12,
    )

    _cover_line(doc, "Learning Objectives", size=13, bold=True, before=8, after=6, color=NAVY)
    objectives = [
        "To gain practical experience in Python programming and data analysis.",
        "To clean, validate and prepare a real-world dataset for machine learning.",
        "To perform exploratory data analysis and communicate the findings clearly.",
        "To engineer interpretable features from raw customer and account data.",
        "To train, compare and validate classification models using scikit-learn.",
        "To evaluate imbalanced classification models with appropriate metrics.",
        "To interpret model behaviour and connect it to business decisions.",
        "To deploy a trained model in an interactive Streamlit application.",
        "To document the work professionally and present it to a review panel.",
    ]
    for item in objectives:
        bullet(doc, item, size=11.5, space_after=4)

    _cover_line(doc, "Expected Outcomes", size=12, bold=True, before=12, after=6, color=NAVY)
    body(
        doc,
        (
            "At the end of the internship, the candidate is expected to demonstrate a reproducible "
            "machine learning pipeline, a validated model with honest performance estimates, a "
            "working demonstration application, and a written report that explains the design "
            "choices, results and limitations of the work."
        ),
        size=11.5,
        first_indent=0.4,
        line_spacing=1.35,
        space_after=6,
    )


def build_index(doc):
    page_break(doc)
    _cover_line(doc, "INDEX", size=14, bold=True, before=2, after=12)

    if TOC_PATH.exists():
        with open(TOC_PATH, "r", encoding="utf-8") as fh:
            pages = {int(k): v for k, v in json.load(fh).items()}
    else:
        pages = {}

    rows = []
    for number, title in CHAPTERS:
        rows.append([str(number) + ".", INDEX_TITLES[number], str(pages.get(number, "—"))])

    table(
        doc,
        ["S. No.", "CONTENTS", "PAGE"],
        rows,
        widths=[0.7, 4.5, 0.9],
        font_size=10.5,
        center_cols=[0, 2],
        cap=None,
    )
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    run = p.add_run(
        "Note: page numbers refer to the printed page numbers at the bottom of each page. "
        "The index is updated after the final pagination of the report."
    )
    from report_style import _set_run_font

    _set_run_font(run, size=9, italic=True, color=GRAY)
