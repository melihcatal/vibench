from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class UploadObjectRequest:
    container_name: str
    blob_name: str
    data: bytes
    content_settings: Optional[Dict[str, Any]] = None

@dataclass
class UploadObjectResponse:
    success: bool
    blob_url: Optional[str] = None
    e_tag: Optional[str] = None
    last_modified: Optional[str] = None
    error: Optional[str] = None

@dataclass
class PresignedDownloadRequest:
    container_name: str
    blob_name: str
    expiry_minutes: int = 60

@dataclass
class PresignedDownloadResponse:
    success: bool
    presigned_url: Optional[str] = None
    error: Optional[str] = None

@dataclass
class ObjectMetadataRequest:
    container_name: str
    blob_name: str

@dataclass
class ObjectMetadataResponse:
    success: bool
    name: Optional[str] = None
    size: Optional[int] = None
    creation_time: Optional[str] = None
    last_modified: Optional[str] = None
    e_tag: Optional[str] = None
    content_settings: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, str]] = None
    error: Optional[str] = None

@dataclass
class ListPrefixRequest:
    container_name: str
    prefix: Optional[str] = None

@dataclass
class ListPrefixResponse:
    success: bool
    blob_names: Optional[list[str]] = None
    error: Optional[str] = None

@dataclass
class StoredDocumentOcrRequest:
    container_name: str
    blob_name: str

@dataclass
class StoredDocumentOcrResponse:
    success: bool
    text_content: Optional[str] = None
    error: Optional[str] = None

@dataclass
class StoredTextTranslateRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None

@dataclass
class StoredTextTranslateResponse:
    success: bool
    translated_text: Optional[str] = None
    error: Optional[str] = None

@dataclass
class StoredAssetSummaryRequest:
    container_name: str
    blob_name: str
    max_sentences: int = 3

@dataclass
class StoredAssetSummaryResponse:
    success: bool
    summary: Optional[str] = None
    error: Optional[str] = None

@dataclass
class AssetMetadataEmbeddingRequest:
    container_name: str
    blob_name: str
    text_content: Optional[str] = None

@dataclass
class AssetMetadataEmbeddingResponse:
    success: bool
    embedding: Optional[list[float]] = None
    error: Optional[str] = None
