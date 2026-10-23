from pydantic import BaseModel
from typing import Optional
import datetime

class ObjectMetadata(BaseModel):
    name: str
    bucket: str
    size: int
    content_type: Optional[str] = None
    updated: datetime.datetime
    md5_hash: Optional[str] = None
    crc32c: Optional[str] = None

class OcrResult(BaseModel):
    source_uri: str
    text_content: str
    language: str

class TranslationResult(BaseModel):
    original_text: str
    original_language: str
    translated_text: str
    target_language: str

class SummaryResult(BaseModel):
    source_text: str
    summary_text: str

class EmbeddingResult(BaseModel):
    source_content: str
    embedding: list[float]
