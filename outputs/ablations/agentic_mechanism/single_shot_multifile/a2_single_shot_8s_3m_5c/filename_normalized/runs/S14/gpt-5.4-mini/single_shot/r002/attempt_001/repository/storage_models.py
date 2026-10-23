from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


def normalize_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not metadata:
        return {}
    return {str(k).lower(): str(v) for k, v in metadata.items() if v is not None}


@dataclass
class UploadRequest:
    bucket: Optional[str]
    key: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    content_type: Optional[str] = None
    acl: Optional[str] = None
    cache_control: Optional[str] = None
    content_disposition: Optional[str] = None
    content_encoding: Optional[str] = None
    sse: Optional[str] = None
    sse_kms_key_id: Optional[str] = None


@dataclass
class UploadResponse:
    bucket: str
    key: str
    etag: str
    content_length: int
    metadata: Dict[str, str]
    content_type: Optional[str] = None


@dataclass
class PresignedUrlRequest:
    bucket: Optional[str]
    key: str
    expires_in_seconds: int = 3600


@dataclass
class PresignedUrlResponse:
    bucket: str
    key: str
    url: str
    expires_in_seconds: int


@dataclass
class ObjectMetadataResponse:
    bucket: str
    key: str
    etag: str
    content_length: int
    content_type: Optional[str]
    last_modified: Any
    metadata: Dict[str, str]
    storage_class: Optional[str]
    version_id: Optional[str]


@dataclass
class ListPrefixRequest:
    bucket: Optional[str]
    prefix: Optional[str] = None
    delimiter: Optional[str] = None


@dataclass
class ListedObject:
    bucket: str
    key: str
    size: int
    last_modified: Any
    etag: str
    storage_class: Optional[str]


@dataclass
class ListPrefixResponse:
    bucket: str
    prefix: str
    objects: List[ListedObject]


@dataclass
class StoredDocumentOCRRequest:
    bucket: Optional[str]
    key: str
    document_language: Optional[str] = None


@dataclass
class StoredDocumentOCRResponse:
    bucket: str
    key: str
    text: str
    page_count: int
    provider: str


@dataclass
class StoredTextTranslateRequest:
    source_language: Optional[str]
    target_language: str
    text: str


@dataclass
class StoredTextTranslateResponse:
    source_language: Optional[str]
    target_language: str
    translated_text: str
    provider: str


@dataclass
class StoredAssetSummaryRequest:
    asset_text: str
    asset_title: Optional[str] = None
    max_sentences: int = 5


@dataclass
class StoredAssetSummaryResponse:
    asset_title: Optional[str]
    summary: str
    provider: str


@dataclass
class AssetMetadataEmbeddingRequest:
    bucket: Optional[str]
    key: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    extracted_text: str = ""


@dataclass
class AssetMetadataEmbeddingResponse:
    bucket: str
    key: str
    vector: List[float]
    dimensions: int
    provider: str
