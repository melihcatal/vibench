from typing import Optional, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime

class StoredObject(BaseModel):
    """Represents a single object in a storage bucket."""
    key: str
    size: int
    last_modified: datetime
    etag: str = Field(..., alias="ETag")

class ObjectMetadata(BaseModel):
    """Represents the metadata of a stored object."""
    key: str
    content_length: int
    content_type: str
    last_modified: datetime
    etag: str
    metadata: Optional[Dict[str, str]] = None
    version_id: Optional[str] = None

class OcrJobRequest(BaseModel):
    """Request model for starting an OCR job on a stored document."""
    bucket_name: str
    object_key: str

class TranslationRequest(BaseModel):
    """Request model for translating extracted text."""
    text: str
    source_language_code: str = "auto"
    target_language_code: str

class SummaryRequest(BaseModel):
    """Request model for summarizing content."""
    text: str
    length: str = "medium" # short, medium, long
    format: str = "paragraph" # paragraph, bullets

class EmbeddingRequest(BaseModel):
    """Request model for creating embeddings from text."""
    text_content: str
