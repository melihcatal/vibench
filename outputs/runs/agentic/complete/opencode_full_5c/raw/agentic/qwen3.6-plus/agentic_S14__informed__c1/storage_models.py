from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, List, Any, BinaryIO


@dataclass
class UploadRequest:
    bucket: str
    key: str
    data: Optional[bytes] = None
    file_path: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    storage_class: str = "STANDARD"
    tags: Optional[Dict[str, str]] = None


@dataclass
class UploadResponse:
    success: bool
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    content_length: int = 0
    error: Optional[str] = None


@dataclass
class PresignedUrlRequest:
    bucket: str
    key: str
    expires_in: int = 3600
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
class ObjectMetadata:
    bucket: str
    key: str
    content_type: Optional[str] = None
    content_length: int = 0
    etag: Optional[str] = None
    last_modified: Optional[datetime] = None
    storage_class: Optional[str] = None
    version_id: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    delete_marker: bool = False


@dataclass
class ListPrefixRequest:
    bucket: str
    prefix: str = ""
    delimiter: str = ""
    max_keys: int = 1000
    start_after: Optional[str] = None
    continuation_token: Optional[str] = None


@dataclass
class ObjectSummary:
    key: str
    size: int = 0
    etag: Optional[str] = None
    last_modified: Optional[datetime] = None
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
    error: Optional[str] = None


@dataclass
class OcrRequest:
    bucket: str
    key: str
    version_id: Optional[str] = None
    pages: Optional[List[int]] = None


@dataclass
class OcrPage:
    page_number: int
    text: str
    confidence: float = 0.0
    blocks: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class OcrResponse:
    success: bool
    document_key: str
    pages: List[OcrPage] = field(default_factory=list)
    full_text: str = ""
    average_confidence: float = 0.0
    error: Optional[str] = None


@dataclass
class TranslateRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str = "en"
    terminology_names: Optional[List[str]] = None


@dataclass
class TranslateResponse:
    success: bool
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    error: Optional[str] = None


@dataclass
class SummaryRequest:
    text: str
    max_tokens: int = 500
    temperature: float = 0.3
    summary_type: str = "concise"


@dataclass
class SummaryResponse:
    success: bool
    summary: str = ""
    model_id: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    error: Optional[str] = None


@dataclass
class EmbeddingRequest:
    text: str
    model_id: str = "amazon.titan-embed-text-v2:0"


@dataclass
class EmbeddingResponse:
    success: bool
    embedding: List[float] = field(default_factory=list)
    model_id: str = ""
    input_tokens: int = 0
    error: Optional[str] = None


@dataclass
class AssetEmbeddingRecord:
    object_key: str
    bucket: str
    metadata: Dict[str, str] = field(default_factory=dict)
    extracted_text: str = ""
    embedding: List[float] = field(default_factory=list)
    embedding_model: str = ""
    created_at: Optional[datetime] = None
