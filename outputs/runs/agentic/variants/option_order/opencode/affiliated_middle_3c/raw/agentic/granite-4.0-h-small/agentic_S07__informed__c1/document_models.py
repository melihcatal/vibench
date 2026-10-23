from typing import TypedDict, List


class Block(TypedDict):
    Id: str
    Text: str
    BlockType: str
    Confidence: float


class KeyValue(TypedDict):
    Key: Block
    Value: Block


class Table(TypedDict):
    Rows: List[str]


class LayoutElement(TypedDict):
    type: str
    text: str = ""
    rows: List[str] = []
    id: str = ""
    key: Block = None
    value: Block = None


class ExtractTextRequest(TypedDict):
    image_path: str


class ExtractTextResponse(TypedDict):
    text: str


class ExtractLayoutRequest(TypedDict):
    image_path: str


class ExtractLayoutResponse(TypedDict):
    layout: List[LayoutElement]


class ExtractTablesRequest(TypedDict):
    image_path: str


class ExtractTablesResponse(TypedDict):
    tables: List[Table]


class ExtractKeyValuesRequest(TypedDict):
    image_path: str


class ExtractKeyValuesResponse(TypedDict):
    key_values: List[KeyValue]
