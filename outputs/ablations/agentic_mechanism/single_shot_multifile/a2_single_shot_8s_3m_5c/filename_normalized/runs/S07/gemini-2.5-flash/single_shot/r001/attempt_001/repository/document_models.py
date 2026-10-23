from typing import List, Dict, Any, Optional

class TextExtractionResult:
    text_content: str
    language_codes: List[str] = []

class LayoutBlock:
    bounding_boxes: List[List[int]]
    text: str
    block_type: str
    confidence: float = 0.0

class TableCell:
    row_index: int
    column_index: int
    text_content: str
    row_span: int = 1
    column_span: int = 1
    bounding_boxes: List[List[int]] = []

class Table:
    header_rows: List[List[TableCell]]
    body_rows: List[List[TableCell]]
    bounding_boxes: List[List[int]] = []
    caption: Optional[str] = None

class KeyValuePair:
    key: str
    value: str
    key_bounding_boxes: List[List[int]] = []
    value_bounding_boxes: List[List[int]] = []
    confidence: float = 0.0

class DocumentExtractionResult:
    text: Optional[TextExtractionResult] = None
    layout_blocks: List[LayoutBlock] = []
    tables: List[Table] = []
    key_value_pairs: List[KeyValuePair] = []
    raw_response: Dict[str, Any] = {}

class TranslatedTextResult:
    translated_text: str
    source_language_code: str
    target_language_code: str

class SafetyAttribute:
    category: str
    probability: str
    severity: Optional[str] = None

class SafetyCheckResult:
    safety_attributes: List[SafetyAttribute]
    is_safe: bool
    raw_response: Dict[str, Any] = {}

class ExtractedField:
    field_name: str
    field_value: str
    confidence: Optional[float] = None
    source_text_segments: List[str] = []

class DocumentFieldsExtractionResult:
    fields: List[ExtractedField]
    raw_response: Dict[str, Any] = {}

class EmbeddingResult:
    embedding: List[float]
    text_segment: str
    model_id: str