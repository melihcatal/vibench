import dataclasses
from typing import Optional, Dict, Any

@dataclasses.dataclass
class UploadObjectRequest:
    bucket_name: str
    object_name: str
    data: bytes
    content_type: Optional[str] = None

@dataclasses.dataclass
class UploadObjectResponse:
    bucket_name: str
    object_name: str
    uri: str

@dataclasses.dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expiration_seconds: int = 3600  # Default to 1 hour

@dataclasses.dataclass
class PresignedDownloadResponse:
    bucket_name: str
    object_name: str
    signed_url: str

@dataclasses.dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_name: str

@dataclasses.dataclass
class ObjectMetadataResponse:
    bucket_name: str
    object_name: str
    size: int
    content_type: Optional[str]
    etag: str
    updated_time: str
    metadata: Optional[Dict[str, Any]]

@dataclasses.dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str
    delimiter: Optional[str] = None

@dataclasses.dataclass
class ListPrefixResponse:
    bucket_name: str
    prefix: str
    objects: list[str]
    prefixes: list[str]

@dataclasses.dataclass
class StoredDocumentOcrRequest:
    bucket_name: str
    object_name: str

@dataclasses.dataclass
class StoredDocumentOcrResponse:
    bucket_name: str
    object_name: str
    full_text: str
    text_annotations: list[Dict[str, Any]]

@dataclasses.dataclass
class StoredTextTranslateRequest:
    project_id: str
    location: str # e.g., 'global' or 'us-central1'
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None

@dataclasses.dataclass
class StoredTextTranslateResponse:
    translated_text: str
    source_language_code: str

@dataclasses.dataclass
class StoredAssetSummaryRequest:
    project_id: str
    location: str # e.g., 'us-central1'
    text_content: str
    model_name: str = "gemini-pro"
    max_output_tokens: int = 1024
    temperature: float = 0.2

@dataclasses.dataclass
class StoredAssetSummaryResponse:
    summary: str

@dataclasses.dataclass
class AssetMetadataEmbeddingRequest:
    project_id: str
    location: str # e.g., 'us-central1'
    content: str
    model_name: str = "text-embedding-004"

@dataclasses.dataclass
class AssetMetadataEmbeddingResponse:
    embedding: list[float]
