from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class ObjectMetadata(BaseModel):
    name: str
    bucket: str
    content_type: Optional[str] = None
    size: int
    time_created: datetime
    custom_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class OCRResponse(BaseModel):
    text: str


class TranslationResponse(BaseModel):
    translated_text: str
    detected_source_language: Optional[str] = None


class SummaryResponse(BaseModel):
    summary: str


class EmbeddingResponse(BaseModel):
    embedding: list[float]
