from dataclasses import dataclass, field
from typing import Optional, BinaryIO, Dict, List, Any

@dataclass
class ObjectUploadRequest:
    bucket_name: str
    object_key: str
    data: BinaryIO | bytes

@dataclass
class ObjectUploadResponse:
    success: bool
    message: str

@dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_key: str
    expiration_seconds: int = 3600  # Default to 1 hour

@dataclass
class PresignedDownloadResponse:
    success: bool
    url: Optional[str]
    message: str

@dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_key: str

@dataclass
class ObjectMetadataResponse:
    success: bool
    object_key: Optional[str] = None
    bucket_name: Optional[str] = None
    size: Optional[int] = None
    content_type: Optional[str] = None
    last_modified: Optional[str] = None
    etag: Optional[str] = None
    user_metadata: Dict[str, str] = field(default_factory=dict)
    raw_metadata: Dict[str, Any] = field(default_factory=dict)
    message: str = ""

@dataclass
class ListedObject:
    key: Optional[str]
    last_modified: Optional[str] = None
    etag: Optional[str] = None
    size: Optional[int] = None
    storage_class: Optional[str] = None
    is_prefix: bool = False

@dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str = ""
    delimiter: str = ""
    max_keys: Optional[int] = None

@dataclass
class ListPrefixResponse:
    success: bool
    bucket_name: str
    prefix: str
    objects: List[ListedObject]
    message: str = ""

@dataclass
class OcrDocumentRequest:
    bucket_name: str
    object_key: str
    document_type: str # e.g., 'PDF', 'PNG', 'JPEG'

@dataclass
class OcrDocumentResponse:
    success: bool
    job_id: Optional[str] = None
    extracted_text: Optional[str] = None
    message: str = ""

@dataclass
class TranslateTextRequest:
    text: str
    source_language_code: str
    target_language_code: str

@dataclass
class TranslateTextResponse:
    success: bool
    translated_text: Optional[str] = None
    message: str = ""

@dataclass
class SummarizeTextRequest:
    text: str

@dataclass
class SummarizeTextResponse:
    success: bool
    summary: Optional[str] = None
    message: str = ""

@dataclass
class EmbedTextRequest:
    text: str

@dataclass
class EmbedTextResponse:
    success: bool
    embedding: Optional[List[float]] = None
    message: str = ""
