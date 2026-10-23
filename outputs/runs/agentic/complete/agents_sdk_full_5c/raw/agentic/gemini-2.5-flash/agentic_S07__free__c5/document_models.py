from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class TextSegment:
    start_index: int
    end_index: int

@dataclass
class TextAnchor:
    text_segments: List[TextSegment] = field(default_factory=list)

@dataclass
class BoundingPoly:
    # Simplified for example; real BoundingPoly has vertices
    pass

@dataclass
class Layout:
    text_anchor: TextAnchor
    bounding_poly: Optional[BoundingPoly] = None
    confidence: float = 0.0

@dataclass
class Block:
    layout: Layout

@dataclass
class Line:
    layout: Layout

@dataclass
class Token:
    layout: Layout

@dataclass
class TableCell:
    text: str
    row_span: int = 1
    col_span: int = 1

@dataclass
class TableRow:
    cells: List[TableCell] = field(default_factory=list)

@dataclass
class DocumentTable:
    num_rows: int
    num_cols: int
    header_rows: List[TableRow] = field(default_factory=list)
    body_rows: List[TableRow] = field(default_factory=list)

@dataclass
class FormField:
    field_name: str
    field_value: str
    confidence: float = 0.0

@dataclass
class DocumentPage:
    page_number: int
    text: str
    blocks: List[Block] = field(default_factory=list)
    lines: List[Line] = field(default_factory=list)
    tokens: List[Token] = field(default_factory=list)
    tables: List[DocumentTable] = field(default_factory=list)
    form_fields: List[FormField] = field(default_factory=list)

@dataclass
class ProcessedDocument:
    text: str
    pages: List[DocumentPage] = field(default_factory=list)
    key_value_pairs: Dict[str, str] = field(default_factory=dict)
    tables: List[DocumentTable] = field(default_factory=list)

@dataclass
class TranslatedText:
    text: str
    detected_language_code: Optional[str] = None

@dataclass
class SafetyRating:
    category: str
    probability: str # e.g., "UNLIKELY", "POSSIBLE", "LIKELY", "VERY_LIKELY"

@dataclass
class SafetyCheckResult:
    is_safe: bool
    safety_ratings: List[SafetyRating] = field(default_factory=list)

@dataclass
class ExtractedField:
    field_name: str
    field_value: str
    confidence: Optional[float] = None

@dataclass
class Embedding:
    values: List[float]

if __name__ == '__main__':
    # Example usage of a dataclass
    segment = TextSegment(start_index=0, end_index=5)
    anchor = TextAnchor(text_segments=[segment])
    layout = Layout(text_anchor=anchor, confidence=0.95)
    block = Block(layout=layout)
    page = DocumentPage(page_number=1, text="Hello World", blocks=[block])
    print(page)
