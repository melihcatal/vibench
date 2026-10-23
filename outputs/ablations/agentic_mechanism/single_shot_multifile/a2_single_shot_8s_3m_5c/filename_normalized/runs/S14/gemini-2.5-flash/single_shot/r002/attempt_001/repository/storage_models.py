from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class UploadObjectRequest(BaseModel):
    bucket: str
    key: str
    data: bytes
    content_type: str = "application/octet-stream"

class UploadObjectResponse(BaseModel):
    bucket: str
    key: str
    etag: str

class PresignedDownloadRequest(BaseModel):
    bucket: str
    key: str
    expires_in: int = 3600  # seconds

class PresignedDownloadResponse(BaseModel):
    url: str

class ObjectMetadataRequest(BaseModel):
    bucket: str
    key: str

class ObjectMetadataResponse(BaseModel):
    bucket: str
    key: str
    size: int
    content_type: str
    etag: str
    last_modified: Optional[str] # ISO format string
    metadata: Dict[str, str]

class ListedObject(BaseModel):
    key: str
    size: int
    last_modified: str # ISO format string

class ListPrefixRequest(BaseModel):
    bucket: str
    prefix: str = ""
    max_keys: int = 100

class ListPrefixResponse(BaseModel):
    objects: List[ListedObject]
    next_continuation_token: Optional[str]

class StoredDocumentOcrRequest(BaseModel):
    bucket: str
    key: str

class StoredDocumentOcrResponse(BaseModel):
    text: str

class StoredTextTranslateRequest(BaseModel):
    text: str
    source_language: str
    target_language: str

class StoredTextTranslateResponse(BaseModel):
    translated_text: str

class StoredAssetSummaryRequest(BaseModel):
    text: str
    max_tokens: int = 200

class StoredAssetSummaryResponse(BaseModel):
    summary: str

class AssetMetadataEmbeddingRequest(BaseModel):
    text: str

class AssetMetadataEmbeddingResponse(BaseModel):
    embedding: List[float]
