"""Export the report to PDF and detect chapter start pages for the index.

Requires Microsoft Word (COM automation). Run after building the DOCX:
    python src/export_report.py
"""

import json
import re
import sys
from pathlib import Path

import pymupdf

BASE = Path(__file__).resolve().parent.parent
if str(BASE / "src") not in sys.path:
    sys.path.insert(0, str(BASE / "src"))

from report_config import CHAPTERS, DOCX_PATH, PDF_PATH, TOC_PATH  # noqa: E402


def export_pdf():
    import win32com.client

    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        document = word.Documents.Open(str(DOCX_PATH))
        document.Repaginate()
        # Force field updates (page numbers) before exporting.
        for story in document.StoryRanges:
            story.Fields.Update()
        document.Save()
        document.ExportAsFixedFormat(
            OutputFileName=str(PDF_PATH),
            ExportFormat=17,  # wdExportFormatPDF
            OpenAfterExport=False,
            OptimizeFor=0,
            Range=0,
            Item=0,
            IncludeDocProps=True,
            KeepIRM=True,
            CreateBookmarks=1,
            DocStructureTags=True,
            BitmapMissingFonts=True,
            UseISO19005_1=False,
        )
        total = document.ComputeStatistics(2)  # wdStatisticPages
        print(f"Word reports {total} pages")
        document.Close(SaveChanges=False)
    finally:
        word.Quit()


def detect_pages():
    doc = pymupdf.open(PDF_PATH)
    page_texts = [page.get_text() for page in doc]
    print(f"PDF pages: {doc.page_count}")

    found = {}
    for number, title in CHAPTERS:
        pattern = re.compile(rf"{number}\.\s*" + r"\s+".join(map(re.escape, title.split())))
        page_no = None
        for index, text in enumerate(page_texts, start=1):
            if pattern.search(text):
                page_no = index
                break
        found[number] = page_no
        print(f"  {number:2d}. {title:<38} -> {page_no}")

    missing = [n for n, p in found.items() if p is None]
    if missing:
        print(f"WARNING: chapters not detected: {missing}")

    TOC_PATH.write_text(json.dumps(found, indent=2), encoding="utf-8")
    print(f"Saved: {TOC_PATH}")

    # Also save a small text dump for inspection.
    dump = BASE / "reports" / "report_page_text.txt"
    with open(dump, "w", encoding="utf-8") as fh:
        for index, text in enumerate(page_texts, start=1):
            fh.write(f"\n===== PAGE {index} =====\n{text}\n")
    print(f"Saved: {dump}")


if __name__ == "__main__":
    if not DOCX_PATH.exists():
        raise SystemExit(f"Missing DOCX: {DOCX_PATH}. Run src/build_report.py first.")
    export_pdf()
    detect_pages()
