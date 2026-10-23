import dataclasses
from typing import Optional, Dict, Any, Union


@dataclasses.dataclass
class UploadObjectRequest:
    bucket_name: str
    object_name: str
    file_path: Optional[str] = None
    data: Optional[Union[bytes, str]] = None
    metadata: Optional[Dict[str, str]] = None


@dataclasses.dataclass
class UploadObjectResponse:
    success: bool
    message: str
    etag: Optional[str] = None


@dataclasses.dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expiration_seconds: int = 3600


@dataclasses.dataclass
class PresignedDownloadResponse:
    success: bool
    message: str
    url: Optional[str] = None


@dataclasses.dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_name: str


@dataclasses.dataclass
class ObjectMetadataResponse:
    success: bool
    message: str
    metadata: Optional[Dict[str, Any]] = None


@dataclasses.dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str
    max_keys: int = 1000


@dataclasses.dataclass
class ListPrefixResponse:
    success: bool
    message: str
    objects: Optional[list[Dict[str, Any]]] = None


@dataclasses.dataclass
class OCRDocumentRequest:
    bucket_name: str
    object_name: str


@dataclasses.dataclass
class OCRDocumentResponse:
    success: bool
    message: str
    text_content: Optional[str] = None
    raw_response: Optional[Dict[str, Any]] = None


@dataclasses.dataclass
class TranslateTextRequest:
    text: str
    source_language_code: str
    target_language_code: str


@dataclasses.dataclass
class TranslateTextResponse:
    success: bool
    message: str
    translated_text: Optional[str] = None


@dataclasses.dataclass
class SummarizeContentRequest:
    text_content: str
    max_tokens: int = 512
    temperature: float = 0.5


@dataclasses.dataclass
class SummarizeContentResponse:
    success: bool
    message: str
    summary: Optional[str] = None


@dataclasses.dataclass
class EmbedMetadataRequest:
    text: str


@dataclasses.dataclass
class EmbedMetadataResponse:
    success: bool
    message: str
    embedding: Optional[list[float]] = None
