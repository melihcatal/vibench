"""
Local request, response, and normalization helpers for OCR and Layout Extraction.
Defines data models and normalization utilities for document processing results.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
from enum import Enum


class BlockType(Enum):
    """Document block types from Google Vision API or Document AI."""
    TEXT = "TEXT"
    TITLE = "TITLE"
    LIST_ITEM = "LIST_ITEM"
    TABLE = "TABLE"
    FORM = "FORM"
    IMAGE = "IMAGE"
    BARCODE = "BARCODE"


@dataclass
class BoundingBox:
    """Normalized bounding box representation."""
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    def to_dict(self) -> Dict[str, float]:
        return {
            "x_min": self.x_min,
            "y_min": self.y_min,
            "x_max": self.x_max,
            "y_max": self.y_max,
        }


@dataclass
class TextBlock:
    """A block of text extracted from a document."""
    text: str
    confidence: float
    bounding_box: Optional[BoundingBox] = None
    block_type: BlockType = BlockType.TEXT
    language: str = "en"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "confidence": self.confidence,
            "bounding_box": self.bounding_box.to_dict() if self.bounding_box else None,
            "block_type": self.block_type.value,
            "language": self.language,
        }


@dataclass
class TableCell:
    """A single cell in an extracted table."""
    row_index: int
    col_index: int
    text: str
    confidence: float
    bounding_box: Optional[BoundingBox] = None
    is_header: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "row_index": self.row_index,
            "col_index": self.col_index,
            "text": self.text,
            "confidence": self.confidence,
            "bounding_box": self.bounding_box.to_dict() if self.bounding_box else None,
            "is_header": self.is_header,
        }


@dataclass
class TableRow:
    """A row in an extracted table."""
    cells: List[TableCell]
    row_index: int

    def to_list(self) -> List[str]:
        return [cell.text for cell in self.cells]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "row_index": self.row_index,
            "cells": [cell.to_dict() for cell in self.cells],
        }


@dataclass
class ExtractedTable:
    """A complete extracted table from a document."""
    rows: List[TableRow]
    bounding_box: Optional[BoundingBox] = None
    table_id: str = ""

    def to_list_of_dicts(self) -> List[Dict[str, str]]:
        """Convert table to list of dictionaries (one per row)."""
        if not self.rows:
            return []
        headers = [cell.text for cell in self.rows[0].cells]
        result = []
        for row in self.rows[1:]:
            row_dict = {}
            for i, cell in enumerate(row.cells):
                key = headers[i] if i < len(headers) else f"col_{i}"
                row_dict[key] = cell.text
            result.append(row_dict)
        return result

    def to_dict(self) -> Dict[str, Any]:
        return {
            "table_id": self.table_id,
            "rows": [row.to_dict() for row in self.rows],
            "bounding_box": self.bounding_box.to_dict() if self.bounding_box else None,
        }


@dataclass
class KeyValue:
    """A key-value pair extracted from a form document."""
    key: str
    value: str
    confidence: float
    key_bounding_box: Optional[BoundingBox] = None
    value_bounding_box: Optional[BoundingBox] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key": self.key,
            "value": self.value,
            "confidence": self.confidence,
            "key_bounding_box": self.key_bounding_box.to_dict() if self.key_bounding_box else None,
            "value_bounding_box": self.value_bounding_box.to_dict() if self.value_bounding_box else None,
        }


@dataclass
class OcrResponse:
    """Normalized OCR response from Google Vision API."""
    full_text: str
    blocks: List[TextBlock]
    language: str = "en"
    page_count: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "full_text": self.full_text,
            "blocks": [block.to_dict() for block in self.blocks],
            "language": self.language,
            "page_count": self.page_count,
        }


@dataclass
class LayoutResponse:
    """Normalized layout extraction response."""
    blocks: List[TextBlock]
    page_width: float = 0.0
    page_height: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "blocks": [block.to_dict() for block in self.blocks],
            "page_width": self.page_width,
            "page_height": self.page_height,
        }


@dataclass
class TableResponse:
    """Normalized table extraction response."""
    tables: List[ExtractedTable]
    page_count: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tables": [table.to_dict() for table in self.tables],
            "page_count": self.page_count,
        }


@dataclass
class KeyValueResponse:
    """Normalized key-value extraction response."""
    key_values: List[KeyValue]
    form_type: str = ""
    page_count: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_values": [kv.to_dict() for kv in self.key_values],
            "form_type": self.form_type,
            "page_count": self.page_count,
        }


def normalize_vision_vertices(
    vertices: Any, image_width: float = 1.0, image_height: float = 1.0
) -> BoundingBox:
    """
    Normalize Google Vision API vertices to a BoundingBox.
    Vertices are normalized to [0, 1] relative coordinates.
    """
    if hasattr(vertices, 'vertices'):
        verts = list(vertices.vertices)
    elif isinstance(vertices, (list, tuple)):
        verts = list(vertices)
    else:
        return BoundingBox(0.0, 0.0, 1.0, 1.0)

    x_coords = []
    y_coords = []
    for v in verts:
        if hasattr(v, 'x') and hasattr(v, 'y'):
            x_coords.append(v.x / image_width if image_width > 0 else 0)
            y_coords.append(v.y / image_height if image_height > 0 else 0)
        elif isinstance(v, (list, tuple)) and len(v) >= 2:
            x_coords.append(v[0] / image_width if image_width > 0 else 0)
            y_coords.append(v[1] / image_height if image_height > 0 else 0)

    if not x_coords or not y_coords:
        return BoundingBox(0.0, 0.0, 1.0, 1.0)

    return BoundingBox(
        x_min=min(x_coords),
        y_min=min(y_coords),
        x_max=max(x_coords),
        y_max=max(y_coords),
    )


def build_vision_image_context(
    language_hints: Optional[List[str]] = None,
    crop_hints_params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Build an image_context dict for Google Vision API requests."""
    context = {}
    if language_hints:
        context["language_hints"] = language_hints
    if crop_hints_params:
        context["crop_hints_params"] = crop_hints_params
    return context
