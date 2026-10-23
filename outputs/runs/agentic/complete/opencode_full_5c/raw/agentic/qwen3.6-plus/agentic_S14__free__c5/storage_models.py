import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class StorageConfig:
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    bucket_name: str = ""
    endpoint_url: Optional[str] = None
    max_retries: int = 3
    connection_timeout: int = 30
    read_timeout: int = 60

    @classmethod
    def from_env(cls) -> "StorageConfig":
        return cls(
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", ""),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
            aws_region=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
            bucket_name=os.environ.get("STORAGE_BUCKET_NAME", ""),
            endpoint_url=os.environ.get("STORAGE_ENDPOINT_URL") or None,
            max_retries=int(os.environ.get("STORAGE_MAX_RETRIES", "3")),
            connection_timeout=int(os.environ.get("STORAGE_CONNECT_TIMEOUT", "30")),
            read_timeout=int(os.environ.get("STORAGE_READ_TIMEOUT", "60")),
        )


@dataclass
class UploadRequest:
    bucket: str
    key: str
    content_type: str = "application/octet-stream"
    metadata: dict = field(default_factory=dict)
    storage_class: str = "STANDARD"
    acl: Optional[str] = None


@dataclass
class UploadResponse:
    success: bool
    key: str
    bucket: str
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


@dataclass
class PresignedUrlResponse:
    success: bool
    url: str = ""
    expires_at: Optional[datetime] = None
    error: Optional[str] = None


@dataclass
class MetadataRequest:
    bucket: str
    key: str
    version_id: Optional[str] = None


@dataclass
class ObjectMetadata:
    key: str
    bucket: str
    content_type: str = ""
    content_length: int = 0
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    version_id: Optional[str] = None
    storage_class: str = ""
    metadata: dict = field(default_factory=dict)
    exists: bool = True


@dataclass
class ListRequest:
    bucket: str
    prefix: str = ""
    delimiter: str = ""
    max_keys: int = 1000
    start_after: Optional[str] = None


@dataclass
class ListObjectItem:
    key: str
    size: int = 0
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    storage_class: str = ""


@dataclass
class ListResponse:
    success: bool
    objects: list = field(default_factory=list)
    common_prefixes: list = field(default_factory=list)
    is_truncated: bool = False
    next_continuation_token: Optional[str] = None
    key_count: int = 0
    error: Optional[str] = None


@dataclass
class OcrRequest:
    bucket: str
    key: str
    version_id: Optional[str] = None
    detect_tables: bool = True
    detect_forms: bool = False
    pages: Optional[list] = None


@dataclass
class OcrResponse:
    success: bool
    text: str = ""
    pages: list = field(default_factory=list)
    tables: list = field(default_factory=list)
    confidence: float = 0.0
    error: Optional[str] = None


@dataclass
class TranslateRequest:
    text: str
    source_language: str = "en"
    target_language: str = "es"
    terminology_name: Optional[str] = None


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
    max_length: int = 300
    min_length: int = 50
    model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"


@dataclass
class SummaryResponse:
    success: bool
    summary: str = ""
    model_id: str = ""
    token_count: int = 0
    error: Optional[str] = None


@dataclass
class EmbeddingRequest:
    text: str
    model_id: str = "amazon.titan-embed-text-v2:0"
    dimensions: int = 1024
    normalize: bool = True


@dataclass
class EmbeddingResponse:
    success: bool
    embedding: list = field(default_factory=list)
    model_id: str = ""
    input_token_count: int = 0
    error: Optional[str] = None


@dataclass
class AssetMetadataEmbedRequest:
    bucket: str
    key: str
    extracted_text: str = ""
    model_id: str = "amazon.titan-embed-text-v2:0"
    include_metadata_fields: list = field(
        default_factory=lambda: [
            "content_type",
            "content_length",
            "last_modified",
            "storage_class",
        ]
    )


@dataclass
class AssetMetadataEmbedResponse:
    success: bool
    combined_embedding: list = field(default_factory=list)
    metadata_embedding: list = field(default_factory=list)
    text_embedding: list = field(default_factory=list)
    object_metadata: Optional[ObjectMetadata] = None
    model_id: str = ""
    error: Optional[str] = None
