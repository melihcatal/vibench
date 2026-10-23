from dataclasses import dataclass
from typing import List, Optional, Dict, Any, Tuple

@dataclass
class ExtractedText:
    content: str

@dataclass
class ExtractedBlock:
    role: Optional[str]
    content: str
    bounding_box: List[Tuple[float, float]]

@dataclass
class ExtractedTable:
    row_count: int
    column_count: int
    cells: List[Dict[str, Any]]

@dataclass
class ExtractedKeyValuePair:
    key: str
    value: str
    confidence: float
