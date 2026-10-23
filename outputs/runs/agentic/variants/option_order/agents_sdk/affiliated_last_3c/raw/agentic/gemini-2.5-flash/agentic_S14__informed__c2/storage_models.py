from pydantic import BaseModel
from typing import Dict, Any, Optional

class StoredObject(BaseModel):
    bucket_name: str
    object_name: str
    last_modified: str
    etag: str
    size: int

class ObjectMetadata(StoredObject):
    content_type: Optional[str] = None
    user_metadata: Dict[str, str] = {}

class OCRResult(BaseModel):
    job_id: Optional[str] = None
    text_content: Optional[str] = None
    pages: Optional[int] = None
    status: Optional[str] = None

class TranslationResult(BaseModel):
    translated_text: str
    source_language_code: str
    target_language_code: str

class SummaryResult(BaseModel):
    summary_text: str
    model_id: str

class EmbeddingResult(BaseModel):
    embedding_vector: list[float]
    model_id: str
    input_text: str
