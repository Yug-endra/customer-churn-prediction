"""Export the slide deck to PNG images via PowerPoint COM automation."""

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PPTX = BASE / "slides" / "Customer_Churn_Prediction_Review.pptx"
OUT = BASE / "slides" / "review_png"
OUT.mkdir(parents=True, exist_ok=True)


def main():
    import win32com.client

    app = win32com.client.DispatchEx("PowerPoint.Application")
    app.Visible = True
    app.DisplayAlerts = 0
    try:
        presentation = app.Presentations.Open(str(PPTX), ReadOnly=True, WithWindow=False)
        presentation.Export(str(OUT), "PNG", 1920, 1080)
        print(f"Exported {presentation.Slides.Count} slides to {OUT}")
        presentation.Close()
    finally:
        app.Quit()


if __name__ == "__main__":
    if not PPTX.exists():
        raise SystemExit(f"Missing PPTX: {PPTX}")
    main()
