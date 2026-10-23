from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ExtractedCell:
    text: str
    row_span: int = 1
    col_span: int = 1

@dataclass
class ExtractedRow:
    cells: List[ExtractedCell]
    row_type: str = "body" # "header" or "body"

@dataclass
class ExtractedTable:
    page_number: int
    rows: List[ExtractedRow]
    bounds: Optional[List[float]] = None # Bounding box coordinates

@dataclass
class ExtractedKeyValue:
    page_number: int
    key: str
    value: str
    key_bounds: Optional[List[float]] = None
    value_bounds: Optional[List[float]] = None

@dataclass
class ExtractedLayoutElement:
    text: str
    element_type: str # e.g., "block", "line", "token"
    page_number: int
    bounds: Optional[List[float]] = None

@dataclass
class DocumentExtractionResult:
    text: str = ""
    layout_elements: List[ExtractedLayoutElement] = field(default_factory=list)
    tables: List[ExtractedTable] = field(default_factory=list)
    key_values: List[ExtractedKeyValue] = field(default_factory=list)


# Helper for converting Document AI text_anchor to actual text (simplified for models)
# In a real scenario, this would reference the full document.text and text_anchor offsets.
def get_text_from_text_anchor(text_anchor: Any, full_text: str) -> str:
    if not text_anchor.text_segments: # type: ignore
        return ""
    
    # Assuming for simplicity that there's usually one segment and it refers to full_text
    start_index = text_anchor.text_segments[0].start_index # type: ignore
    end_index = text_anchor.text_segments[0].end_index # type: ignore
    return full_text[start_index:end_index]
