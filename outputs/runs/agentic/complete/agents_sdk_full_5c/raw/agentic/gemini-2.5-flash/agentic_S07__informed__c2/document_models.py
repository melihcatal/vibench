from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class DocumentText:
    content: str
    page_number: Optional[int] = None
    bounding_box: Optional[List[float]] = None # [x1, y1, x2, y2, ...]

@dataclass
class DocumentTable:
    cells: List[Dict[str, Any]] # Each cell is a dict with content, row_index, col_index, etc.
    row_count: int
    column_count: int

@dataclass
class DocumentField:
    field_name: str
    field_value: Any
    confidence: Optional[float] = None

@dataclass
class OCRExtractionResult:
    full_text: str
    paragraphs: List[DocumentText]
    tables: List[DocumentTable]
    key_value_pairs: Dict[str, str] # Simplified for now
    fields: List[DocumentField] # For structured extraction later
