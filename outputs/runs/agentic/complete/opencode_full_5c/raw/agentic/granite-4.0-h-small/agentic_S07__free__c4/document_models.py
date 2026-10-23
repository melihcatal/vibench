from pydantic import BaseModel, Field
from typing import List, Dict, Any


class OCRRequest(BaseModel):
    """Request model for sending an image for OCR processing."""

    image_bytes: bytes = Field(..., description="Raw image bytes.")
    language: str = Field(default="en", description="Language code for OCR.")


class OCRResponse(BaseModel):
    """Normalized response containing extracted text."""

    text: str = Field(..., description="Plain text extracted from the image.")


class LayoutRequest(BaseModel):
    """Request model for layout extraction."""

    image_bytes: bytes
    pages: int = Field(default=1, description="Number of pages to process.")


class LayoutResponse(BaseModel):
    """Normalized layout response containing blocks, lines, and tables."""

    blocks: List[Dict[str, Any]] = Field(
        default_factory=list, description="Document blocks."
    )
    lines: List[Dict[str, Any]] = Field(default_factory=list, description="Text lines.")
    tables: List[Dict[str, Any]] = Field(
        default_factory=list, description="Detected tables."
    )


class TableRequest(BaseModel):
    """Request model for table extraction."""

    image_bytes: bytes


class TableResponse(BaseModel):
    """Normalized tabular data response."""

    tables: List[Dict[str, Any]] = Field(
        default_factory=list, description="List of tables with cell structure."
    )


class KeyValueRequest(BaseModel):
    """Request model for key-value pair extraction from forms."""

    image_bytes: bytes
    form_fields: List[str] = Field(
        default_factory=list, description="Optional list of expected field names."
    )


class KeyValueResponse(BaseModel):
    """Normalized key-value pair response."""

    key_values: Dict[str, str] = Field(
        default_factory=dict, description="Mapping of field names to extracted values."
    )


class TranslationRequest(BaseModel):
    """Request model for translating extracted text."""

    source_text: str
    target_lang: str = Field(default="es", description="Target language code.")


class TranslationResponse(BaseModel):
    """Response containing translated text."""

    translated_text: str


class SafetyCheckRequest(BaseModel):
    """Request model for safety/content moderation check."""

    text: str


class SafetyCheckResponse(BaseModel):
    """Response indicating whether the text is safe and any flagged categories."""

    is_safe: bool
    flagged_categories: List[str] = Field(default_factory=list)


class FieldExtractionRequest(BaseModel):
    """Request model for extracting structured fields from OCR-normalized text."""

    text: str
    schema: Dict[str, Any] = Field(
        ..., description="JSON schema describing expected field names/types."
    )


class FieldExtractionResponse(BaseModel):
    """Structured fields extracted from the document."""

    extracted_fields: Dict[str, Any]


class EmbeddingRequest(BaseModel):
    """Request model for generating embeddings of document sections."""

    sections: List[str] = Field(
        default_factory=list, description="List of text sections to embed."
    )


class EmbeddingResponse(BaseModel):
    """Embedding vector per section."""

    embeddings: List[List[float]]
