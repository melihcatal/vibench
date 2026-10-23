from typing import TypedDict, List

# Types used across helper modules
class TextResult(TypedDict):
    text: str
    blocks: List[dict]

class LayoutResult(TypedDict):
    blocks: List[dict]

class TableResult(TypedDict):
    cells: List[dict]
    rows: List[dict]

class KeyValueResult(TypedDict):
    pairs: List[dict]
