"""
document_models.py - Local request, response, and normalization helpers
for OCR and Layout Extraction tasks.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class BoundingBox:
    """Normalized bounding box representation."""
    x: float
    y: float
    width: float
    height: float

    def to_dict(self) -> Dict[str, float]:
        return {"x": self.x, "y": self.y, "width": self.width, "height": self.height}

    @classmethod
    def from_polygon(cls, polygon: List[float]) -> "BoundingBox":
        """Create from a flat polygon list [x0, y0, x1, y1, x2, y2, x3, y3]."""
        xs = [polygon[i] for i in range(0, len(polygon), 2)]
        ys = [polygon[i] for i in range(1, len(polygon), 2)]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        return cls(x=min_x, y=min_y, width=max_x - min_x, height=max_y - min_y)

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "BoundingBox":
        return cls(x=data["x"], y=data["y"], width=data["width"], height=data["height"])


@dataclass
class OcrTextResult:
    """Normalized result for plain text OCR extraction."""
    extracted_text: str
    language: Optional[str] = None
    confidence: float = 0.0
    lines: List[Dict[str, Any]] = field(default_factory=list)
    words: List[Dict[str, Any]] = field(default_factory=list)
    page_dimensions: Optional[Dict[str, float]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "extracted_text": self.extracted_text,
            "language": self.language,
            "confidence": self.confidence,
            "lines": self.lines,
            "words": self.words,
            "page_dimensions": self.page_dimensions,
        }


@dataclass
class LayoutBlock:
    """A single layout block (paragraph, heading, list item, etc.)."""
    content: str
    kind: str
    bounding_box: Optional[Dict[str, float]] = None
    spans: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class LayoutResult:
    """Normalized result for document layout extraction."""
    blocks: List[LayoutBlock] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    page_dimensions: Optional[Dict[str, float]] = None
    model_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "blocks": [
                {
                    "content": b.content,
                    "kind": b.kind,
                    "bounding_box": b.bounding_box,
                    "spans": b.spans,
                }
                for b in self.blocks
            ],
            "tables": self.tables,
            "page_dimensions": self.page_dimensions,
            "model_id": self.model_id,
        }


@dataclass
class TableCell:
    """A single cell within an extracted table."""
    content: str
    row_index: int
    column_index: int
    row_span: int = 1
    column_span: int = 1
    is_header: bool = False
    confidence: float = 0.0
    bounding_box: Optional[Dict[str, float]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "content": self.content,
            "row_index": self.row_index,
            "column_index": self.column_index,
            "row_span": self.row_span,
            "column_span": self.column_span,
            "is_header": self.is_header,
            "confidence": self.confidence,
            "bounding_box": self.bounding_box,
        }


@dataclass
class ExtractedTable:
    """A single table extracted from a document."""
    row_count: int
    column_count: int
    cells: List[TableCell] = field(default_factory=list)
    bounding_box: Optional[Dict[str, float]] = None
    caption: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "row_count": self.row_count,
            "column_count": self.column_count,
            "cells": [c.to_dict() for c in self.cells],
            "bounding_box": self.bounding_box,
            "caption": self.caption,
        }


@dataclass
class TableResult:
    """Normalized result for table extraction from documents."""
    tables: List[ExtractedTable] = field(default_factory=list)
    page_dimensions: Optional[Dict[str, float]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tables": [t.to_dict() for t in self.tables],
            "page_dimensions": self.page_dimensions,
        }


@dataclass
class KeyValueEntry:
    """A single key-value pair extracted from a form-like document."""
    key: str
    value: str
    confidence: float = 0.0
    bounding_box: Optional[Dict[str, float]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "value": self.value,
            "confidence": self.confidence,
            "bounding_box": self.bounding_box,
        }


@dataclass
class KeyValueResult:
    """Normalized result for key-value pair extraction."""
    key_value_pairs: List[KeyValueEntry] = field(default_factory=list)
    model_id: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_value_pairs": [kv.to_dict() for kv in self.key_value_pairs],
            "model_id": self.model_id,
        }


def normalize_azure_words_to_lines(azure_words: list) -> List[Dict[str, Any]]:
    """Convert Azure Computer Vision words into a simplified line-based format."""
    lines_map: Dict[str, List[Dict[str, Any]]] = {}
    for word in azure_words:
        text = word.get("text", "")
        bbox = word.get("bounding_box", [])
        confidence = word.get("confidence", 0.0)
        polygon = bbox if bbox else []
        entry = {
            "text": text,
            "bounding_box": BoundingBox.from_polygon(polygon).to_dict() if len(polygon) >= 8 else None,
            "confidence": confidence,
        }
        line_key = word.get("bounding_box", [0])[1] if word.get("bounding_box") else 0
        rounded_y = round(line_key, 1)
        if rounded_y not in lines_map:
            lines_map[rounded_y] = []
        lines_map[rounded_y].append(entry)

    result_lines = []
    for y_key in sorted(lines_map.keys()):
        line_text = " ".join([w["text"] for w in lines_map[y_key]])
        result_lines.append({"text": line_text, "words": lines_map[y_key], "y": y_key})
    return result_lines


def normalize_azure_kv_to_entries(azure_fields: list) -> List[KeyValueEntry]:
    """Convert Azure Document Intelligence fields to KeyValueEntry list."""
    entries = []
    for field_name, field_value in azure_fields.items():
        key = field_name
        if field_value is None:
            value = ""
            confidence = 0.0
        else:
            value = field_value.value if hasattr(field_value, "value") else str(field_value)
            confidence = field_value.confidence if hasattr(field_value, "confidence") else 0.0
        entries.append(KeyValueEntry(
            key=key,
            value=str(value) if value is not None else "",
            confidence=confidence,
        ))
    return entries


def normalize_google_table_to_cells(
    table_data: Dict[str, Any],
    header_rows: int = 1,
) -> List[TableCell]:
    """Convert Google Document AI table header/cell data to TableCell list."""
    cells = []
    rows = table_data.get("header_rows", []) + table_data.get("body_rows", [])
    for row_idx, row in enumerate(rows):
        row_cells = row.get("cells", [])
        for col_idx, cell in enumerate(row_cells):
            content = cell.get("content", "")
            is_header = row_idx < header_rows
            bbox_data = cell.get("bounding_box", {})
            confidence = cell.get("confidence", 0.0)
            cells.append(TableCell(
                content=content,
                row_index=row_idx,
                column_index=col_idx,
                is_header=is_header,
                confidence=confidence,
                bounding_box=bbox_data if bbox_data else None,
            ))
    return cells
