from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum


class DocumentType(Enum):
    """Supported document types."""

    GENERAL = "general"
    INVOICE = "invoice"
    RECEIPT = "receipt"
    ID_DOCUMENT = "idDocument"
    CONTRACT = "contract"
    FORM = "form"


@dataclass
class TextExtractionResult:
    """Result of text extraction from document."""

    text: str
    language: Optional[str] = None
    provider: str = ""
    model_id: str = ""
    confidence: float = 0.0
    page_count: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutElement:
    """A layout element (line, paragraph, table cell, etc.)."""

    type: str  # "line", "paragraph", "table_cell", "figure", "list_item"
    text: str
    bounding_box: Optional[List[float]] = None
    page_number: int = 1
    confidence: float = 1.0
    row_index: Optional[int] = None
    column_index: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutExtractionResult:
    """Result of layout extraction from document."""

    elements: List[LayoutElement]
    provider: str = ""
    model_id: str = ""
    page_count: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableCell:
    """A cell in a table."""

    content: str
    row_index: int
    column_index: int
    row_span: int = 1
    column_span: int = 1
    bounding_box: Optional[List[float]] = None
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Table:
    """A table extracted from document."""

    cells: List[TableCell]
    row_count: int
    column_count: int
    page_number: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TableExtractionResult:
    """Result of table extraction from document."""

    tables: List[Table]
    provider: str = ""
    model_id: str = ""
    total_tables: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyValuePair:
    """A key-value pair extracted from document."""

    key: str
    value: str
    confidence: float = 1.0
    bounding_box: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KeyValueExtractionResult:
    """Result of key-value extraction from document."""

    key_values: List[KeyValuePair]
    provider: str = ""
    model_id: str = ""
    document_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    """Result of text translation."""

    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    provider: str = ""
    model_id: str = ""
    confidence: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyCheckResult:
    """Result of safety/content moderation check."""

    text: str
    is_safe: bool
    categories: Dict[str, float]  # category -> score
    provider: str = ""
    model_id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FieldExtractionResult:
    """Result of structured field extraction."""

    fields: Dict[str, Any]
    provider: str = ""
    model_id: str = ""
    confidence: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    """Result of text embedding."""

    text: str
    embedding: List[float]
    provider: str = ""
    model_id: str = ""
    dimensions: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_bounding_box(box: Any) -> Optional[List[float]]:
    """Normalize bounding box from various formats."""
    if box is None:
        return None
    if isinstance(box, list):
        return box
    if hasattr(box, "__iter__"):
        return list(box)
    return None


def validate_image_path(image_path: str) -> bool:
    """Validate that image path exists and has supported extension."""
    import os

    supported_extensions = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".bmp", ".pdf"}
    if not os.path.exists(image_path):
        return False
    ext = os.path.splitext(image_path)[1].lower()
    return ext in supported_extensions
