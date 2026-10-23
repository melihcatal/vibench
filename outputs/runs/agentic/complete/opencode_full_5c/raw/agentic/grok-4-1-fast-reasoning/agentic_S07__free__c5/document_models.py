from typing import List, Dict, TypedDict


class TextResponse(TypedDict):
    text: str


class Block(TypedDict):
    type: str
    text: str
    bbox: Dict[str, float]


class LayoutResponse(TypedDict):
    blocks: List[Block]


class Table(TypedDict):
    rows: List[List[str]]


class TablesResponse(TypedDict):
    tables: List[Table]


class KVPair(TypedDict):
    key: str
    value: str


class KVResponse(TypedDict):
    pairs: List[KVPair]


class TranslateResponse(TypedDict):
    translated_text: str


class SafetyResponse(TypedDict):
    flagged: bool
    categories: Dict[str, bool]


class FieldsResponse(TypedDict):
    fields: Dict[str, str]


class EmbeddingResponse(TypedDict):
    embedding: List[float]
