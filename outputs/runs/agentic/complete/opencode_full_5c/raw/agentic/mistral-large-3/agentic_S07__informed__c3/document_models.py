from typing import List, Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class OCRResponse:
    """Normalized response for OCR text extraction."""

    text: str
    pages: int
    language: str


@dataclass
class LayoutElement:
    """Normalized layout element (block, line, table, etc.)."""

    type: str
    text: str
    bounding_box: Optional[List[float]]
    confidence: Optional[float] = None
    rows: Optional[int] = None
    columns: Optional[int] = None


@dataclass
class LayoutResponse:
    """Normalized response for layout extraction."""

    elements: List[LayoutElement]
    pages: int


@dataclass
class TableCell:
    """Normalized table cell structure."""

    row_index: int
    column_index: int
    text: str
    is_header: bool


@dataclass
class TableResponse:
    """Normalized response for table extraction."""

    tables: List[Dict[str, Any]]
    pages: int


@dataclass
class KeyValuePair:
    """Normalized key-value pair."""

    key: str
    value: str
    confidence: Optional[float] = None


@dataclass
class KeyValueResponse:
    """Normalized response for key-value extraction."""

    key_value_pairs: List[KeyValuePair]
    pages: int
