from typing import Dict, Any, List
from pydantic import BaseModel

class ObjectInfo(BaseModel):
    key: str
    size: int
    last_modified: str
    etag: str
    metadata: Dict[str, Any] = {}

class PresignedUrlResponse(BaseModel):
    url: str

class ObjectListingEntry(BaseModel):
    key: str
    last_modified: str
    etag: str
    size: int
    storage_class: str

class DocumentTextResponse(BaseModel):
    text_content: str
    detected_languages: List[str] = []

class TranslatedTextResponse(BaseModel):
    translated_text: str
    source_language_code: str
    target_language_code: str

class SummaryResponse(BaseModel):
    summary: str

class EmbeddingResponse(BaseModel):
    embedding: List[float]
