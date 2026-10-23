"""
Local request, response, and normalization helpers for OCR and Layout Extraction.
Defines data models and utility functions for processing Azure Document Intelligence results.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class OCRTextBlock:
    """Represents a single text block from OCR extraction."""
    content: str
    confidence: float
    bounding_box: Optional[List[float]] = None
    page_number: Optional[int] = None


@dataclass
class LayoutElement:
    """Represents a layout element such as paragraph, section heading, table, etc."""
    element_type: str  # e.g., 'paragraph', 'sectionHeading', 'table', 'figure'
    content: str
    bounding_box: Optional[List[float]] = None
    confidence: float = 0.0
    page_number: Optional[int] = None


@dataclass
class TableCell:
    """Represents a single table cell with row/column position."""
    content: str
    row_index: int
    column_index: int
    row_span: int = 1
    column_span: int = 1
    confidence: float = 0.0
    bounding_box: Optional[List[float]] = None


@dataclass
class TableData:
    """Represents a full table with cells and dimensions."""
    row_count: int
    column_count: int
    cells: List[TableCell] = field(default_factory=list)
    bounding_box: Optional[List[float]] = None
    page_number: Optional[int] = None


@dataclass
class KeyValueEntry:
    """Represents an extracted key-value pair from a form."""
    key: str
    value: str
    confidence: float = 0.0
    key_bounding_box: Optional[List[float]] = None
    value_bounding_box: Optional[List[float]] = None
    page_number: Optional[int] = None


@dataclass
class DocumentTextResult:
    """Aggregated result for plain text extraction."""
    full_text: str
    blocks: List[OCRTextBlock] = field(default_factory=list)
    page_count: int = 0


@dataclass
class DocumentLayoutResult:
    """Aggregated result for layout extraction."""
    elements: List[LayoutElement] = field(default_factory=list)
    tables: List[TableData] = field(default_factory=list)
    page_count: int = 0


@dataclass
class DocumentKeyValueResult:
    """Aggregated result for key-value pair extraction."""
    pairs: List[KeyValueEntry] = field(default_factory=list)
    page_count: int = 0


def normalize_bounding_box(bbox: Any) -> Optional[List[float]]:
    """
    Normalize Azure Document Intelligence bounding polygon to a list of floats.

    Args:
        bbox: A polygon object with 'points' attribute or similar.

    Returns:
        List of floats representing [x1, y1, x2, y2, ...] or None.
    """
    if bbox is None:
        return None
    if hasattr(bbox, "points"):
        return [float(coord) for pt in bbox.points for coord in [pt.x, pt.y]]
    if isinstance(bbox, list):
        return [float(c) for c in bbox]
    return None


def normalize_ocr_text_result(result: Any) -> DocumentTextResult:
    """
    Normalize Azure Document Intelligence analyze result into DocumentTextResult.

    Args:
        result: The Azure Document Intelligence result object.

    Returns:
        DocumentTextResult: Normalized text extraction result.
    """
    full_text_parts = []
    blocks = []

    for page in getattr(result, "pages", []):
        for line in getattr(page, "lines", []):
            text = getattr(line, "content", "")
            confidence = getattr(line, "confidence", 0.0)
            bbox = normalize_bounding_box(getattr(line, "bounding_polygon", None))
            full_text_parts.append(text)
            blocks.append(OCRTextBlock(
                content=text,
                confidence=confidence,
                bounding_box=bbox,
                page_number=getattr(page, "page_number", None),
            ))

    full_text = "\n".join(full_text_parts)
    return DocumentTextResult(
        full_text=full_text,
        blocks=blocks,
        page_count=len(getattr(result, "pages", [])),
    )


def normalize_layout_result(result: Any) -> DocumentLayoutResult:
    """
    Normalize Azure Document Intelligence analyze result into DocumentLayoutResult.

    Args:
        result: The Azure Document Intelligence result object.

    Returns:
        DocumentLayoutResult: Normalized layout extraction result.
    """
    elements = []

    for paragraph in getattr(result, "paragraphs", []):
        role = getattr(paragraph, "role", "paragraph")
        content = getattr(paragraph, "content", "")
        confidence = getattr(paragraph, "confidence", 0.0)
        bbox = normalize_bounding_box(getattr(paragraph, "bounding_polygon", None))

        if role == "pageHeader":
            element_type = "pageHeader"
        elif role == "pageFooter":
            element_type = "pageFooter"
        elif role == "title":
            element_type = "title"
        elif role == "sectionHeading":
            element_type = "sectionHeading"
        else:
            element_type = "paragraph"

        elements.append(LayoutElement(
            element_type=element_type,
            content=content,
            bounding_box=bbox,
            confidence=confidence,
        ))

    tables = []
    for table in getattr(result, "tables", []):
        row_count = getattr(table, "row_count", 0)
        column_count = getattr(table, "column_count", 0)
        bbox = normalize_bounding_box(getattr(table, "bounding_polygon", None))
        page_num = None
        regions = getattr(table, "regions", [])
        if regions:
            page_num = getattr(regions[0], "page_number", None)

        cells = []
        for cell in getattr(table, "cells", []):
            cells.append(TableCell(
                content=getattr(cell, "content", ""),
                row_index=getattr(cell, "row_index", 0),
                column_index=getattr(cell, "column_index", 0),
                row_span=getattr(cell, "row_span", 1),
                column_span=getattr(cell, "column_span", 1),
                confidence=getattr(cell, "confidence", 0.0),
                bounding_box=normalize_bounding_box(getattr(cell, "bounding_polygon", None)),
            ))

        tables.append(TableData(
            row_count=row_count,
            column_count=column_count,
            cells=cells,
            bounding_box=bbox,
            page_number=page_num,
        ))

    return DocumentLayoutResult(
        elements=elements,
        tables=tables,
        page_count=len(getattr(result, "pages", [])),
    )


def normalize_table_result(result: Any) -> List[TableData]:
    """
    Normalize Azure Document Intelligence analyze result into a list of TableData.

    Args:
        result: The Azure Document Intelligence result object.

    Returns:
        List[TableData]: Normalized table extraction results.
    """
    tables = []
    for table in getattr(result, "tables", []):
        row_count = getattr(table, "row_count", 0)
        column_count = getattr(table, "column_count", 0)
        bbox = normalize_bounding_box(getattr(table, "bounding_polygon", None))
        page_num = None
        regions = getattr(table, "regions", [])
        if regions:
            page_num = getattr(regions[0], "page_number", None)

        cells = []
        for cell in getattr(table, "cells", []):
            cells.append(TableCell(
                content=getattr(cell, "content", ""),
                row_index=getattr(cell, "row_index", 0),
                column_index=getattr(cell, "column_index", 0),
                row_span=getattr(cell, "row_span", 1),
                column_span=getattr(cell, "column_span", 1),
                confidence=getattr(cell, "confidence", 0.0),
                bounding_box=normalize_bounding_box(getattr(cell, "bounding_polygon", None)),
            ))

        tables.append(TableData(
            row_count=row_count,
            column_count=column_count,
            cells=cells,
            bounding_box=bbox,
            page_number=page_num,
        ))

    return tables


def normalize_key_value_result(result: Any) -> DocumentKeyValueResult:
    """
    Normalize Azure Document Intelligence analyze result into DocumentKeyValueResult.

    Args:
        result: The Azure Document Intelligence result object.

    Returns:
        DocumentKeyValueResult: Normalized key-value extraction result.
    """
    pairs = []

    key_value_pairs = getattr(result, "key_value_pairs", [])
    for kv in key_value_pairs:
        key_obj = getattr(kv, "key", None)
        value_obj = getattr(kv, "value", None)

        key_text = ""
        value_text = ""
        key_bbox = None
        value_bbox = None
        confidence = getattr(kv, "confidence", 0.0)

        if key_obj:
            if hasattr(key_obj, "content"):
                key_text = key_obj.content
            key_bbox = normalize_bounding_box(
                getattr(key_obj, "bounding_polygon", None) or
                getattr(key_obj, "bounding_regions", [None])[0] if getattr(key_obj, "bounding_regions", None) else None
            )

        if value_obj:
            if hasattr(value_obj, "content"):
                value_text = value_obj.content
            value_bbox = normalize_bounding_box(
                getattr(value_obj, "bounding_polygon", None) or
                getattr(value_obj, "bounding_regions", [None])[0] if getattr(value_obj, "bounding_regions", None) else None
            )

        page_num = None
        if key_obj and hasattr(key_obj, "bounding_regions"):
            regions = getattr(key_obj, "bounding_regions", [])
            if regions:
                page_num = getattr(regions[0], "page_number", None)

        pairs.append(KeyValueEntry(
            key=key_text,
            value=value_text,
            confidence=confidence,
            key_bounding_box=key_bbox,
            value_bounding_box=value_bbox,
            page_number=page_num,
        ))

    return DocumentKeyValueResult(
        pairs=pairs,
        page_count=len(getattr(result, "pages", [])),
    )
