import dataclasses
from typing import Optional, Dict, List, Union


@dataclasses.dataclass
class UploadObjectRequest:
    bucket_name: str
    object_name: str
    data: Union[bytes, str]
    content_type: Optional[str] = None


@dataclasses.dataclass
class UploadObjectResponse:
    object_name: str
    bucket_name: str
    size: int
    media_link: str


@dataclasses.dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expiration_seconds: int = 3600


@dataclasses.dataclass
class PresignedDownloadResponse:
    url: str


@dataclasses.dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_name: str


@dataclasses.dataclass
class ObjectMetadataResponse:
    object_name: str
    bucket_name: str
    size: int
    content_type: Optional[str]
    etag: str
    metadata: Dict[str, str]


@dataclasses.dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str
    max_results: Optional[int] = None


@dataclasses.dataclass
class ListedObject:
    object_name: str
    size: int
    updated: str


@dataclasses.dataclass
class ListPrefixResponse:
    objects: List[ListedObject]


@dataclasses.dataclass
class StoredDocumentOcrRequest:
    bucket_name: str
    object_name: str
    project_id: str
    location: str
    processor_id: str


@dataclasses.dataclass
class OcrResult:
    text: str
    pages: int


@dataclasses.dataclass
class StoredDocumentOcrResponse:
    object_name: str
    ocr_result: OcrResult


@dataclasses.dataclass
class StoredTextTranslateRequest:
    text: str
    target_language_code: str
    project_id: str
    location: str
    source_language_code: Optional[str] = None


@dataclasses.dataclass
class StoredTextTranslateResponse:
    translated_text: str
    source_language_code: str


@dataclasses.dataclass
class StoredAssetSummaryRequest:
    text_content: str
    model_name: str = "gemini-pro"


@dataclasses.dataclass
class StoredAssetSummaryResponse:
    summary: str


@dataclasses.dataclass
class AssetMetadataEmbeddingRequest:
    text_content: str
    model_name: str = "embedding-001"


@dataclasses.dataclass
class AssetMetadataEmbeddingResponse:
    embedding: List[float]
