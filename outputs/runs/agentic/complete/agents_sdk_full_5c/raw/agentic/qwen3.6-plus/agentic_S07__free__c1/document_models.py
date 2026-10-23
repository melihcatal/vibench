"""
Local request, response, and normalization helpers for OCR and Layout Extraction.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ImageSource:
    """Represents the source of a document image."""
    file_path: Optional[str] = None
    base64_data: Optional[str] = None
    content_type: str = "image/png"
    mime_type: str = "image/png"


@dataclass
class BoundingBox:
    """Normalized bounding box coordinates."""
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    polygon: Optional[List[Dict[str, float]]] = None


@dataclass
class OCRWord:
    """Individual word from OCR extraction."""
    text: str = ""
    confidence: float = 0.0
    bounding_box: Optional[BoundingBox] = None


@dataclass
class OCRLine:
    """Line of text from OCR extraction."""
    text: str = ""
    confidence: float = 0.0
    words: List[OCRWord] = field(default_factory=list)
    bounding_box: Optional[BoundingBox] = None


@dataclass
class OCRBlock:
    """Text block from document analysis."""
    text: str = ""
    block_type: str = "paragraph"
    confidence: float = 0.0
    lines: List[OCRLine] = field(default_factory=list)
    bounding_box: Optional[BoundingBox] = None


@dataclass
class ExtractTextRequest:
    """Request model for text extraction."""
    image: ImageSource = field(default_factory=ImageSource)
    language_hints: List[str] = field(default_factory=lambda: ["en"])
    page: int = 1


@dataclass
class ExtractTextResponse:
    """Response model for text extraction."""
    full_text: str = ""
    blocks: List[OCRBlock] = field(default_factory=list)
    lines: List[OCRLine] = field(default_factory=list)
    words: List[OCRWord] = field(default_factory=list)
    page_count: int = 1
    provider: str = ""
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class LayoutElement:
    """Represents a layout element from document analysis."""
    element_type: str = "text"
    text: str = ""
    confidence: float = 0.0
    bounding_box: Optional[BoundingBox] = None
    children: List["LayoutElement"] = field(default_factory=list)


@dataclass
class ExtractLayoutRequest:
    """Request model for layout extraction."""
    image: ImageSource = field(default_factory=ImageSource)
    features: List[str] = field(default_factory=lambda: ["blocks", "lines", "words"])


@dataclass
class ExtractLayoutResponse:
    """Response model for layout extraction."""
    elements: List[LayoutElement] = field(default_factory=list)
    page_width: int = 0
    page_height: int = 0
    confidence: float = 0.0
    provider: str = ""
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TableCell:
    """Represents a single cell in an extracted table."""
    text: str = ""
    row_index: int = 0
    col_index: int = 0
    row_span: int = 1
    col_span: int = 1
    confidence: float = 0.0
    bounding_box: Optional[BoundingBox] = None


@dataclass
class TableData:
    """Represents a single table extracted from a document."""
    table_id: str = ""
    rows: int = 0
    columns: int = 0
    cells: List[TableCell] = field(default_factory=list)
    confidence: float = 0.0
    bounding_box: Optional[BoundingBox] = None


@dataclass
class ExtractTablesRequest:
    """Request model for table extraction."""
    image: ImageSource = field(default_factory=ImageSource)
    include_confidence: bool = True


@dataclass
class ExtractTablesResponse:
    """Response model for table extraction."""
    tables: List[TableData] = field(default_factory=list)
    page_count: int = 1
    provider: str = ""
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class KeyValueEntry:
    """Represents an extracted key-value pair."""
    key: str = ""
    value: str = ""
    key_confidence: float = 0.0
    value_confidence: float = 0.0
    key_bounding_box: Optional[BoundingBox] = None
    value_bounding_box: Optional[BoundingBox] = None


@dataclass
class ExtractKeyValuesRequest:
    """Request model for key-value pair extraction."""
    image: ImageSource = field(default_factory=ImageSource)
    form_type: str = "generic"


@dataclass
class ExtractKeyValuesResponse:
    """Response model for key-value pair extraction."""
    key_values: List[KeyValueEntry] = field(default_factory=list)
    confidence: float = 0.0
    provider: str = ""
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TranslationRequest:
    """Request model for text translation."""
    text: str = ""
    source_language: str = "auto"
    target_language: str = "en"


@dataclass
class TranslationResponse:
    """Response model for text translation."""
    translated_text: str = ""
    detected_source_language: str = ""
    provider: str = ""
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class SafetyCheckRequest:
    """Request model for content safety check."""
    text: str = ""
    categories: Optional[List[str]] = None


@dataclass
class SafetyResult:
    """Result for a single safety category."""
    category: str = ""
    severity: int = 0
    flagged: bool = False


@dataclass
class SafetyCheckResponse:
    """Response model for content safety check."""
    overall_safe: bool = True
    results: List[SafetyResult] = field(default_factory=list)
    provider: str = ""
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class FieldDefinition:
    """Defines a field to extract from document text."""
    name: str = ""
    field_type: str = "string"
    description: str = ""
    required: bool = False


@dataclass
class FieldExtractionRequest:
    """Request model for structured field extraction."""
    document_text: str = ""
    fields: List[FieldDefinition] = field(default_factory=list)
    extraction_instructions: str = ""


@dataclass
class ExtractedField:
    """A single extracted field value."""
    name: str = ""
    value: Any = None
    confidence: float = 0.0
    source_text: str = ""


@dataclass
class FieldExtractionResponse:
    """Response model for field extraction."""
    fields: List[ExtractedField] = field(default_factory=list)
    provider: str = ""
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddingRequest:
    """Request model for text embedding."""
    text: str = ""
    model: str = "text-embedding-3-small"


@dataclass
class EmbeddingResponse:
    """Response model for text embedding."""
    embedding: List[float] = field(default_factory=list)
    model: str = ""
    token_count: int = 0
    provider: str = ""
    raw_response: Optional[Dict[str, Any]] = None


def normalize_bbox_from_vertices(vertices: List[Dict[str, float]]) -> BoundingBox:
    """Normalize polygon vertices to a bounding box."""
    if not vertices:
        return BoundingBox()
    x_coords = [v.get("x", v.get("X", 0)) for v in vertices]
    y_coords = [v.get("y", v.get("Y", 0)) for v in vertices]
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    return BoundingBox(
        x=min_x,
        y=min_y,
        width=max_x - min_x,
        height=max_y - min_y,
        polygon=vertices,
    )


def normalize_bbox_from_geometry(
    left: float = 0, top: float = 0, width: float = 0, height: float = 0
) -> BoundingBox:
    """Normalize geometry values to a bounding box."""
    return BoundingBox(x=left, y=top, width=width, height=height)
