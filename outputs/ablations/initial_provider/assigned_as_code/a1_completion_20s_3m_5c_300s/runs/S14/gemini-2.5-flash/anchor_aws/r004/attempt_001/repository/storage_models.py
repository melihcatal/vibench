from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class StorageConfig:
    region: str
    bucket: str


@dataclass
class UploadPayload:
    object_name: str
    data: Any
    content_type: Optional[str] = None


@dataclass
class DownloadRequest:
    object_name: str
    expires_in: int = 3600  # Seconds


@dataclass
class ObjectMetadataRequest:
    object_name: str


@dataclass
class ListObjectsRequest:
    prefix: str = ""
    max_keys: int = 1000


@dataclass
class OCRRequest:
    object_name: str


@dataclass
class TranslateRequest:
    text: str
    source_language_code: str
    target_language_code: str


@dataclass
class SummarizeRequest:
    text: str


@dataclass
class EmbedRequest:
    text: str
