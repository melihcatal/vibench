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
    media_link: str


@dataclasses.dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expiration_seconds: int = 3600


@dataclasses.dataclass
class PresignedDownloadResponse:
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
    content_type: str
    etag: str
    metadata: Dict[str, str]


@dataclasses.dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: Optional[str] = None
    max_results: Optional[int] = None


@dataclasses.dataclass
class ListPrefixResponse:
    objects: List[Dict[str, Any]]


@dataclasses.dataclass
class StoredDocumentOcrRequest:
    project_id: str
    location: str
    processor_id: str
    gcs_input_uri: str


@dataclasses.dataclass
class StoredDocumentOcrResponse:
    text_content: str
    document_json: Dict[str, Any]


@dataclasses.dataclass
class StoredTextTranslateRequest:
    project_id: str
    location: str
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None


@dataclasses.dataclass
class StoredTextTranslateResponse:
    translated_text: str
    detected_language_code: Optional[str] = None


@dataclasses.dataclass
class StoredAssetSummaryRequest:
    text_content: str
    max_output_tokens: int = 200


@dataclasses.dataclass
class StoredAssetSummaryResponse:
    summary: str


@dataclasses.dataclass
class AssetMetadataEmbeddingRequest:
    text_to_embed: str


@dataclasses.dataclass
class AssetMetadataEmbeddingResponse:
    embedding: List[float]
