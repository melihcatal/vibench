from typing import List, Dict, Any, Optional

class DocumentPayload:
    """Represents the input payload for document processing."""
    document_bytes: bytes
    mime_type: Optional[str] = None
    file_name: Optional[str] = None

    def __init__(self, document_bytes: bytes, mime_type: Optional[str] = None, file_name: Optional[str] = None):
        self.document_bytes = document_bytes
        self.mime_type = mime_type
        self.file_name = file_name

class ExtractionResult:
    """Base class for all document extraction results."""
    pass

class TextExtractionResult(ExtractionResult):
    """Result for plain text extraction."""
    text: str

    def __init__(self, text: str):
        self.text = text

class LayoutBlock:
    """Represents a generic layout block in a document."""
    block_type: str # e.g., 'WORD', 'LINE', 'TABLE', 'KEY_VALUE_SET'
    text: Optional[str] = None
    geometry: Dict[str, Any] # Bounding box information

    def __init__(self, block_type: str, text: Optional[str] = None, geometry: Dict[str, Any] = None):
        self.block_type = block_type
        self.text = text
        self.geometry = geometry if geometry is not None else {}

class LayoutExtractionResult(ExtractionResult):
    """Result for layout element extraction."""
    blocks: List[LayoutBlock]

    def __init__(self, blocks: List[LayoutBlock]):
        self.blocks = blocks

class TableCell:
    """Represents a cell within a table."""
    row_index: int
    column_index: int
    content: str
    geometry: Dict[str, Any]

    def __init__(self, row_index: int, column_index: int, content: str, geometry: Dict[str, Any]):
        self.row_index = row_index
        self.column_index = column_index
        self.content = content
        self.geometry = geometry

class Table:
    """Represents a table structure."""
    rows: List[List[TableCell]]
    geometry: Dict[str, Any]

    def __init__(self, rows: List[List[TableCell]], geometry: Dict[str, Any]):
        self.rows = rows
        self.geometry = geometry

class TableExtractionResult(ExtractionResult):
    """Result for table extraction."""
    tables: List[Table]

    def __init__(self, tables: List[Table]):
        self.tables = tables

class KeyValue:
    """Represents a key-value pair."""
    key: str
    value: str
    key_geometry: Dict[str, Any]
    value_geometry: Dict[str, Any]

    def __init__(self, key: str, value: str, key_geometry: Dict[str, Any] = None, value_geometry: Dict[str, Any] = None):
        self.key = key
        self.value = value
        self.key_geometry = key_geometry if key_geometry is not None else {}
        self.value_geometry = value_geometry if value_geometry is not None else {}

class KeyValueExtractionResult(ExtractionResult):
    """Result for key-value pair extraction."""
    key_values: List[KeyValue]

    def __init__(self, key_values: List[KeyValue]):
        self.key_values = key_values

class TranslationResult:
    """Result for text translation."""
    translated_text: str
    source_language: Optional[str] = None
    target_language: str

    def __init__(self, translated_text: str, target_language: str, source_language: Optional[str] = None):
        self.translated_text = translated_text
        self.target_language = target_language
        self.source_language = source_language

class SafetyRating:
    """Represents a safety rating for a content category."""
    category: str
    probability: str # e.g., 'VERY_UNLIKELY', 'UNLIKELY', 'NEGLIGIBLE', 'LOW', 'MEDIUM', 'HIGH'

    def __init__(self, category: str, probability: str):
        self.category = category
        self.probability = probability

class SafetyCheckResult:
    """Result for content safety check."""
    safety_ratings: List[SafetyRating]

    def __init__(self, safety_ratings: List[SafetyRating]):
        self.safety_ratings = safety_ratings

class Field:
    """Represents a structured field extracted from a document."""
    field_name: str
    field_value: str
    confidence: Optional[float] = None

    def __init__(self, field_name: str, field_value: str, confidence: Optional[float] = None):
        self.field_name = field_name
        self.field_value = field_value
        self.confidence = confidence

class FieldExtractionResult(ExtractionResult):
    """Result for structured field extraction."""
    fields: List[Field]

    def __init__(self, fields: List[Field]):
        self.fields = fields

class EmbeddingResult:
    """Result for text embedding."""
    embedding: List[float]

    def __init__(self, embedding: List[float]):
        self.embedding = embedding
