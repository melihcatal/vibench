from pydantic import BaseModel, Field, Literal, Optional
from typing import Dict, List, Tuple, Union
from typing import TypedDict


class TextExtractionRequest(BaseModel):
    """Request payload for plain text OCR."""
    image_path: str = Field(..., description="Path to the scanned document image. For hosted APIs use a multipart upload.")


class TextExtractionResponse(BaseModel):
    """Response payload from plain text extraction."""
    text: str = Field(..., description="Extracted plain text.")
    confidence: Optional[float] = Field(None, description="Confidence score from the OCR service.")


class LayoutElement(BaseModel):
    """A generic layout element (block, line, or table)."""
    type: Literal['block', 'line', 'table'] = Field(..., description="Element type.")
    bounding_box: List[float] = Field(..., description="[x0, y0, x1, y1] coordinates in pixels or normalized units.")


class LayoutExtractionResponse(BaseModel):
    """Response containing multiple layout elements."""
    elements: List[LayoutElement]


class TableCell(BaseModel):
    """Cell inside a table grid."""
    content: str = Field(..., description="Cell textual content.")
    column: int = Field(..., description="Zero‑based column index.")
    row: int = Field(..., description="Zero‑based row index.")


class TableRow(BaseModel):
    """A single row composed of cells."""
    cells: List[TableCell] = Field(...)


class TableExtractionResponse(BaseModel):
    """Response containing extracted table rows."""
    rows: List[TableRow]


class KeyValueExtractionResponse(TypedDict):
    """Key‑value pair list extracted from a form.",
    pairs: List[Tuple[str, str]]


class TranslatedTextResponse(TypedDict):
    """Translation output."""
    translated_text: str
    detected_source_language: Optional[str]


class UnsafeContentCheckResponse(TypedDict):
    """Safety/violence detection result."""
    is_unsafe: bool


class FieldType(Literal['text', 'date', 'number', 'boolean']):
    """Allowed field types for a structured schema.""


class Field(BaseModel):
    """Structured field after parsing OCR text with a hosted parser."""
    name: str = Field(..., description="Field identifier.")
    value: str = Field(..., description="Extracted value.")
    type_: FieldType = Field(..., description="Semantic type of the field.")


class FieldExtractionResponse(BaseModel):
    """Result of a hosted form parser.",
    fields: List[Field]


class EmbeddingRequest(BaseModel):
    """Request to embed a list of text chunks."""
    texts: List[str] = Field(..., description="Chunks of text to embed, e.g. per section of a document.")
    model: Optional[str] = Field(None, description="Identifier of the embedding model, defaults to MiniLM if omitted.")


class EmbeddingResponse(BaseModel):
    """Response containing a list of embedding vectors.",
    embeddings: List[List[float]]
