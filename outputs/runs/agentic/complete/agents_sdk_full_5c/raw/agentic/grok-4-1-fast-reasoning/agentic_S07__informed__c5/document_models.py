from typing import Dict, List, Any, TypedDict, Optional

class LayoutElement(TypedDict):
    type: str
    text: str
    confidence: Optional[float]
    bbox: Optional[List[float]]

class TableCell(TypedDict):
    row: int
    column: int
    text: str
    confidence: Optional[float]

class Table(TypedDict):
    cells: List[TableCell]

class KeyValuePair(TypedDict):
    key: str
    value: str
    confidence: Optional[float]

ExtractedText = str
