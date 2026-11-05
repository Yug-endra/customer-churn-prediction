"""Assemble all twelve chapters of the internship report."""

from report_chapters_a import (
    chapter_1,
    chapter_2,
    chapter_3,
    chapter_4,
    chapter_5,
    chapter_6,
)
from report_chapters_b import (
    chapter_7,
    chapter_8,
    chapter_9,
    chapter_10,
    chapter_11,
    chapter_12,
)

CHAPTER_BUILDERS = [
    chapter_1,
    chapter_2,
    chapter_3,
    chapter_4,
    chapter_5,
    chapter_6,
    chapter_7,
    chapter_8,
    chapter_9,
    chapter_10,
    chapter_11,
    chapter_12,
]


def build_chapters(doc):
    """Append chapters 1-12 to the document in order."""
    for builder in CHAPTER_BUILDERS:
        builder(doc)
