from typing import Any, Dict, List, TypedDict

class BoundingBox(TypedDict):
    vertexes: List[Dict[str, float]]

class TextElement(TypedDict):
    content: str
    boundingBox: BoundingBox

class LayoutElement(TypedDict):
    type: str  # e.g., \"TEXT\", \"LINE\", \"TABLE\", \"FIELD\"
    text: TextElement
    confidence: float

class KeyValuePair(TypedDict):
    key: TextElement
    value: TextElement

class DocumentKeyValueResponse(TypedDict):
    pairs: List[KeyValuePair]

class DocumentResponse(TypedDict):
    text: str
    entities: List[TextElement]

class DocumentLayoutResponse(TypedDict):
    blocks: List[LayoutElement]

class DocumentTableResponse(TypedDict):
    tables: List[LayoutElement]
