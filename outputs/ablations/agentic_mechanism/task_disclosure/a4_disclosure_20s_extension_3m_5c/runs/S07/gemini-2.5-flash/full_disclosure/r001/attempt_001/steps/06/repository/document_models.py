from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class BoundingBox:
    x1: int
    y1: int
    x2: int
    y2: int

@dataclass
class Word:
    text: str
    bounding_box: BoundingBox
    confidence: Optional[float] = None

@dataclass
class Paragraph:
    text: str
    bounding_box: BoundingBox
    words: List[Word] = field(default_factory=list)

@dataclass
class Block:
    text: str
    bounding_box: BoundingBox
    paragraphs: List[Paragraph] = field(default_factory=list)

@dataclass
class Page:
    page_number: int
    width: int
    height: int
    blocks: List[Block] = field(default_factory=list)

@dataclass
class OcrResponse:
    full_text: str
    pages: List[Page] = field(default_factory=list)
    language_codes: List[str] = field(default_factory=list)

@dataclass
class OcrRequest:
    image_content: bytes
    language_hints: Optional[List[str]] = field(default_factory=list)

@dataclass
class LayoutElement:
    type: str  # e.g., "text_block", "table", "form_field", "line", "word"
    text: Optional[str] = None
    bounding_box: Optional[BoundingBox] = None
    children: List["LayoutElement"] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict) # e.g., for table rows/columns, form field key/value

@dataclass
class LayoutResponse:
    elements: List[LayoutElement] = field(default_factory=list)
    page_dimensions: List[Dict[str, int]] = field(default_factory=list) # e.g., [{"page_number": 1, "width": 100, "height": 200}]

@dataclass
class LayoutRequest:
    image_content: bytes
    features: List[str] = field(default_factory=list) # e.g., ["text_blocks", "tables", "form_fields", "lines", "words"]
