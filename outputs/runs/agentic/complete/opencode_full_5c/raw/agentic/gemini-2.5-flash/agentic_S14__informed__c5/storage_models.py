from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class UploadObjectRequest:
    bucket_name: str
    object_name: str
    data: bytes
    content_type: Optional[str] = None


@dataclass
class UploadObjectResponse:
    bucket_name: str
    object_name: str
    size: int
    e_tag: str
    self_link: str


@dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expiration_seconds: int


@dataclass
class PresignedDownloadResponse:
    url: str


@dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_name: str


@dataclass
class ObjectMetadataResponse:
    bucket_name: str
    object_name: str
    size: int
    content_type: str
    e_tag: str
    last_modified: str
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str
    max_keys: Optional[int] = None


@dataclass
class ObjectSummary:
    object_name: str
    size: int
    last_modified: str


@dataclass
class ListPrefixResponse:
    bucket_name: str
    prefix: str
    objects: List[ObjectSummary]
    next_continuation_token: Optional[str] = None


@dataclass
class OcrDocumentRequest:
    bucket_name: str
    object_name: str


@dataclass
class OcrDocumentResponse:
    document_text: str
    pages: List[Dict[str, Any]]


@dataclass
class TranslateTextRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class TranslateTextResponse:
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class SummarizeAssetRequest:
    text_content: str
    max_output_tokens: int = 100


@dataclass
class SummarizeAssetResponse:
    summary: str


@dataclass
class EmbedMetadataRequest:
    metadata_fields: Dict[str, str]
    text_content: Optional[str] = None


@dataclass
class EmbedMetadataResponse:
    embedding: List[float]
