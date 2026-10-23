from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime


@dataclass
class StorageObject:
    bucket_name: str
    key: str
    last_modified: Optional[datetime] = None
    size: Optional[int] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None


@dataclass
class UploadObjectRequest:
    bucket_name: str
    key: str
    data: Union[bytes, str]  # bytes for binary, str for file path
    content_type: Optional[str] = None


@dataclass
class UploadObjectResponse:
    bucket_name: str
    key: str
    version_id: Optional[str] = None
    etag: Optional[str] = None


@dataclass
class PresignedDownloadRequest:
    bucket_name: str
    key: str
    expiration_seconds: int = 3600  # 1 hour


@dataclass
class PresignedDownloadResponse:
    presigned_url: str


@dataclass
class ObjectMetadataRequest:
    bucket_name: str
    key: str


@dataclass
class ObjectMetadataResponse:
    bucket_name: str
    key: str
    metadata: Dict[str, Any]


@dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str
    max_keys: int = 1000


@dataclass
class ListPrefixResponse:
    bucket_name: str
    prefix: str
    objects: List[StorageObject]
    common_prefixes: List[str]


@dataclass
class OcrDocumentRequest:
    bucket_name: str
    key: str


@dataclass
class OcrDocumentResponse:
    job_id: Optional[str] = None
    document_text: Optional[str] = None
    pages: Optional[List[Dict[str, Any]]] = None


@dataclass
class TranslateTextRequest:
    text: str
    source_language_code: str
    target_language_code: str


@dataclass
class TranslateTextResponse:
    translated_text: str
    source_language_code: str
    target_language_code: str


@dataclass
class SummarizeContentRequest:
    content: str
    max_tokens: int = 200
    temperature: float = 0.5


@dataclass
class SummarizeContentResponse:
    summary: str


@dataclass
class EmbedMetadataRequest:
    text: str


@dataclass
class EmbedMetadataResponse:
    embedding: List[float]
