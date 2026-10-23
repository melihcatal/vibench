from dataclasses import dataclass
from typing import Any, Optional, BinaryIO


@dataclass
class ObjectMetadata:
    """Normalized metadata returned for an object"""

    bucket_name: str
    object_key: str
    size: int
    etag: str
    content_type: str
    last_modified: str


@dataclass
class UploadResponse:
    """Response when uploading an object"""

    bucket_name: str
    object_key: str
    etag: str


@dataclass
class DownloadResponse:
    """Response when downloading an object"""

    bucket_name: str
    object_key: str
    content: Optional[bytes]
    content_type: Optional[str]


@dataclass
class ListPrefixResponse:
    """Paginated list of objects under a prefix"""

    bucket_name: str
    prefix: str
    contents: list[ObjectMetadata]
    continuation_token: Optional[str]


@dataclass
class PresignedUrlResponse:
    """Presigned download URL"""

    url: str
    expires_at: int


@dataclass
class OCRDocument:
    """Result of OCR on a stored document"""

    text: str


@dataclass
class TranslatedText:
    """Translated version of extracted text"""

    translated: str


@dataclass
class AssetSummary:
    """Summarized content of a stored asset"""

    summary: str


@dataclass
class EmbeddingMetadata:
    """Metadata + extracted text to be embedded for search"""

    object_key: str
    metadata: dict[str, Any]
    text: Optional[str]
