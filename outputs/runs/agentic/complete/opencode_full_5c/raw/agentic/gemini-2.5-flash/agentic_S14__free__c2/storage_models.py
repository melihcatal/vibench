from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class UploadObjectRequest:
    bucket_name: str
    object_key: str
    file_content: bytes
    content_type: Optional[str] = None


@dataclass
class UploadObjectResponse:
    e_tag: str
    version_id: Optional[str] = None


@dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_key: str
    expiration_seconds: int = 3600


@dataclass
class PresignedDownloadResponse:
    presigned_url: str


@dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_key: str


@dataclass
class ObjectMetadataResponse:
    content_type: Optional[str] = None
    content_length: Optional[int] = None
    last_modified: Optional[str] = None
    e_tag: Optional(str) = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str
    max_keys: int = 1000


@dataclass
class ListedObject:
    key: str
    last_modified: str
    e_tag: str
    size: int


@dataclass
class ListPrefixResponse:
    objects: List[ListedObject]


@dataclass
class StoredDocumentOcrRequest:
    bucket_name: str
    object_key: str


@dataclass
class StoredDocumentOcrResponse:
    detected_text: str


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
    text_content: str
    max_tokens: int = 200


@dataclass
class StoredAssetSummaryResponse:
    summary: str


@dataclass
class AssetMetadataEmbeddingRequest:
    text: str


@dataclass
class AssetMetadataEmbeddingResponse:
    embedding: List[float]
