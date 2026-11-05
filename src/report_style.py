"""Formatting helpers for the internship report."""

import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

from report_config import STUDENT

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
NAVY = RGBColor(0x0B, 0x25, 0x45)
NAVY_HEX = "0B2545"
TEAL = RGBColor(0x1B, 0x7F, 0x79)
TEAL_HEX = "1B7F79"
CORAL = RGBColor(0xD9, 0x5D, 0x39)
RED = RGBColor(0xC0, 0x00, 0x00)
DARK_RED = RGBColor(0xA6, 0x1C, 0x00)
BLUE = RGBColor(0x1F, 0x4E, 0x79)
GRAY = RGBColor(0x5F, 0x6B, 0x7A)
GRAY_HEX = "5F6B7A"
LIGHT = "F4F6F8"
LIGHT_TEAL = "E6F2F1"
LIGHT_CORAL = "FBEAE4"
BORDER_HEX = "D5DEE6"
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

BODY_FONT = "Times New Roman"
CODE_FONT = "Consolas"


def _set_run_font(run, name=BODY_FONT, size=None, bold=None, italic=None, color=None):
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), name)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color is not None:
        run.font.color.rgb = color


TOKEN_RE = re.compile(r"(\*\*.+?\*\*|\*[^*\n]+?\*|`[^`\n]+?`)")


def add_formatted_runs(paragraph, text, size=12, color=None, bold=False, italic=False):
    """Add text with **bold**, *italic* and `code` spans as Word runs."""
    for part in TOKEN_RE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            run = paragraph.add_run(part[2:-2])
            _set_run_font(run, size=size, bold=True, italic=italic, color=color)
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            run = paragraph.add_run(part[1:-1])
            _set_run_font(
                run,
                name=CODE_FONT,
                size=max(size - 0.8, 8),
                bold=bold,
                italic=italic,
                color=RGBColor(0x1B, 0x2A, 0x38),
            )
        elif part.startswith("*") and part.endswith("*") and len(part) > 2:
            run = paragraph.add_run(part[1:-1])
            _set_run_font(run, size=size, bold=bold, italic=True, color=color)
        else:
            run = paragraph.add_run(part)
            _set_run_font(run, size=size, bold=bold, italic=italic, color=color)


def _add_field(paragraph, instruction):
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = instruction
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = "1"
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    run._r.append(begin)
    run._r.append(instr)
    run._r.append(separate)
    run._r.append(text)
    run._r.append(end)
    return run


def _shade_cell(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def _cell_margins(cell, top=50, bottom=50, left=90, right=90):
    tc_pr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement("w:tcMar")
    for tag, value in (("top", top), ("bottom", bottom), ("start", left), ("end", right)):
        el = OxmlElement(f"w:{tag}")
        el.set(qn("w:w"), str(value))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tc_pr.append(mar)


def _paragraph_border(paragraph, edge="bottom", color=NAVY_HEX, size=8, space=4):
    p_pr = paragraph._p.get_or_add_pPr()
    borders = p_pr.find(qn("w:pBdr"))
    if borders is None:
        borders = OxmlElement("w:pBdr")
        p_pr.append(borders)
    el = OxmlElement(f"w:{edge}")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(size))
    el.set(qn("w:space"), str(space))
    el.set(qn("w:color"), color)
    borders.append(el)


def _table_borders(table, color=BORDER_HEX, size=4):
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(size))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        borders.append(el)
    tbl_pr.append(borders)


def _fixed_layout(table, widths):
    table.autofit = False
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_pr = table._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tbl_pr.append(layout)
    tbl_w = OxmlElement("w:tblW")
    tbl_w.set(qn("w:w"), str(int(sum(widths) * 1440)))
    tbl_w.set(qn("w:type"), "dxa")
    tbl_pr.append(tbl_w)


def setup_document():
    doc = Document()
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.top_margin = Inches(0.95)
    section.bottom_margin = Inches(0.85)
    section.header_distance = Inches(0.45)
    section.footer_distance = Inches(0.4)

    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.space_after = Pt(6)
    rpr = normal.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(attr), BODY_FONT)

    h1 = doc.styles["Heading 1"]
    h1.font.name = BODY_FONT
    h1.font.size = Pt(14)
    h1.font.bold = True
    h1.font.color.rgb = NAVY
    h1.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    h1.paragraph_format.space_before = Pt(0)
    h1.paragraph_format.space_after = Pt(14)
    h1.paragraph_format.keep_with_next = True

    h2 = doc.styles["Heading 2"]
    h2.font.name = BODY_FONT
    h2.font.size = Pt(12.5)
    h2.font.bold = True
    h2.font.color.rgb = NAVY
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(6)
    h2.paragraph_format.keep_with_next = True

    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = _add_field(p, " PAGE ")
    _set_run_font(run, size=9.5, color=GRAY)
    return doc


def page_break(doc):
    doc.add_page_break()


def rich_paragraph(
    doc,
    text,
    size=12,
    color=None,
    bold=False,
    italic=False,
    align=WD_ALIGN_PARAGRAPH.JUSTIFY,
    first_indent=0.5,
    space_before=0,
    space_after=6,
    line_spacing=1.5,
    keep_with_next=False,
    style=None,
):
    p = doc.add_paragraph(style=style)
    p.alignment = align
    pf = p.paragraph_format
    pf.first_line_indent = Inches(first_indent)
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = line_spacing
    pf.keep_with_next = keep_with_next

    add_formatted_runs(
        p,
        text,
        size=size,
        color=color,
        bold=bold,
        italic=italic,
    )
    return p


def body(doc, text, **kwargs):
    return rich_paragraph(doc, text, **kwargs)


def bullet(doc, text, level=0, size=12, space_after=4):
    p = doc.add_paragraph(style="List Bullet")
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.left_indent = Inches(0.35 + 0.25 * level)
    pf.first_line_indent = Inches(-0.22)
    pf.space_before = Pt(0)
    pf.space_after = Pt(space_after)
    pf.line_spacing = 1.3
    add_formatted_runs(p, text, size=size)
    return p


def numbered(doc, items, size=12, indent=0.35, space_after=4):
    for idx, text in enumerate(items, start=1):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf = p.paragraph_format
        pf.left_indent = Inches(indent + 0.25)
        pf.first_line_indent = Inches(-0.25)
        pf.space_before = Pt(0)
        pf.space_after = Pt(space_after)
        pf.line_spacing = 1.3
        run = p.add_run(f"{idx}.  ")
        _set_run_font(run, size=size, bold=True, color=NAVY)
        add_formatted_runs(p, text, size=size)


def chapter(doc, number, title, new_page=True):
    if new_page:
        doc.add_page_break()
    p = doc.add_paragraph(style="Heading 1")
    run = p.add_run(f"{number}.  {title}")
    _set_run_font(run, size=14, bold=True, color=NAVY)
    _paragraph_border(p, "bottom", NAVY_HEX, 8, 4)
    p.paragraph_format.space_after = Pt(14)
    return p


def section(doc, number, title):
    p = doc.add_paragraph(style="Heading 2")
    run = p.add_run(f"{number}  {title}")
    _set_run_font(run, size=12.5, bold=True, color=NAVY)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(5)
    return p


def subsection(doc, number, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(f"{number}  {title}")
    _set_run_font(run, size=12, bold=True, italic=True, color=BLUE)
    return p


def caption(doc, text, space_after=10):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    _set_run_font(run, size=9.5, italic=True, color=GRAY)
    return p


def figure(doc, path, width=6.3, cap=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run()
    run.add_picture(str(Path(path)), width=Inches(width))
    if cap:
        caption(doc, cap)


def table(doc, headers, rows, widths, font_size=9.5, header_fill=NAVY_HEX,
          zebra=True, center_cols=None, first_col_bold=False, cap=None):
    center_cols = center_cols or []
    table_obj = doc.add_table(rows=1, cols=len(headers))
    table_obj.style = "Table Grid"
    _fixed_layout(table_obj, widths)
    _table_borders(table_obj)

    for idx, width in enumerate(widths):
        table_obj.columns[idx].width = Inches(width)

    header = table_obj.rows[0]
    header._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
    for idx, text in enumerate(headers):
        cell = header.cells[idx]
        cell.width = Inches(widths[idx])
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        _shade_cell(cell, header_fill)
        _cell_margins(cell)
        p = cell.paragraphs[0]
        p.alignment = (
            WD_ALIGN_PARAGRAPH.CENTER if idx in center_cols else WD_ALIGN_PARAGRAPH.LEFT
        )
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(str(text))
        _set_run_font(run, size=font_size, bold=True, color=WHITE)

    for row_idx, row in enumerate(rows, start=1):
        tr = table_obj.add_row()
        tr._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        for col_idx, text in enumerate(row):
            cell = tr.cells[col_idx]
            cell.width = Inches(widths[col_idx])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            if zebra and row_idx % 2 == 0:
                _shade_cell(cell, "F7F9FB")
            _cell_margins(cell)
            p = cell.paragraphs[0]
            p.alignment = (
                WD_ALIGN_PARAGRAPH.CENTER if col_idx in center_cols else WD_ALIGN_PARAGRAPH.LEFT
            )
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            add_formatted_runs(
                p,
                str(text),
                size=font_size,
                bold=(first_col_bold and col_idx == 0),
            )

    if cap:
        caption(doc, cap)
    return table_obj


def code_block(doc, lines, cap=None, font_size=8.2, keep_together=True):
    if cap:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(cap)
        _set_run_font(run, size=9.5, bold=True, color=NAVY)
    last = len(lines) - 1
    for idx, line in enumerate(lines):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = Inches(0.12)
        pf.right_indent = Inches(0.05)
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing = 1.0
        pf.keep_with_next = idx < last if keep_together else False
        p_pr = p._p.get_or_add_pPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), "F5F7F9")
        p_pr.append(shd)
        run = p.add_run(line if line else " ")
        _set_run_font(run, name=CODE_FONT, size=font_size, color=RGBColor(0x1B, 0x2A, 0x38))
    if last >= 0:
        doc.paragraphs[-1].paragraph_format.space_after = Pt(8)
