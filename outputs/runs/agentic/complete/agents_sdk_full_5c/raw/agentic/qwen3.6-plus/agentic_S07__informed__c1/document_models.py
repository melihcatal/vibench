"""Define local request, response, and normalization helpers for OCR and Layout Extraction."""

from dataclasses import dataclass, field
from typing import Any


# --- OCR Text extraction models ---

@dataclass
class OcrTextRequest:
    """Request model for plain text OCR extraction."""
    image_bytes: bytes = field(default=b"")
    image_path: str = field(default="")
    region: str = field(default="us-east-1")


@dataclass
class OcrTextResponse:
    """Response model for plain text OCR extraction."""
    full_text: str = field(default="")
    lines: list[dict[str, Any]] = field(default_factory=list)
    words: list[dict[str, Any]] = field(default_factory=list)
    page_count: int = field(default=0)
    provider: str = field(default="")


# --- Layout extraction models ---

@dataclass
class LayoutRequest:
    """Request model for document layout analysis."""
    document_bytes: bytes = field(default=b"")
    content_type: str = field(default="application/pdf")


@dataclass
class LayoutElement:
    """Single layout element (line, word, table, paragraph, etc.)."""
    element_type: str = field(default="")
    text: str = field(default="")
    page_number: int | None = field(default=None)
    bounding_polygon: list[float] | None = field(default=None)
    confidence: float | None = field(default=None)
    row_count: int | None = field(default=None)
    column_count: int | None = field(default=None)
    role: str | None = field(default=None)


@dataclass
class LayoutResponse:
    """Response model for document layout analysis."""
    elements: list[LayoutElement] = field(default_factory=list)
    page_count: int = field(default=0)
    provider: str = field(default="")


# --- Table extraction models ---

@dataclass
class TableRequest:
    """Request model for table extraction."""
    document_bytes: bytes = field(default=b"")
    mime_type: str = field(default="application/pdf")


@dataclass
class TableCell:
    """Single cell within an extracted table."""
    text: str = field(default="")
    row_index: int = field(default=0)
    col_index: int = field(default=0)
    row_span: int = field(default=1)
    col_span: int = field(default=1)
    confidence: float | None = field(default=None)


@dataclass
class TableRow:
    """A single row of table cells."""
    cells: list[TableCell] = field(default_factory=list)
    row_index: int = field(default=0)


@dataclass
class TableExtractionResponse:
    """Response model for table extraction."""
    tables: list[dict[str, Any]] = field(default_factory=list)
    page_count: int = field(default=0)
    provider: str = field(default="")


# --- Key-Value extraction models ---

@dataclass
class KeyValueRequest:
    """Request model for key-value pair extraction."""
    document_bytes: bytes = field(default=b"")
    filename: str = field(default="document.pdf")


@dataclass
class KeyValuePair:
    """A single key-value pair from a form-like document."""
    key: str = field(default="")
    value: str = field(default="")
    confidence: float | None = field(default=None)
    page_number: int | None = field(default=None)


@dataclass
class KeyValueResponse:
    """Response model for key-value pair extraction."""
    key_value_pairs: list[KeyValuePair] = field(default_factory=list)
    page_count: int = field(default=0)
    provider: str = field(default="")


# --- Translation models (for ocr_translate.py) ---

@dataclass
class TranslateRequest:
    """Request model for translating extracted OCR text."""
    text: str = field(default="")
    source_language: str = field(default="")
    target_language: str = field(default="en")


@dataclass
class TranslateResponse:
    """Response model for text translation."""
    translated_text: str = field(default="")
    source_language: str = field(default="")
    target_language: str = field(default="")
    provider: str = field(default="")


# --- Safety models (for ocr_safety.py) ---

@dataclass
class SafetyCheckRequest:
    """Request model for content safety analysis."""
    text: str = field(default="")
    categories: list[str] = field(default_factory=list)


@dataclass
class SafetyFlag:
    """A single safety flag or category result."""
    category: str = field(default="")
    score: float = field(default=0.0)
    severity: str = field(default="")
    flagged: bool = field(default=False)


@dataclass
class SafetyCheckResponse:
    """Response model for content safety analysis."""
    flags: list[SafetyFlag] = field(default_factory=list)
    overall_safe: bool = field(default=True)
    provider: str = field(default="")


# --- Field extraction models (for document_field_extraction.py) ---

@dataclass
class FieldExtractionRequest:
    """Request model for structured field extraction."""
    document_bytes: bytes = field(default=b"")
    filename: str = field(default="document.pdf")
    document_type: str = field(default="invoice")


@dataclass
class ExtractedField:
    """A single extracted structured field."""
    name: str = field(default="")
    value: str = field(default="")
    confidence: float = field(default=0.0)
    page_number: int | None = field(default=None)


@dataclass
class FieldExtractionResponse:
    """Response model for structured field extraction."""
    fields: list[ExtractedField] = field(default_factory=list)
    document_type: str = field(default="")
    provider: str = field(default="")


# --- Embedding models (for ocr_embedding.py) ---

@dataclass
class EmbeddingRequest:
    """Request model for generating embeddings from text."""
    texts: list[str] = field(default_factory=list)
    model: str = field(default="")


@dataclass
class EmbeddingResponse:
    """Response model for text embedding."""
    embeddings: list[list[float]] = field(default_factory=list)
    model: str = field(default="")
    provider: str = field(default="")
