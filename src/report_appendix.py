"""Appendix A: full source code listings for the internship report."""

from pathlib import Path

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

from report_config import BASE
from report_style import GRAY, NAVY, body, code_block, section, _paragraph_border, _set_run_font


FILES = [
    ("src/train.py", "Training, evaluation and figure generation"),
    ("app.py", "Streamlit application"),
    ("src/report_config.py", "Shared report configuration"),
]


def _chunk(lines, size=48):
    for start in range(0, len(lines), size):
        yield lines[start : start + size]


def build_appendix(doc):
    doc.add_page_break()

    p = doc.add_paragraph()
    run = p.add_run("APPENDIX A")
    _set_run_font(run, size=16, bold=True, color=NAVY)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    _paragraph_border(p, "bottom", "0B2545", 8, 4)

    p = doc.add_paragraph()
    run = p.add_run("SOURCE CODE")
    _set_run_font(run, size=16, bold=True, color=NAVY)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(12)

    body(
        doc,
        (
            "This appendix reproduces the source code of the project. The files are listed in the "
            "order in which they are used: data preparation and training first, then the "
            "application, then the report generators. The files in the repository are the "
            "authoritative versions; the listings here are provided for review without access to "
            "the repository."
        ),
        size=11.5,
        first_indent=0.4,
        line_spacing=1.3,
        space_after=10,
    )

    for index, (relative, description) in enumerate(FILES, start=1):
        path = BASE / relative
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        while lines and not lines[-1].strip():
            lines.pop()
        total_parts = (len(lines) + 47) // 48
        section(doc, f"A.{index}", f"{relative}  -  {description}")
        body(
            doc,
            f"{len(lines)} lines.",
            size=10,
            first_indent=0,
            space_before=2,
            space_after=4,
            color=GRAY,
        )
        for part_no, chunk in enumerate(_chunk(lines), start=1):
            cap = f"Code A.{index}: {relative}"
            if total_parts > 1:
                cap += f" (part {part_no} of {total_parts})"
            code_block(doc, chunk, cap=cap, font_size=7.2, keep_together=False)
