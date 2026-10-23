from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class UploadObjectRequest:
    container_name: str
    blob_name: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    metadata: Optional[Dict[str, str]] = None

@dataclass
class UploadObjectResponse:
    success: bool
    blob_url: Optional[str] = None
    error: Optional[str] = None

@dataclass
class PresignedDownloadRequest:
    container_name: str
    blob_name: str
    expiry_minutes: int = 60

@dataclass
class PresignedDownloadResponse:
    success: bool
    download_url: Optional[str] = None
    error: Optional[str] = None

@dataclass
class ObjectMetadataRequest:
    container_name: str
    blob_name: str

@dataclass
class ObjectMetadataResponse:
    success: bool
    metadata: Optional[Dict[str, str]] = None
    size: Optional[int] = None
    last_modified: Optional[str] = None
    error: Optional[str] = None

@dataclass
class ListPrefixRequest:
    container_name: str
    prefix: Optional[str] = None

@dataclass
class ListedObject:
    name: str
    size: int
    last_modified: str

@dataclass
class ListPrefixResponse:
    success: bool
    objects: Optional[List[ListedObject]] = None
    error: Optional[str] = None

@dataclass
class StoredDocumentOcrRequest:
    container_name: str
    blob_name: str

@dataclass
class StoredDocumentOcrResponse:
    success: bool
    extracted_text: Optional[str] = None
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
    text: str
    summary_length: str = "short" # e.g., 'short', 'medium', 'long'

@dataclass
class StoredAssetSummaryResponse:
    success: bool
    summary: Optional[str] = None
    error: Optional[str] = None

@dataclass
class AssetMetadataEmbeddingRequest:
    text_content: str
    metadata_tags: Optional[Dict[str, str]] = None

@dataclass
class AssetMetadataEmbeddingResponse:
    success: bool
    embedding: Optional[List[float]] = None
    error: Optional[str] = None
