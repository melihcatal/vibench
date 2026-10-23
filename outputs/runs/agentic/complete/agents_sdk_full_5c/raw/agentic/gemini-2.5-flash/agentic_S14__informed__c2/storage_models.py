from dataclasses import dataclass
from typing import Optional, Dict, List, Union

@dataclass
class ObjectStorageUploadRequest:
    object_key: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: str = "application/octet-stream"

@dataclass
class ObjectStorageDownloadRequest:
    object_key: str
    expiration_seconds: int = 3600

@dataclass
class ObjectMetadataRequest:
    object_key: str

@dataclass
class ObjectMetadata:
    object_key: str
    size: int
    last_modified: str
    content_type: str
    etag: str
    metadata: Dict[str, str]

@dataclass
class ObjectListPrefixRequest:
    prefix: str
    max_keys: int = 100

@dataclass
class OCRRequest:
    bucket_name: str
    object_key: str

@dataclass
class TranslateRequest:
    text: str
    source_language_code: str
    target_language_code: str

@dataclass
class SummarizeRequest:
    text: str
    max_tokens: int = 500

@dataclass
class EmbeddingRequest:
    text: str
