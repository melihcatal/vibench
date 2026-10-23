"""
Define local request, response, and normalization helpers for OCR and Layout Extraction.
Provides dataclasses and utility functions to standardize responses across providers.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple


@dataclass
class BoundingBox:
    """Represents a bounding box with polygon vertices."""
    x_min: float = 0.0
    y_min: float = 0.0
    x_max: float = 0.0
    y_max: float = 0.0
    polygon: List[Tuple[float, float]] = field(default_factory=list)

    @classmethod
    def from_docai_vertices(cls, vertices: List[Dict[str, Any]]) -> "BoundingBox":
        """Build from Google Document AI normalized vertex list."""
        xs = [v.get("x", 0.0) for v in vertices]
        ys = [v.get("y", 0.0) for v in vertices]
        return cls(
            x_min=min(xs) if xs else 0.0,
            y_min=min(ys) if ys else 0.0,
            x_max=max(xs) if xs else 0.0,
            y_max=max(ys) if ys else 0.0,
            polygon=[(v.get("x", 0.0), v.get("y", 0.0)) for v in vertices],
        )

    @classmethod
    def from_azure_bounding(cls, bounding: List[List[float]]) -> "BoundingBox":
        """Build from Azure Document Intelligence polygon bounding."""
        xs = [p[0] for p in bounding]
        ys = [p[1] for p in bounding]
        return cls(
            x_min=min(xs) if xs else 0.0,
            y_min=min(ys) if ys else 0.0,
            x_max=max(xs) if xs else 0.0,
            y_max=max(ys) if ys else 0.0,
            polygon=[(p[0], p[1]) for p in bounding],
        )


@dataclass
class OcrWord:
    """A single OCR-recognized word."""
    text: str
    confidence: float = 1.0
    bounding_box: Optional[BoundingBox] = None


@dataclass
class OcrLine:
    """A line of text composed of multiple words."""
    text: str
    confidence: float = 1.0
    words: List[OcrWord] = field(default_factory=list)
    bounding_box: Optional[BoundingBox] = None


@dataclass
class LayoutBlock:
    """A layout block (paragraph, heading, list, etc.)."""
    block_type: str
    text: str
    confidence: float = 1.0
    bounding_box: Optional[BoundingBox] = None
    child_blocks: List["LayoutBlock"] = field(default_factory=list)


@dataclass
class TableCell:
    """A single cell within an extracted table."""
    row_index: int = 0
    column_index: int = 0
    text: str = ""
    confidence: float = 1.0
    row_span: int = 1
    column_span: int = 1
    bounding_box: Optional[BoundingBox] = None


@dataclass
class TableStructure:
    """A table with row/column metadata and cells."""
    row_count: int = 0
    column_count: int = 0
    cells: List[TableCell] = field(default_factory=list)
    bounding_box: Optional[BoundingBox] = None


@dataclass
class KeyValueEntry:
    """A key-value pair extracted from a form."""
    key: str
    value: str
    confidence: float = 1.0
    key_bounding_box: Optional[BoundingBox] = None
    value_bounding_box: Optional[BoundingBox] = None


@dataclass
class OcrDocumentResult:
    """Aggregated OCR document extraction result."""
    plain_text: str = ""
    lines: List[OcrLine] = field(default_factory=list)
    blocks: List[LayoutBlock] = field(default_factory=list)
    tables: List[TableStructure] = field(default_factory=list)
    key_value_pairs: List[KeyValueEntry] = field(default_factory=list)
    page_count: int = 0
    language: str = "en"


@dataclass
class TranslationResult:
    """Result of text translation."""
    source_language: str = ""
    target_language: str = ""
    translated_text: str = ""
    original_text: str = ""


@dataclass
class SafetyAnalysisResult:
    """Result of content safety analysis."""
    text_analyzed: str = ""
    categories: Dict[str, float] = field(default_factory=dict)
    is_safe: bool = True
    flags: List[str] = field(default_factory=list)


@dataclass
class StructuredField:
    """A structured field extracted from a document."""
    field_name: str
    value: str
    confidence: float = 1.0
    field_type: str = "string"


@dataclass
class EmbeddingResult:
    """Result of text embedding generation."""
    text: str = ""
    model: str = ""
    embedding: List[float] = field(default_factory=list)
    dimension: int = 0
    sections: List[EmbeddingResult] = field(default_factory=list)


def normalize_plain_text(raw_text: str) -> str:
    """Clean up OCR plain text: collapse whitespace, strip."""
    cleaned = re.sub(r"\s+", " ", raw_text)
    return cleaned.strip()


def lines_to_plain_text(lines: List[OcrLine]) -> str:
    """Join OcrLine objects into a single plain text string."""
    return "\n".join(line.text for line in lines)


def build_kv_dict(pairs: List[KeyValueEntry]) -> Dict[str, str]:
    """Convert key-value entry list to a simple dict."""
    return {entry.key: entry.value for entry in pairs}


def tables_to_csv(tables: List[TableStructure]) -> str:
    """Convert table structures to CSV string representation."""
    output_lines = []
    for tidx, table in enumerate(tables):
        output_lines.append(f"--- Table {tidx + 1} ---")
        grid = [[""] * table.column_count for _ in range(table.row_count)]
        for cell in table.cells:
            r = min(cell.row_index, table.row_count - 1)
            c = min(cell.column_index, table.column_count - 1)
            grid[r][c] = cell.text
        for row in grid:
            output_lines.append(",".join(f'"{v}"' for v in row))
    return "\n".join(output_lines)
