from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class OCRRequest:
    document_content: str  # Base64 encoded image or document path
    document_type: Optional[str] = None # e.g., "image/jpeg", "application/pdf"

@dataclass
class LayoutBlock:
    id: str
    text_content: str
    bounding_box: List[float] # [x1, y1, x2, y2] normalized coordinates
    block_type: str # e.g., "paragraph", "line", "word", "table", "figure"
    confidence: Optional[float] = None

@dataclass
class TableCell:
    row_index: int
    column_index: int
    text_content: str
    bounding_box: List[float] # [x1, y1, x2, y2] normalized coordinates
    confidence: Optional[float] = None

@dataclass
class OCRResponse:
    extracted_text: str
    layout_blocks: List[LayoutBlock] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list) # List of tables, each a dict for flexibility
    raw_ocr_output: Optional[Dict[str, Any]] = None

@dataclass
class NormalizedDocument:
    normalized_text: str
    normalized_layout: List[LayoutBlock] = field(default_factory=list)
    normalized_tables: List[Dict[str, Any]] = field(default_factory=list)
    document_id: Optional[str] = None
