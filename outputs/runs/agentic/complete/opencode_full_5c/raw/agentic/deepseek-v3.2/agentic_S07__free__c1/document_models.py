from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum


class DocumentType(Enum):
    """Types of documents that can be processed."""

    INVOICE = "invoice"
    RECEIPT = "receipt"
    FORM = "form"
    CONTRACT = "contract"
    REPORT = "report"
    LETTER = "letter"
    OTHER = "other"


@dataclass
class TextExtractionRequest:
    """Request for text extraction from an image."""

    image_path: Optional[str] = None
    image_base64: Optional[str] = None
    language_hints: List[str] = field(default_factory=lambda: ["en"])
    include_confidence: bool = True


@dataclass
class OCRResponse:
    """Response from OCR text extraction."""

    text: str
    confidence: float
    provider: str
    model: str
    raw_response: Any = None
    language: Optional[str] = None


@dataclass
class LayoutExtractionRequest:
    """Request for layout extraction from a document."""

    image_path: Optional[str] = None
    image_base64: Optional[str] = None
    include_text: bool = True
    include_bounding_boxes: bool = True


@dataclass
class LayoutElement:
    """A single layout element (block, line, etc.)."""

    type: str  # "block", "paragraph", "line", "word"
    text: str
    bounding_box: List[tuple]  # List of (x, y) coordinates
    confidence: float = 0.0


@dataclass
class LayoutResponse:
    """Response from layout extraction."""

    elements: List[LayoutElement]
    provider: str
    model: str
    raw_response: Any = None


@dataclass
class TableExtractionRequest:
    """Request for table extraction from a document."""

    image_path: Optional[str] = None
    image_base64: Optional[str] = None
    mime_type: Optional[str] = None
    include_empty_cells: bool = False


@dataclass
class TableCell:
    """A single table cell."""

    text: str
    row_span: int = 1
    col_span: int = 1


@dataclass
class Table:
    """A table with rows and columns."""

    rows: List[List[TableCell]]
    row_count: int
    column_count: int


@dataclass
class TableResponse:
    """Response from table extraction."""

    tables: List[Table]
    provider: str
    model: str
    raw_response: Any = None


@dataclass
class KeyValueExtractionRequest:
    """Request for key-value pair extraction from a form."""

    image_path: Optional[str] = None
    image_base64: Optional[str] = None
    mime_type: Optional[str] = None
    document_type: Optional[DocumentType] = None


@dataclass
class KeyValuePair:
    """A key-value pair extracted from a document."""

    key: str
    value: str
    confidence: float = 0.0


@dataclass
class KeyValueResponse:
    """Response from key-value extraction."""

    pairs: List[KeyValuePair]
    provider: str
    model: str
    raw_response: Any = None


@dataclass
class NormalizedDocument:
    """Normalized document data after processing."""

    text: str
    layout_elements: List[LayoutElement] = field(default_factory=list)
    tables: List[Table] = field(default_factory=list)
    key_value_pairs: List[KeyValuePair] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_ocr_response(response: OCRResponse) -> Dict[str, Any]:
    """Normalize OCR response to a standard format."""
    return {
        "text": response.text,
        "confidence": response.confidence,
        "provider": response.provider,
        "model": response.model,
        "language": response.language,
    }


def normalize_layout_response(response: LayoutResponse) -> Dict[str, Any]:
    """Normalize layout response to a standard format."""
    elements = []
    for elem in response.elements:
        elements.append(
            {
                "type": elem.type,
                "text": elem.text,
                "bounding_box": elem.bounding_box,
                "confidence": elem.confidence,
            }
        )

    return {
        "elements": elements,
        "provider": response.provider,
        "model": response.model,
        "element_count": len(elements),
    }


def normalize_table_response(response: TableResponse) -> Dict[str, Any]:
    """Normalize table response to a standard format."""
    tables = []
    for table in response.tables:
        table_data = []
        for row in table.rows:
            row_data = []
            for cell in row:
                row_data.append(
                    {
                        "text": cell.text,
                        "row_span": cell.row_span,
                        "col_span": cell.col_span,
                    }
                )
            table_data.append(row_data)

        tables.append(
            {
                "rows": table_data,
                "row_count": table.row_count,
                "column_count": table.column_count,
            }
        )

    return {
        "tables": tables,
        "provider": response.provider,
        "model": response.model,
        "table_count": len(tables),
    }


def normalize_keyvalue_response(response: KeyValueResponse) -> Dict[str, Any]:
    """Normalize key-value response to a standard format."""
    pairs = []
    for pair in response.pairs:
        pairs.append(
            {"key": pair.key, "value": pair.value, "confidence": pair.confidence}
        )

    return {
        "pairs": pairs,
        "provider": response.provider,
        "model": response.model,
        "pair_count": len(pairs),
    }
