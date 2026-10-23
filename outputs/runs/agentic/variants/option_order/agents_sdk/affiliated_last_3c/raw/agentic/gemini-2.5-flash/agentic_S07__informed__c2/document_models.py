from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class BoundingRegion:
    page_number: int
    bounding_box: List[float] # List of 8 floats for 4 (x,y) points

@dataclass
class DocumentLine:
    content: str
    bounding_regions: List[BoundingRegion] = field(default_factory=list)

@dataclass
class DocumentParagraph:
    content: str
    bounding_regions: List[BoundingRegion] = field(default_factory=list)

@dataclass
class DocumentCell:
    content: str
    row_index: int
    column_index: int
    row_span: int = 1
    column_span: int = 1

@dataclass
class DocumentTable:
    cells: List[DocumentCell]
    page_number: Optional[int] = None

@dataclass
class DocumentKeyValue:
    key: str
    value: Optional[str]
    confidence: Optional[float]

@dataclass
class DocumentTextResult:
    content: str
    paragraphs: List[DocumentParagraph] = field(default_factory=list)
    lines: List[DocumentLine] = field(default_factory=list)

@dataclass
class DocumentLayoutResult(DocumentTextResult):
    tables: List[DocumentTable] = field(default_factory=list)

@dataclass
class DocumentFormResult(DocumentLayoutResult):
    key_value_pairs: List[DocumentKeyValue] = field(default_factory=list)

# These models are primarily for local representation/normalization if needed,
# as Azure SDKs return their own objects directly.
# This file serves as a placeholder for potential future local model definitions.
