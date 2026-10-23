from typing import TypedDict, List, Dict

# TypedDict definitions for normalized OCR/Layout responses

class BlockResult(TypedDict):
    id: str
    text: str
    block_type: str
    geometry: Dict[str, float]

class LineResult(TypedDict):
    block_id: str
    text: str

class KeyValueResult(TypedDict):
    role: str
    key: str
    value: str

class TableCellResult(TypedDict):
    row_idx: int
    col_idx: int
    text: str

class TableResult(TypedDict):
    rows: List[List[TableCellResult]]

class LayoutResult(TypedDict):
    lines: List[LineResult]
    key_values: List[KeyValueResult]
    tables: List[TableResult]
    blocks: List[BlockResult]

class TableCellsResult(TypedDict):
    cells: List[TableCellResult]
