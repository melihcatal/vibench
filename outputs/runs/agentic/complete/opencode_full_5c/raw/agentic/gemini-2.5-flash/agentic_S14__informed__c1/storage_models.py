from typing import Literal, Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class UploadObjectRequest:
    bucket_name: str
    object_name: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: Optional[str] = None


@dataclass
class UploadObjectResponse:
    e_tag: str
    version_id: Optional[str] = None


@dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expiration: int = 3600  # Seconds


@dataclass
class PresignedDownloadResponse:
    url: str


@dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_name: str


@dataclass
class ObjectMetadataResponse:
    metadata: Dict[str, Any]
    content_type: Optional[str] = None
    content_length: Optional[int] = None


@dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str
    max_keys: int = 1000


@dataclass
class ListPrefixResponse:
    objects: list[Dict[str, Any]]
    common_prefixes: list[str]


@dataclass
class StoredDocumentOcrRequest:
    bucket_name: str
    object_name: str


@dataclass
class StoredDocumentOcrResponse:
    text_extracted: str
    # raw_response: Dict[str, Any] # Consider adding raw response for more detail if needed


@dataclass
class StoredTextTranslateRequest:
    text: str
    source_language_code: str
    target_language_code: str


@dataclass
class StoredTextTranslateResponse:
    translated_text: str
    source_language_code: str
    target_language_code: str


@dataclass
class StoredAssetSummaryRequest:
    text: str
    max_tokens: int = 200
    model_id: str = "anthropic.claude-v2"


@dataclass
class StoredAssetSummaryResponse:
    summary: str


@dataclass
class AssetMetadataEmbeddingRequest:
    text: str
    model_id: str = "amazon.titan-embed-text-v1"


@dataclass
class AssetMetadataEmbeddingResponse:
    embedding: list[float]
