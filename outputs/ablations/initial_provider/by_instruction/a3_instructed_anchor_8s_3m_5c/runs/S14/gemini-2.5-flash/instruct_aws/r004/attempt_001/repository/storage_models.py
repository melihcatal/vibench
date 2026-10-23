import dataclasses
from typing import Literal, Optional

@dataclasses.dataclass
class UploadObjectRequest:
    bucket_name: str
    object_name: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None

@dataclasses.dataclass
class UploadObjectResponse:
    object_name: str
    e_tag: str
    version_id: Optional[str] = None

@dataclasses.dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expires_in: int = 3600  # Seconds

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
    last_modified: str
    size: int
    content_type: str
    e_tag: str
    metadata: dict

@dataclasses.dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str
    delimiter: Optional[str] = None
    max_keys: Optional[int] = None

@dataclasses.dataclass
class ListPrefixItem:
    key: str
    last_modified: str
    size: int
    e_tag: str

@dataclasses.dataclass
class ListPrefixResponse:
    items: list[ListPrefixItem]
    common_prefixes: list[str] = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class StoredDocumentOcrRequest:
    bucket_name: str
    object_name: str
    document_format: Literal['PDF', 'PNG', 'JPEG']

@dataclasses.dataclass
class StoredDocumentOcrResponse:
    text_content: str
    detected_languages: list[str]

@dataclasses.dataclass
class StoredTextTranslateRequest:
    text: str
    source_language: str
    target_language: str

@dataclasses.dataclass
class StoredTextTranslateResponse:
    translated_text: str
    source_language: str
    target_language: str

@dataclasses.dataclass
class StoredAssetSummaryRequest:
    bucket_name: str
    object_name: str
    summary_length: Literal['short', 'medium', 'long'] = 'medium'

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
    embedding: list[float]
