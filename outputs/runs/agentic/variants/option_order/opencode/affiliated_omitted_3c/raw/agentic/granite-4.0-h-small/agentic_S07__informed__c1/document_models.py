# document_models.py
# Data models and normalization helpers for OCR and layout extraction

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class TextBlock:
    """Represents a block of text (paragraph, line, or word) extracted from a document."""

    text: str
    bounding_box: List[float] = None  # [x1, y1, x2, y2]


@dataclass
class LayoutElement:
    """Base type for any layout element (block, line, table, etc.)."""

    type_: str
    # Generic attributes can be added as needed


@dataclass
class TableCell:
    """Cell within a table layout element."""

    row_index: int
    column_index: int
    text: str
    bounding_box: List[float] = None


@dataclass
class KeyValue:
    """Key-value pair extracted from a form/document."""

    key: str
    value: str


@dataclass
class ExtractionResult:
    """General container for any extraction operation."""

    raw_output: Any  # Provider-specific raw response
    normalized: Any  # Provider-agnostic normalized structure


# Example normalization (can be expanded in each service file)
def normalize_text_extraction_response(raw):
    # Convert provider raw blocks to TextBlock list
    if isinstance(raw, list) and "Blocks" in raw[0]:
        return [
            TextBlock(block["Text"], [b.x, b.y, b.width, b.height])
            for block in raw
            if block["BlockType"] == "LINE"
        ]
    return raw


# Placeholder for other normalizations
