from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class DocumentInput(BaseModel):
    image_bytes: bytes
    mime_type: str

class TextExtractionOutput(BaseModel):
    text: str

class LayoutElement(BaseModel):
    type: str
    text: str
    bounding_box: List[float] # Flat list of [x1, y1, x2, y2, ...]

class LayoutExtractionOutput(BaseModel):
    elements: List[LayoutElement]

class TableCell(BaseModel):
    text: str
    row_span: int = 1
    col_span: int = 1

class TableRow(BaseModel):
    cells: List[TableCell]

class Table(BaseModel):
    rows: List[TableRow]

class TableExtractionOutput(BaseModel):
    tables: List[Table]

class KeyValuePair(BaseModel):
    key: str
    value: str

class KeyValueExtractionOutput(BaseModel):
    pairs: List[KeyValuePair]

class TranslationInput(BaseModel):
    text: str
    target_lang: str
    source_lang: Optional[str] = None

class TranslationOutput(BaseModel):
    translated_text: str
    detected_source_lang: Optional[str] = None

class SafetyCheckInput(BaseModel):
    text: str

class SafetyCheckOutput(BaseModel):
    unsafe: bool
    categories: Dict[str, float] = Field(default_factory=dict)
    category_scores: Dict[str, float] = Field(default_factory=dict) # OpenAI specific

class FieldExtractionInput(BaseModel):
    document_text: str
    fields_to_extract: Dict[str, str] # e.g., {'invoice_number': 'string', 'total_amount': 'float'}

class FieldExtractionOutput(BaseModel):
    extracted_fields: Dict[str, Any]

class EmbeddingInput(BaseModel):
    text_segments: List[str]

class EmbeddingOutput(BaseModel):
    embeddings: List[List[float]]
