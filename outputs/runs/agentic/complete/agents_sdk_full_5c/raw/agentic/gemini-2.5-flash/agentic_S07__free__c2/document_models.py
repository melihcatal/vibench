from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class DocumentProcessingRequest:
    file_content: bytes
    mime_type: str
    project_id: str
    location: str

@dataclass
class TextExtractionResponse:
    text: str

@dataclass
class LayoutBlock:
    text_content: str
    block_type: str  # e.g., "paragraph", "line", "table"
    # Add bounding box, confidence, etc., if needed for richer layout extraction

@dataclass
class LayoutExtractionResponse:
    layout_blocks: List[LayoutBlock]

@dataclass
class TableCell:
    content: str
    # Add row_span, col_span, bounding_box, etc., for richer table info

@dataclass
class TableRow:
    cells: List[TableCell]

@dataclass
class ExtractedTable:
    header_rows: List[TableRow]
    body_rows: List[TableRow]

@dataclass
class TableExtractionResponse:
    tables: List[ExtractedTable]

@dataclass
class KeyValueParagraph:
    key: str
    value: str

@dataclass
class KeyValueExtractionResponse:
    key_value_pairs: List[KeyValueParagraph]

@dataclass
class TranslationRequest:
    text_content: str
    target_language: str
    source_language: Optional[str] = None

@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: Optional[str] = None

@dataclass
class SafetyCheckRequest:
    text_content: str

@dataclass
class SafetyAttribute:
    category: str
    score: float

@dataclass
class SafetyCheckResponse:
    safety_attributes: List[SafetyAttribute]
    is_safe: bool

@dataclass
class FieldExtractionRequest:
    document_text: str
    extraction_schema: Dict[str, Any]  # JSON schema for desired output

@dataclass
class FieldExtractionResponse:
    extracted_data: Dict[str, Any]

@dataclass
class EmbeddingRequest:
    text_segments: List[str]

@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
