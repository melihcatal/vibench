import dataclasses
from typing import Dict, Any, List, Optional


@dataclasses.dataclass
class UploadObjectRequest:
    bucket_name: str
    object_key: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: str = "application/octet-stream"


@dataclasses.dataclass
class UploadObjectResponse:
    success: bool
    message: str
    etag: Optional[str] = None
    version_id: Optional[str] = None


@dataclasses.dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_key: str
    expiration: int = 3600  # Seconds


@dataclasses.dataclass
class PresignedDownloadResponse:
    success: bool
    url: Optional[str] = None
    message: str = ""


@dataclasses.dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_key: str


@dataclasses.dataclass
class ObjectMetadataResponse:
    success: bool
    metadata: Optional[Dict[str, Any]] = None
    message: str = ""


@dataclasses.dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str
    max_keys: int = 1000


@dataclasses.dataclass
class ListedObject:
    key: str
    last_modified: str
    etag: str
    size: int


@dataclasses.dataclass
class ListPrefixResponse:
    success: bool
    objects: List[ListedObject]
    message: str = ""


@dataclasses.dataclass
class StoredDocumentOCRRequest:
    bucket_name: str
    object_key: str


@dataclasses.dataclass
class StoredDocumentOCRResponse:
    success: bool
    text_content: Optional[str] = None
    message: str = ""


@dataclasses.dataclass
class StoredTextTranslateRequest:
    text: str
    source_language_code: str
    target_language_code: str


@dataclasses.dataclass
class StoredTextTranslateResponse:
    success: bool
    translated_text: Optional[str] = None
    message: str = ""


@dataclasses.dataclass
class StoredAssetSummaryRequest:
    text_content: str
    max_tokens: int = 500


@dataclasses.dataclass
class StoredAssetSummaryResponse:
    success: bool
    summary: Optional[str] = None
    message: str = ""


@dataclasses.dataclass
class AssetMetadataEmbeddingRequest:
    text: str


@dataclasses.dataclass
class AssetMetadataEmbeddingResponse:
    success: bool
    embedding: Optional[List[float]] = None
    message: str = ""
