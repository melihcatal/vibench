from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class TextExtractionRequest:
    image_path: str
    language_hints: Optional[List[str]] = None


@dataclass
class TextExtractionResponse:
    text: str
    confidence: float
    provider: str
    raw_response: Any


@dataclass
class LayoutExtractionRequest:
    image_path: str


@dataclass
class LayoutBlock:
    block_type: str
    text: str
    confidence: float
    bounding_box: Dict[str, float]
    relationships: List[Dict[str, Any]]
    page: int


@dataclass
class LayoutExtractionResponse:
    blocks: List[LayoutBlock]
    provider: str
    raw_response: Any


@dataclass
class TableExtractionRequest:
    image_path: str


@dataclass
class TableCell:
    row_index: int
    column_index: int
    content: str
    bounding_regions: List[Dict[str, Any]]


@dataclass
class Table:
    row_count: int
    column_count: int
    cells: List[TableCell]
    bounding_regions: List[Dict[str, Any]]


@dataclass
class TableExtractionResponse:
    tables: List[Table]
    provider: str
    raw_response: Any


@dataclass
class KeyValueExtractionRequest:
    image_path: str
    processor_id: Optional[str] = None


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: float
    normalized_value: Optional[str] = None


@dataclass
class KeyValueExtractionResponse:
    key_values: List[KeyValuePair]
    provider: str
    raw_response: Any


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    provider: str
    raw_response: Any


@dataclass
class SafetyCheckRequest:
    text: str
    attributes: List[str] = None


@dataclass
class SafetyAttributeScore:
    attribute: str
    score: float
    summary_score: Optional[float] = None


@dataclass
class SafetyCheckResponse:
    scores: List[SafetyAttributeScore]
    provider: str
    raw_response: Any


@dataclass
class FieldExtractionRequest:
    text: str
    field_schema: Dict[str, Any]


@dataclass
class ExtractedField:
    field_name: str
    value: Any
    confidence: float
    raw_text: Optional[str] = None


@dataclass
class FieldExtractionResponse:
    fields: List[ExtractedField]
    provider: str
    raw_response: Any


@dataclass
class EmbeddingRequest:
    text: str
    model: str = "text-embedding-ada-002"


@dataclass
class EmbeddingResponse:
    embedding: List[float]
    model: str
    provider: str
    raw_response: Any


def normalize_bounding_box(box: Dict[str, Any]) -> Dict[str, float]:
    """
    Normalize bounding box coordinates from different providers.
    """
    if "left" in box and "top" in box and "width" in box and "height" in box:
        return box

    if "Left" in box and "Top" in box and "Width" in box and "Height" in box:
        return {
            "left": box["Left"],
            "top": box["Top"],
            "width": box["Width"],
            "height": box["Height"],
        }

    if "x" in box and "y" in box and "w" in box and "h" in box:
        return {
            "left": box["x"],
            "top": box["y"],
            "width": box["w"],
            "height": box["h"],
        }

    return {"left": 0.0, "top": 0.0, "width": 0.0, "height": 0.0}


def parse_confidence(confidence_value: Any) -> float:
    """
    Parse confidence value from different provider formats.
    """
    if isinstance(confidence_value, (int, float)):
        return float(confidence_value)

    if isinstance(confidence_value, str):
        try:
            return float(confidence_value)
        except ValueError:
            return 0.0

    return 0.0
