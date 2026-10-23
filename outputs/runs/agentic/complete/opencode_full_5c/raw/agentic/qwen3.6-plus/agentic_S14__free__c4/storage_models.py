import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional, Dict, List, Any
from enum import Enum


class StorageClass(str, Enum):
    STANDARD = "STANDARD"
    STANDARD_IA = "STANDARD_IA"
    GLACIER = "GLACIER"
    DEEP_ARCHIVE = "DEEP_ARCHIVE"
    INTELLIGENT_TIERING = "INTELLIGENT_TIERING"


class ObjectCannedACL(str, Enum):
    PRIVATE = "private"
    PUBLIC_READ = "public-read"
    PUBLIC_READ_WRITE = "public-read-write"
    AUTHENTICATED_READ = "authenticated-read"


@dataclass
class UploadRequest:
    bucket: str
    key: str
    body: Optional[bytes] = None
    file_path: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = field(default_factory=dict)
    storage_class: StorageClass = StorageClass.STANDARD
    acl: Optional[ObjectCannedACL] = None
    tags: Optional[Dict[str, str]] = field(default_factory=dict)
    server_side_encryption: Optional[str] = None


@dataclass
class UploadResponse:
    success: bool
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    storage_class: Optional[str] = None
    content_length: int = 0
    error_message: Optional[str] = None


@dataclass
class PresignedURLRequest:
    bucket: str
    key: str
    expiration_seconds: int = 3600
    http_method: str = "GET"
    response_content_disposition: Optional[str] = None
    response_content_type: Optional[str] = None


@dataclass
class PresignedURLResponse:
    success: bool
    url: Optional[str] = None
    expires_at: Optional[datetime] = None
    error_message: Optional[str] = None


@dataclass
class MetadataRequest:
    bucket: str
    key: str
    version_id: Optional[str] = None


@dataclass
class MetadataResponse:
    success: bool
    bucket: str
    key: str
    content_type: Optional[str] = None
    content_length: int = 0
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    version_id: Optional[str] = None
    server_side_encryption: Optional[str] = None
    error_message: Optional[str] = None


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
    size: int
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None
    owner: Optional[str] = None


@dataclass
class ListPrefixResponse:
    success: bool
    bucket: str
    prefix: str
    objects: List[ObjectSummary] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None
    key_count: int = 0
    error_message: Optional[str] = None


@dataclass
class OCRRequest:
    bucket: str
    key: str
    version_id: Optional[str] = None
    detect_tables: bool = True
    detect_forms: bool = False
    region: Optional[str] = None


@dataclass
class OCRPage:
    page_number: int
    text: str
    confidence: float
    blocks: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class OCRResponse:
    success: bool
    document_key: str
    pages: List[OCRPage] = field(default_factory=list)
    full_text: str = ""
    tables: List[List[List[str]]] = field(default_factory=list)
    job_id: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class TranslateRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str = "en"
    region: Optional[str] = None


@dataclass
class TranslateResponse:
    success: bool
    translated_text: str = ""
    source_language: Optional[str] = None
    target_language: str = "en"
    confidence: Optional[float] = None
    error_message: Optional[str] = None


@dataclass
class SummaryRequest:
    text: str
    max_tokens: int = 500
    temperature: float = 0.3
    focus: Optional[str] = None
    model: str = "gpt-4o"


@dataclass
class SummaryResponse:
    success: bool
    summary: str = ""
    model_used: str = ""
    tokens_used: Optional[int] = None
    error_message: Optional[str] = None


@dataclass
class EmbeddingRequest:
    text: str
    metadata: Optional[Dict[str, str]] = None
    model: str = "text-embedding-3-small"
    dimensions: Optional[int] = None


@dataclass
class EmbeddingResponse:
    success: bool
    embedding: List[float] = field(default_factory=list)
    model_used: str = ""
    dimensions: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None


def normalize_metadata_keys(metadata: Dict[str, str]) -> Dict[str, str]:
    return {
        k.lower().replace(" ", "_").replace("-", "_"): str(v)
        for k, v in metadata.items()
    }


def format_datetime_iso(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


def parse_datetime_iso(dt_str: Optional[str]) -> Optional[datetime]:
    if dt_str is None:
        return None
    try:
        return datetime.fromisoformat(dt_str)
    except (ValueError, TypeError):
        return None


def response_to_dict(response_obj) -> Dict[str, Any]:
    result = asdict(response_obj)
    for key, value in result.items():
        if isinstance(value, datetime):
            result[key] = format_datetime_iso(value)
    return result
