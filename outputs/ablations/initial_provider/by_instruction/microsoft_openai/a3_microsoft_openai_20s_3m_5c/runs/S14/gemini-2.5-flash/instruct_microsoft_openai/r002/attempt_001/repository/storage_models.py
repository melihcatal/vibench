import dataclasses
from typing import Optional, Dict, Any, List

@dataclasses.dataclass
class UploadObjectRequest:
    container_name: str
    blob_name: str
    data: bytes
    content_settings: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class UploadObjectResponse:
    message: str
    etag: str

@dataclasses.dataclass
class PresignedDownloadRequest:
    container_name: str
    blob_name: str
    expiry_minutes: int = 60

@dataclasses.dataclass
class PresignedDownloadResponse:
    presigned_url: str

@dataclasses.dataclass
class ObjectMetadataRequest:
    container_name: str
    blob_name: str

@dataclasses.dataclass
class ObjectMetadataResponse:
    metadata: Dict[str, Any]
    size: int
    last_modified: str
    etag: str

@dataclasses.dataclass
class ListPrefixRequest:
    container_name: str
    prefix: Optional[str] = None

@dataclasses.dataclass
class ListPrefixResponse:
    blob_names: List[str]

@dataclasses.dataclass
class StoredDocumentOCRRequest:
    container_name: str
    blob_name: str

@dataclasses.dataclass
class StoredDocumentOCRResponse:
    text_content: str
    language: Optional[str] = None

@dataclasses.dataclass
class StoredTextTranslateRequest:
    text_content: str
    target_language: str
    source_language: Optional[str] = None

@dataclasses.dataclass
class StoredTextTranslateResponse:
    translated_text: str
    source_language: Optional[str] = None

@dataclasses.dataclass
class StoredAssetSummaryRequest:
    container_name: str
    blob_name: str
    model: str = "gpt-35-turbo"

@dataclasses.dataclass
class StoredAssetSummaryResponse:
    summary: str

@dataclasses.dataclass
class AssetMetadataEmbeddingRequest:
    container_name: str
    blob_name: str
    text_content: Optional[str] = None
    model: str = "text-embedding-ada-002"

@dataclasses.dataclass
class AssetMetadataEmbeddingResponse:
    embedding: List[float]
    model: str
