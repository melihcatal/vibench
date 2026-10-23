from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class DocumentRequest:
    """Represents a request to process a document."""
    content: bytes
    mime_type: str

@dataclass
class TextExtractionResponse:
    """Response for plain text extraction."""
    text_content: str

@dataclass
class TableCell:
    """Represents a single cell in a table."""
    content: str

@dataclass
class TableRow:
    """Represents a row in a table."""
    cells: List[TableCell]

@dataclass
class Table:
    """Represents an extracted table."""
    rows: List[TableRow]

@dataclass
class TableExtractionResponse:
    """Response for table extraction."""
    text_content: str
    tables: List[Table] = field(default_factory=list)

@dataclass
class LayoutExtractionResponse:
    """Response for layout element extraction."""
    text_content: str
    blocks: List[str] = field(default_factory=list)
    lines: List[str] = field(default_factory=list)

@dataclass
class KeyValuePair:
    """Represents an extracted key-value pair."""
    key: str
    value: str

@dataclass
class KeyValuePairExtractionResponse:
    """Response for key-value pair extraction."""
    text_content: str
    key_value_pairs: List[KeyValuePair] = field(default_factory=list)

@dataclass
class TranslationResponse:
    """Response for text translation."""
    translated_text: str

@dataclass
class SafetyAnalysisResponse:
    """Response for content safety analysis."""
    is_safe: bool
    scores: Dict[str, float] = field(default_factory=dict)

@dataclass
class FieldExtractionResponse:
    """Response for structured field extraction."""
    fields: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EmbeddingResponse:
    """Response for text embedding."""
    embedding: List[float]

