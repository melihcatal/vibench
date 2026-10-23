from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class StorageObject(BaseModel):
    bucket: str
    key: str


class UploadRequest(BaseModel):
    storage_object: StorageObject
    file_path: Optional[str] = None
    file_content: Optional[bytes] = None


class PresignedUrlRequest(BaseModel):
    storage_object: StorageObject
    expiration: int = 3600


class ObjectMetadata(BaseModel):
    key: str
    version_id: Optional[str] = None
    size: int
    last_modified: str
    etag: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ListPrefixRequest(BaseModel):
    bucket: str
    prefix: str


class ListedObject(BaseModel):
    key: str
    size: int
    last_modified: str


class OcrRequest(BaseModel):
    storage_object: StorageObject


class TranslateRequest(BaseModel):
    text: str
    source_language: str = "auto"
    target_language: str


class SummaryRequest(BaseModel):
    text: str


class EmbeddingRequest(BaseModel):
    text: str
    metadata: Dict[str, Any]
