from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

@dataclass
class UploadObjectRequest:
    bucket_name: str
    object_name: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None

@dataclass
class UploadObjectResponse:
    bucket_name: str
    object_name: str
    public_url: str

@dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expiry_seconds: Optional[int] = None

@dataclass
class PresignedDownloadResponse:
    bucket_name: str
    object_name: str
    signed_url: str

@dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_name: str

@dataclass
class ObjectMetadataResponse:
    bucket_name: str
    object_name: str
    size: Optional[int] = None
    content_type: Optional[str] = None
    updated: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: Optional[str] = None
    delimiter: Optional[str] = None

@dataclass
class ObjectSummary:
    name: str
    size: Optional[int] = None
    updated: Optional[str] = None

@dataclass
class ListPrefixResponse:
    bucket_name: str
    prefix: Optional[str] = None
    objects: List[ObjectSummary] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)

@dataclass
class StoredDocumentOcrRequest:
    bucket_name: str
    object_name: str
    mime_type: str

@dataclass
class StoredDocumentOcrResponse:
    bucket_name: str
    object_name: str
    extracted_text: str
    pages: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class StoredTextTranslateRequest:
    text: str
    source_language_code: Optional[str] = None
    target_language_code: str

@dataclass
class StoredTextTranslateResponse:
    original_text: str
    translated_text: str
    source_language_code: Optional[str] = None
    target_language_code: str

@dataclass
class StoredAssetSummaryRequest:
    text_content: str
    max_output_tokens: Optional[int] = 200

@dataclass
class StoredAssetSummaryResponse:
    original_content: str
    summary: str

@dataclass
class AssetMetadataEmbeddingRequest:
    text_content: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AssetMetadataEmbeddingResponse:
    text_content: str
    embedding: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)
