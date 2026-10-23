from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class LayoutElement:
    page_number: int
    type: str          # e.g. 'LINE', 'WORD', 'TOKEN', 'TABLE', 'KEY_VALUE_SET'
    text: str
    confidence: float
    bounding_box: Dict[str, float]   # coordinates (normalized or absolute)

@dataclass
class LayoutResult:
    document_id: str
    pages: List[LayoutElement]
    entities: List[Dict[str, Any]]   # normalized key-value or table entries

@dataclass
class OCRRequest:
    file_path: str
    mime_type: str = 'application/pdf'

@dataclass
class OCRResult:
    raw_text: str
    layout_result: LayoutResult