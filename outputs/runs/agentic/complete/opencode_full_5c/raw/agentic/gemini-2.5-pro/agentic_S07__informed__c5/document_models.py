from dataclasses import dataclass
from typing import List, Tuple, Any


@dataclass
class Block:
    content: str
    bounding_box: List[Tuple[float, float]]


@dataclass
class Table:
    cells: List[List[str]]
    row_count: int
    column_count: int
    bounding_box: List[Tuple[float, float]]


@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: float


@dataclass
class Document:
    content: str
    blocks: List[Block]
    tables: List[Table]
    key_value_pairs: List[KeyValuePair]


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_lang: str


@dataclass
class SafetyAnalysis:
    is_safe: bool
    categories: dict[str, Any]


@dataclass
class StructuredField:
    name: str
    value: Any
    confidence: float


@dataclass
class EmbeddingVector:
    text: str
    vector: List[float]
