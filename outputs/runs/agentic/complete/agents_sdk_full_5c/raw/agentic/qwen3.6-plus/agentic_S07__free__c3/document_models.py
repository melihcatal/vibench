"""
Define local request, response, and normalization helpers for OCR and Layout Extraction.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class OCRRequest:
    """Request model for OCR operations."""
    image_path: str
    features: list = field(default_factory=lambda: ["TEXT", "FORMS", "TABLES"])
    language: str = "en"
    output_s3: Optional[str] = None


@dataclass
class OCRTextBlock:
    """Normalized OCR text block response."""
    text: str
    confidence: float = 0.0
    block_type: str = "LINE"
    page: int = 0
    geometry: Optional[dict] = None


@dataclass
class LayoutElement:
    """Normalized layout element response."""
    element_type: str  # WORD, LINE, CELL, TABLE, KEY, VALUE, etc.
    text: str
    confidence: float = 0.0
    bounding_box: Optional[dict] = None
    page: int = 0
    relationships: Optional[list] = None


@dataclass
class TableCell:
    """Normalized table cell response."""
    text: str
    row_index: int = 0
    column_index: int = 0
    is_header: bool = False
    confidence: float = 0.0
    row_span: int = 1
    column_span: int = 1


@dataclass
class TableStructure:
    """Normalized table structure response."""
    cells: list = field(default_factory=list)
    row_count: int = 0
    column_count: int = 0
    page: int = 0
    confidence: float = 0.0


@dataclass
class KeyValueItem:
    """Normalized key-value pair response."""
    key: str
    value: str
    key_confidence: float = 0.0
    value_confidence: float = 0.0
    page: int = 0


@dataclass
class OCRResponse:
    """Normalized OCR response."""
    text_blocks: list = field(default_factory=list)
    full_text: str = ""
    page_count: int = 1
    model_version: str = ""
    status_code: int = 0


@dataclass
class LayoutResponse:
    """Normalized layout response."""
    elements: list = field(default_factory=list)
    page_count: int = 1
    model_version: str = ""
    status_code: int = 0


@dataclass
class TableResponse:
    """Normalized table response."""
    tables: list = field(default_factory=list)
    page_count: int = 1
    model_version: str = ""
    status_code: int = 0


@dataclass
class KeyValueResponse:
    """Normalized key-value pair response."""
    pairs: list = field(default_factory=list)
    page_count: int = 1
    model_version: str = ""
    status_code: int = 0


@dataclass
class TranslationRequest:
    """Request model for translation."""
    text: str
    source_language: str = "en"
    target_language: str = "es"


@dataclass
class TranslationResponse:
    """Normalized translation response."""
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    confidence: float = 0.0


@dataclass
class SafetyRequest:
    """Request model for safety analysis."""
    text: str
    categories: list = field(default_factory=lambda: [
        "HATE", "SEXUALLY_EXPLICIT", "DANGEROUS", "MEDICAL", "VIOLENCE"
    ])


@dataclass
class SafetyResponse:
    """Normalized safety response."""
    is_safe: bool = True
    categories: dict = field(default_factory=dict)
    overall_confidence: float = 0.0


@dataclass
class FieldExtractionRequest:
    """Request model for field extraction."""
    text: str
    schema: Optional[dict] = None
    document_type: str = "general"


@dataclass
class ExtractedField:
    """Normalized extracted field."""
    field_name: str
    value: str
    confidence: float = 0.0
    field_type: str = "string"


@dataclass
class FieldExtractionResponse:
    """Normalized field extraction response."""
    fields: list = field(default_factory=list)
    document_type: str = "general"
    confidence: float = 0.0


@dataclass
class EmbeddingRequest:
    """Request model for embedding generation."""
    text: str
    model: str = "text-embedding-ada-002"


@dataclass
class EmbeddingResponse:
    """Normalized embedding response."""
    embedding: list = field(default_factory=list)
    model: str = ""
    usage: Optional[dict] = None
