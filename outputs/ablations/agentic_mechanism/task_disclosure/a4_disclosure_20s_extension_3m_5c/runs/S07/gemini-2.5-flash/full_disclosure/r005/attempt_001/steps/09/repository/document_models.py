from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class OcrRequest:
    """Represents a request for OCR processing."""
    image_bytes: bytes = field(repr=False)  # Raw image bytes
    language_hints: Optional[List[str]] = None  # e.g., ['en', 'es']
    mime_type: Optional[str] = None # e.g., 'image/jpeg', 'application/pdf'

@dataclass
class BoundingBox:
    """Represents a bounding box with coordinates (x1, y1, x2, y2)."""
    x1: int
    y1: int
    x2: int
    y2: int

@dataclass
class Word:
    """Represents a single word detected by OCR."""
    text: str
    bounding_box: BoundingBox
    confidence: float # Confidence score, typically between 0 and 1

@dataclass
class Line:
    """Represents a line of text detected by OCR."""
    text: str
    bounding_box: BoundingBox
    words: List[Word]
    confidence: float

@dataclass
class Block:
    """Represents a block of text detected by OCR."""
    block_type: str # e.g., 'text', 'paragraph', 'table'
    bounding_box: BoundingBox
    lines: List[Line]
    text: str # Aggregated text for the block
    confidence: float

@dataclass
class TableCell:
    """Represents a cell within a table."""
    text: str
    bounding_box: BoundingBox
    row_index: int
    column_index: int
    row_span: int = 1
    column_span: int = 1

@dataclass
class TableRow:
    """Represents a row within a table."""
    cells: List[TableCell]

@dataclass
class Table:
    """Represents a table detected in the document."""
    bounding_box: BoundingBox
    rows: List[TableRow]
    caption: Optional[str] = None

@dataclass
class KeyValuePair:
    """Represents a key-value pair extracted from a form-like document."""
    key: str
    key_bounding_box: BoundingBox
    value: str
    value_bounding_box: BoundingBox
    confidence: float

@dataclass
class LayoutElement:
    """Generic layout element."""
    element_type: str # e.g., 'text', 'image', 'table', 'form_field'
    bounding_box: BoundingBox
    text_content: Optional[str] = None # For text-based elements

@dataclass
class OcrResponse:
    """Represents the response from OCR and layout extraction."""
    full_text: str
    pages: List[Any] = field(default_factory=list) # Placeholder for page-specific data if needed
    blocks: List[Block] = field(default_factory=list)
    tables: List[Table] = field(default_factory=list)
    key_value_pairs: List[KeyValuePair] = field(default_factory=list)
    layout_elements: List[LayoutElement] = field(default_factory=list)

@dataclass
class NormalizedDocument:
    """Represents a normalized document with extracted information."""
    text_content: str
    extracted_fields: Dict[str, Any] = field(default_factory=dict)
    structured_data: Dict[str, Any] = field(default_factory=dict)
