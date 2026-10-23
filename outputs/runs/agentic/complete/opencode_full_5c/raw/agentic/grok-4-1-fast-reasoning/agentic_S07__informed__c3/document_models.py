from typing import TypedDict, List, Dict, Any


class ExtractTextResponse(TypedDict):
    text: str


class ExtractLayoutResponse(TypedDict):
    elements: List[Dict[str, Any]]


class ExtractTablesResponse(TypedDict):
    tables: List[List[List[str]]]


class ExtractKeyValuesResponse(TypedDict):
    pairs: List[Dict[str, str]]


class TranslateResponse(TypedDict):
    translated: str


class SafetyResponse(TypedDict):
    is_safe: bool
    toxicity_score: float


class FieldExtractionResponse(TypedDict):
    fields: Dict[str, Any]


class EmbeddingResponse(TypedDict):
    embeddings: List[List[float]]
