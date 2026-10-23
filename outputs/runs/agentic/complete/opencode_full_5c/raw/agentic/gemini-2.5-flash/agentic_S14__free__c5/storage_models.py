from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, List, Any

# --- S3 Related Models ---


@dataclass
class UploadObjectRequest:
    bucket_name: str
    object_key: str
    data: bytes  # File content as bytes
    content_type: str = "application/octet-stream"


@dataclass
class UploadObjectResponse:
    success: bool
    message: str


@dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_key: str
    expires_in_seconds: int = 3600  # Default to 1 hour


@dataclass
class PresignedDownloadResponse:
    success: bool
    presigned_url: Optional[str]
    message: str


@dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_key: str


@dataclass
class ObjectMetadataResponse:
    success: bool
    metadata: Optional[Dict[str, Any]]  # Dictionary to hold metadata
    message: str


@dataclass
class ObjectInfo:
    key: str
    last_modified: datetime
    size: int
    etag: str


@dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str = ""  # List all if empty


@dataclass
class ListPrefixResponse:
    success: bool
    objects: List[ObjectInfo]
    message: str


# --- Later-Step Integration Models ---


@dataclass
class OcrRequest:
    bucket_name: str
    object_key: str


@dataclass
class OcrResponse:
    success: bool
    extracted_text: Optional[str]
    message: str


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None  # Auto-detect if not provided


@dataclass
class TranslationResponse:
    success: bool
    translated_text: Optional[str]
    message: str


@dataclass
class SummarizationRequest:
    text: str
    # Add optional parameters like desired_length, format, etc. if needed
    # For now, keep it simple


@dataclass
class SummarizationResponse:
    success: bool
    summary: Optional[str]
    message: str


@dataclass
class EmbeddingRequest:
    text_to_embed: str
    # Add optional parameters like model_name, task_type if needed
    # For now, keep it simple


@dataclass
class EmbeddingResponse:
    success: bool
    embedding: Optional[List[float]]
    message: str
