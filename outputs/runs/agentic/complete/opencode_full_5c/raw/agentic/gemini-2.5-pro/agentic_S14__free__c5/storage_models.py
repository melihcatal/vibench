from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class StorageObject(BaseModel):
    name: str
    bucket: str
    size: Optional[int] = None
    content_type: Optional[str] = None


class PresignedUrlResponse(BaseModel):
    object_name: str
    url: str
    expiration_seconds: int


class ObjectMetadata(BaseModel):
    name: str
    bucket: str
    size: int
    content_type: str
    create_time: str
    update_time: str
    custom_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class ExtractedText(BaseModel):
    source_object: str
    text: str


class TranslatedText(BaseModel):
    source_text: str
    translated_text: str
    target_language: str


class AssetSummary(BaseModel):
    source_object: str
    summary: str


class AssetEmbedding(BaseModel):
    source_object: str
    embedding: List[float]
    model: str
