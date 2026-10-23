import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class TextBlock:
    """Represents a block of text with its content and bounding box."""
    id: str
    text_content: str
    bounding_box: List[float]  # [x1, y1, x2, y2] or [x1, y1, x2, y1, x2, y2, x1, y2]

@dataclasses.dataclass
class Line:
    """Represents a line of text."""
    id: str
    text_content: str
    bounding_box: List[float]

@dataclasses.dataclass
class TableCell:
    """Represents a cell within a table."""
    id: str
    text_content: str
    bounding_box: List[float]
    row_index: int
    column_index: int
    row_span: int = 1
    column_span: int = 1

@dataclasses.dataclass
class Table:
    """Represents a table structure."""
    id: str
    bounding_box: List[float]
    cells: List[TableCell]

@dataclasses.dataclass
class LayoutElement:
    """Base class for any layout element."""
    id: str
    bounding_box: List[float]
    type: str # e.g., "text", "line", "table"

@dataclasses.dataclass
class Page:
    """Represents a single page of a document."""
    page_number: int
    width: float
    height: float
    layout_elements: List[LayoutElement] = dataclasses.field(default_factory=list)
    text_blocks: List[TextBlock] = dataclasses.field(default_factory=list)
    lines: List[Line] = dataclasses.field(default_factory=list)
    tables: List[Table] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class Document:
    """Represents a document with multiple pages."""
    id: str
    pages: List[Page]

@dataclasses.dataclass
class OCRRequest:
    """Request model for OCR extraction."""
    image_data: bytes  # Raw image data
    language_hints: Optional[List[str]] = None

@dataclasses.dataclass
class OCRResponse:
    """Response model for OCR extraction."""
    document_id: str
    extracted_text: str
    pages: List[Page]

@dataclasses.dataclass
class LayoutExtractionRequest:
    """Request model for layout extraction."""
    document_id: str
    image_data: bytes
    extract_blocks: bool = True
    extract_lines: bool = False
    extract_tables: bool = False

@dataclasses.dataclass
class LayoutExtractionResponse:
    """Response model for layout extraction."""
    document_id: str
    pages: List[Page]

class NormalizationHelper:
    """Helper class for normalizing OCR and layout extraction results."""

    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalizes extracted text (e.g., removes extra spaces, cleans special characters)."""
        return " ".join(text.split()).strip()

    @staticmethod
    def merge_text_blocks(blocks: List[TextBlock]) -> str:
        """Merges text from multiple text blocks into a single string."""
        return " ".join([block.text_content for block in blocks])
