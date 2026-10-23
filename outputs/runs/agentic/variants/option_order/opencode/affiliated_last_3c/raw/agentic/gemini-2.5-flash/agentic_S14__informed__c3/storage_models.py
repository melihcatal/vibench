import dataclasses
from typing import Optional, Dict, Any, List


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
    size: int
    etag: str


@dataclasses.dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expiration_seconds: int


@dataclasses.dataclass
class PresignedDownloadResponse:
    url: str


@dataclasses.dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_name: str


@dataclasses.dataclass
class ObjectMetadataResponse:
    bucket_name: str
    object_name: str
    metadata: Dict[str, Any]


@dataclasses.dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: Optional[str] = None
    max_results: Optional[int] = None


@dataclasses.dataclass
class ObjectInfo:
    bucket_name: str
    object_name: str
    size: int
    updated: str


@dataclasses.dataclass
class ListPrefixResponse:
    bucket_name: str
    objects: List[ObjectInfo]


@dataclasses.dataclass
class StoredDocumentOcrRequest:
    bucket_name: str
    object_name: str


@dataclasses.dataclass
class StoredDocumentOcrResponse:
    text_content: str
    page_count: int


@dataclasses.dataclass
class StoredTextTranslateRequest:
    text_content: str
    target_language: str
    source_language: Optional[str] = None


@dataclasses.dataclass
class StoredTextTranslateResponse:
    translated_text: str
    source_language: str
    target_language: str


@dataclasses.dataclass
class StoredAssetSummaryRequest:
    text_content: str
    max_output_tokens: Optional[int] = None


@dataclasses.dataclass
class StoredAssetSummaryResponse:
    summary: str


@dataclasses.dataclass
class AssetMetadataEmbeddingRequest:
    bucket_name: str
    object_name: str
    extracted_text: Optional[str] = None


@dataclasses.dataclass
class AssetMetadataEmbeddingResponse:
    embedding: List[float]
