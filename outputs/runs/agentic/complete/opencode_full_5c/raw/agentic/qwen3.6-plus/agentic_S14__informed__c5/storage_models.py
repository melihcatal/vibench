import os
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class ObjectUploadRequest:
    bucket: str
    object_name: str
    content: bytes
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class PresignedUrlRequest:
    bucket: str
    object_name: str
    expiration_minutes: int = 60


@dataclass
class ObjectMetadataResponse:
    object_name: str
    bucket: str
    size: int
    content_type: Optional[str]
    etag: Optional[str]
    storage_class: Optional[str]
    last_modified: Optional[datetime]
    metadata: Optional[Dict[str, str]] = None


@dataclass
class ListPrefixRequest:
    bucket: str
    prefix: str = ""
    delimiter: str = ""
    max_results: Optional[int] = None


@dataclass
class ObjectListingItem:
    name: str
    size: int
    content_type: Optional[str]
    last_modified: Optional[datetime]
    etag: Optional[str]


@dataclass
class ObjectListingResponse:
    objects: List[ObjectListingItem] = field(default_factory=list)
    prefixes: List[str] = field(default_factory=list)
    next_page_token: Optional[str] = None


@dataclass
class OCRRequest:
    file_content: bytes
    mime_type: str
    project_id: str
    processor_id: str
    location: str = "us"


@dataclass
class OCRResponse:
    text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None
    project_id: Optional[str] = None
    location: str = "global"


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: Optional[str] = None


@dataclass
class SummaryRequest:
    text: str
    model: str = "gemini-2.0-flash"
    max_tokens: int = 512
    temperature: float = 0.3


@dataclass
class SummaryResponse:
    summary: str
    model_used: str


@dataclass
class EmbeddingRequest:
    texts: List[str]
    model: str = "text-embedding-004"
    task_type: str = "RETRIEVAL_DOCUMENT"


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
    model_used: str
