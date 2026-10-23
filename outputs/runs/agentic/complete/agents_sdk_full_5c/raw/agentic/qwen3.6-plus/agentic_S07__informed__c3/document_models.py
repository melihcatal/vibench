"""
Local request, response, and normalization helpers for OCR and Layout Extraction.

Defines dataclasses that represent common OCR/document extraction response
shapes and provides normalization utilities for Azure Document Intelligence output.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TextBlock:
    content: str
    confidence: float = 1.0


@dataclass
class LayoutBlock:
    kind: str  # "text", "table", "listItem", "selectionMark", "heading", "footnote", "pageHeader", "pageFooter"
    content: str
    page: int = 0
    bounding_box: Optional[List[float]] = None
    confidence: float = 1.0


@dataclass
class TableCell:
    row_index: int
    column_index: int
    content: str
    row_span: int = 1
    column_span: int = 1
    confidence: float = 1.0


@dataclass
class TableData:
    row_count: int
    column_count: int
    cells: List[TableCell] = field(default_factory=list)


@dataclass
class KeyValueItem:
    key: str
    value: str
    confidence: float = 1.0


@dataclass
class OcrTextResponse:
    full_text: str = ""
    pages: int = 0
    language: Optional[str] = None
    blocks: List[TextBlock] = field(default_factory=list)


@dataclass
class OcrLayoutResponse:
    pages: int = 0
    layout_blocks: List[LayoutBlock] = field(default_factory=list)


@dataclass
class OcrTableResponse:
    tables: List[TableData] = field(default_factory=list)


@dataclass
class OcrKeyValueResponse:
    key_value_pairs: List[KeyValueItem] = field(default_factory=list)


def normalize_azure_di_text_response(result: dict) -> OcrTextResponse:
    """Normalize Azure Document Intelligence analyze result to OcrTextResponse."""
    full_text = result.get("content", "")
    pages = len(result.get("pages", []))
    language = None
    pages_data = result.get("pages", [])
    if pages_data:
        lang_candidates = pages_data[0].get("languages", [])
        if lang_candidates:
            language = lang_candidates[0].get("locale")
    blocks = []
    paragraphs = result.get("paragraphs", [])
    for p in paragraphs:
        conf = p.get("confidence", 1.0)
        blocks.append(TextBlock(content=p.get("content", ""), confidence=conf))
    return OcrTextResponse(
        full_text=full_text,
        pages=pages,
        language=language,
        blocks=blocks,
    )


def normalize_azure_di_layout_response(result: dict) -> OcrLayoutResponse:
    """Normalize Azure Document Intelligence layout result to OcrLayoutResponse."""
    pages = len(result.get("pages", []))
    layout_blocks = []
    paragraphs = result.get("paragraphs", [])
    for p in paragraphs:
        bbox = p.get("bounding_regions", [{}])[0].get("polygon") if p.get("bounding_regions") else None
        page_num = p.get("bounding_regions", [{}])[0].get("page_number", 0) if p.get("bounding_regions") else 0
        kind = p.get("role", "text")
        layout_blocks.append(
            LayoutBlock(
                kind=kind,
                content=p.get("content", ""),
                page=page_num,
                bounding_box=bbox,
                confidence=p.get("confidence", 1.0),
            )
        )
    tables = result.get("tables", [])
    for t in tables:
        bbox = t.get("bounding_regions", [{}])[0].get("polygon") if t.get("bounding_regions") else None
        page_num = t.get("bounding_regions", [{}])[0].get("page_number", 0) if t.get("bounding_regions") else 0
        layout_blocks.append(
            LayoutBlock(
                kind="table",
                content=f"[Table {t.get('row_count', 0)}x{t.get('column_count', 0)}]",
                page=page_num,
                bounding_box=bbox,
                confidence=t.get("confidence", 1.0),
            )
        )
    return OcrLayoutResponse(pages=pages, layout_blocks=layout_blocks)


def normalize_azure_di_table_response(result: dict) -> OcrTableResponse:
    """Normalize Azure Document Intelligence analyze result to OcrTableResponse."""
    tables = []
    for t in result.get("tables", []):
        cells = []
        for c in t.get("cells", []):
            cells.append(
                TableCell(
                    row_index=c.get("row_index", 0),
                    column_index=c.get("column_index", 0),
                    content=c.get("content", ""),
                    row_span=c.get("row_span", 1),
                    column_span=c.get("column_span", 1),
                    confidence=c.get("confidence", 1.0),
                )
            )
        tables.append(
            TableData(
                row_count=t.get("row_count", 0),
                column_count=t.get("column_count", 0),
                cells=cells,
            )
        )
    return OcrTableResponse(tables=tables)


def normalize_azure_di_keyvalue_response(result: dict) -> OcrKeyValueResponse:
    """Normalize Azure Document Intelligence key-value pairs result."""
    kv_items = []
    for kv in result.get("documents", []):
        fields = kv.get("fields", {})
        for field_name, field_data in fields.items():
            kv_items.append(
                KeyValueItem(
                    key=field_name,
                    value=field_data.get("content", field_data.get("valueString", "")),
                    confidence=field_data.get("confidence", 1.0),
                )
            )
    return OcrKeyValueResponse(key_value_pairs=kv_items)
