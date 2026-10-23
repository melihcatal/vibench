from typing import TypedDict, List, Dict, Any


class TextResult(TypedDict):
    text: str


class LayoutResult(TypedDict):
    blocks: List[Dict[str, Any]]


class TablesResult(TypedDict):
    tables: List[List[List[str]]]


class KeyValuesResult(TypedDict):
    pairs: List[Dict[str, Any]]


class TranslateResult(TypedDict):
    translated_text: str


class SafetyResult(TypedDict):
    flagged: bool
    categories_scores: Dict[str, float]


class FieldsResult(TypedDict):
    fields: Dict[str, Any]


class EmbeddingResult(TypedDict):
    embedding: List[float]
