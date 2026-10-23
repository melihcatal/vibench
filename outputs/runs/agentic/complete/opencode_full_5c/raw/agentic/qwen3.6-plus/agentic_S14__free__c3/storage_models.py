from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class UploadRequest:
    bucket: str
    key: str
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    tags: Optional[Dict[str, str]] = None
    storage_class: Optional[str] = None
    server_side_encryption: Optional[str] = None


@dataclass
class UploadResponse:
    success: bool
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    content_length: Optional[int] = None
    error: Optional[str] = None


@dataclass
class PresignedUrlRequest:
    bucket: str
    key: str
    expiry_seconds: int = 3600
    http_method: str = "GET"
    response_content_disposition: Optional[str] = None
    response_content_type: Optional[str] = None


@dataclass
class PresignedUrlResponse:
    success: bool
    url: Optional[str] = None
    expires_at: Optional[datetime] = None
    error: Optional[str] = None


@dataclass
class MetadataRequest:
    bucket: str
    key: str
    version_id: Optional[str] = None


@dataclass
class MetadataResponse:
    success: bool
    content_type: Optional[str] = None
    content_length: Optional[int] = None
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    version_id: Optional[str] = None
    error: Optional[str] = None


@dataclass
class ListPrefixRequest:
    bucket: str
    prefix: str = ""
    delimiter: Optional[str] = None
    max_keys: int = 1000
    start_after: Optional[str] = None


@dataclass
class ObjectSummary:
    key: str
    size: Optional[int] = None
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None
    is_common_prefix: bool = False


@dataclass
class ListPrefixResponse:
    success: bool
    objects: List[ObjectSummary] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None
    error: Optional[str] = None


@dataclass
class OcrRequest:
    bucket: str
    key: str
    version_id: Optional[str] = None


@dataclass
class OcrPage:
    page_number: int
    text: str
    blocks: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class OcrResponse:
    success: bool
    pages: List[OcrPage] = field(default_factory=list)
    full_text: str = ""
    error: Optional[str] = None


@dataclass
class TranslateRequest:
    text: str
    source_language: str = "auto"
    target_language: str = "en"


@dataclass
class TranslateResponse:
    success: bool
    translated_text: Optional[str] = None
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    error: Optional[str] = None


@dataclass
class SummaryRequest:
    text: str
    max_length: int = 500
    temperature: float = 0.3


@dataclass
class SummaryResponse:
    success: bool
    summary: Optional[str] = None
    model_id: Optional[str] = None
    error: Optional[str] = None


@dataclass
class EmbeddingRequest:
    text: str
    metadata: Optional[Dict[str, str]] = None
    object_key: Optional[str] = None


@dataclass
class EmbeddingResponse:
    success: bool
    embedding: Optional[List[float]] = None
    vector_count: int = 0
    model_id: Optional[str] = None
    error: Optional[str] = None


def normalize_s3_metadata(raw_metadata: Optional[Dict[str, str]]) -> Dict[str, str]:
    if not raw_metadata:
        return {}
    return {k.lower().replace("x-amz-meta-", ""): v for k, v in raw_metadata.items()}


def parse_s3_datetime(dt) -> Optional[datetime]:
    if dt is None:
        return None
    if isinstance(dt, datetime):
        return dt.replace(tzinfo=None) if dt.tzinfo else dt
    return None
