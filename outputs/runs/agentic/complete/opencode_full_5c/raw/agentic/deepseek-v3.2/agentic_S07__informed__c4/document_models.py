from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class BlockType(str, Enum):
    LINE = "line"
    WORD = "word"
    TABLE = "table"
    TABLE_CELL = "table_cell"
    FORM_FIELD = "form_field"
    CHECKBOX = "checkbox"
    SIGNATURE = "signature"


@dataclass
class TextExtractionRequest:
    image_path: str
    mime_type: Optional[str] = None
    language_hints: List[str] = field(default_factory=list)


@dataclass
class TextExtractionResponse:
    text: str
    raw_response: Any
    provider: str
    confidence: Optional[float] = None
    language: Optional[str] = None


@dataclass
class LayoutExtractionRequest:
    image_path: str
    mime_type: Optional[str] = None
    include_tables: bool = True
    include_lines: bool = True


@dataclass
class LayoutBlock:
    text: str
    bounding_box: List[Tuple[float, float]]
    confidence: float
    block_type: BlockType
    page_number: Optional[int] = None
    row_index: Optional[int] = None
    column_index: Optional[int] = None


@dataclass
class LayoutExtractionResponse:
    blocks: List[LayoutBlock]
    raw_response: Any
    provider: str
    page_count: Optional[int] = None


@dataclass
class TableExtractionRequest:
    image_path: str
    mime_type: Optional[str] = None
    max_tables: Optional[int] = None


@dataclass
class TableCell:
    text: str
    row_index: int
    column_index: int
    row_span: int = 1
    column_span: int = 1
    confidence: float = 0.0
    bounding_box: Optional[Dict[str, float]] = None


@dataclass
class Table:
    cells: List[TableCell]
    confidence: float
    bounding_box: Dict[str, float]
    row_count: Optional[int] = None
    column_count: Optional[int] = None


@dataclass
class TableExtractionResponse:
    tables: List[Table]
    raw_response: Any
    provider: str


@dataclass
class KeyValueExtractionRequest:
    image_path: str
    mime_type: Optional[str] = None
    expected_fields: Optional[List[str]] = None


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: float
    bounding_box: Optional[Dict[str, Any]] = None


@dataclass
class KeyValueExtractionResponse:
    key_values: List[KeyValuePair]
    raw_response: Any
    provider: str


def normalize_bounding_box(box: Any, provider: str) -> List[Tuple[float, float]]:
    """Normalize bounding box coordinates from different providers."""
    if provider == "google_documentai":
        if hasattr(box, "vertices"):
            return [(vertex.x, vertex.y) for vertex in box.vertices]
    elif provider == "azure_document_intelligence":
        if isinstance(box, list):
            return [(point.get("x", 0), point.get("y", 0)) for point in box]
    elif provider == "amazon_textract":
        if isinstance(box, dict):
            return [
                (box.get("Left", 0), box.get("Top", 0)),
                (box.get("Left", 0) + box.get("Width", 0), box.get("Top", 0)),
                (
                    box.get("Left", 0) + box.get("Width", 0),
                    box.get("Top", 0) + box.get("Height", 0),
                ),
                (box.get("Left", 0), box.get("Top", 0) + box.get("Height", 0)),
            ]
    return []


def parse_ocr_response(response: Any, provider: str) -> Dict[str, Any]:
    """Parse OCR response from different providers into a common format."""
    result = {"text": "", "blocks": [], "tables": [], "key_values": []}

    if provider == "google_documentai":
        if hasattr(response, "document"):
            result["text"] = response.document.text
    elif provider == "azure_document_intelligence":
        if hasattr(response, "to_dict"):
            data = response.to_dict()
            result["text"] = data.get("content", "")
    elif provider == "amazon_textract":
        result["text"] = " ".join(
            block.get("Text", "")
            for block in response.get("Blocks", [])
            if block.get("BlockType") == "LINE"
        )

    return result
