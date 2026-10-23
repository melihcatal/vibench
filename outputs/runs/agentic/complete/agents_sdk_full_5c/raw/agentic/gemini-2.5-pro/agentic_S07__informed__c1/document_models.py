from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class ExtractedText:
    content: str
    source_file: str

@dataclass
class LayoutBlock:
    kind: str
    content: str
    bounding_box: List[Dict[str, float]]

@dataclass
class TableCell:
    row_index: int
    column_index: int
    content: str
    kind: str

@dataclass
class ExtractedTable:
    row_count: int
    column_count: int
    cells: List[TableCell]

@dataclass
class KeyValuePair:
    key: str
    value: str
    confidence: float

@dataclass
class DocumentAnalysisResult:
    text: ExtractedText
    layouts: List[LayoutBlock]
    tables: List[ExtractedTable]
    key_value_pairs: List[KeyValuePair]

