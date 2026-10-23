from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class UploadObjectRequest(BaseModel):
    bucket_name: str
    object_key: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: Optional[str] = None


class UploadObjectResponse(BaseModel):
    success: bool
    message: str
    object_url: Optional[str] = None


class PresignedDownloadRequest(BaseModel):
    bucket_name: str
    object_key: str
    expiration_seconds: int = 3600


class PresignedDownloadResponse(BaseModel):
    success: bool
    message: str
    presigned_url: Optional[str] = None


class ObjectMetadataRequest(BaseModel):
    bucket_name: str
    object_key: str


class ObjectMetadataResponse(BaseModel):
    success: bool
    message: str
    metadata: Optional[Dict[str, Any]] = None


class ListPrefixRequest(BaseModel):
    bucket_name: str
    prefix: str
    max_keys: int = 100


class ObjectSummary(BaseModel):
    key: str
    last_modified: Optional[str] = None
    etag: Optional[str] = None
    size: Optional[int] = None


class ListPrefixResponse(BaseModel):
    success: bool
    message: str
    objects: List[ObjectSummary] = []
    next_continuation_token: Optional[str] = None


class StoredDocumentOCRRequest(BaseModel):
    bucket_name: str
    object_key: str


class StoredDocumentOCRResponse(BaseModel):
    success: bool
    message: str
    extracted_text: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None


class StoredTextTranslateRequest(BaseModel):
    text: str
    source_language_code: str
    target_language_code: str


class StoredTextTranslateResponse(BaseModel):
    success: bool
    message: str
    translated_text: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None


class StoredAssetSummaryRequest(BaseModel):
    text: str
    language_code: str = "en"


class StoredAssetSummaryResponse(BaseModel):
    success: bool
    message: str
    summary_text: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None


class AssetMetadataEmbeddingRequest(BaseModel):
    text_to_embed: str


class AssetMetadataEmbeddingResponse(BaseModel):
    success: bool
    message: str
    embedding: Optional[List[float]] = None
    raw_response: Optional[Dict[str, Any]] = None
