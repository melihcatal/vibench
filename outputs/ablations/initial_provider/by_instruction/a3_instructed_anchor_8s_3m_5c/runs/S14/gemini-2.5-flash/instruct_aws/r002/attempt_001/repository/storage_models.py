import dataclasses
from typing import Dict, Any, Optional

@dataclasses.dataclass
class UploadObjectRequest:
    bucket_name: str
    object_key: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: Optional[str] = None

@dataclasses.dataclass
class UploadObjectResponse:
    object_key: str
    e_tag: str
    version_id: Optional[str] = None
    upload_success: bool

@dataclasses.dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_key: str
    expiration_seconds: int = 3600

@dataclasses.dataclass
class PresignedDownloadResponse:
    presigned_url: str

@dataclasses.dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_key: str

@dataclasses.dataclass
class ObjectMetadataResponse:
    object_key: str
    metadata: Dict[str, Any]

@dataclasses.dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str
    max_keys: int = 1000

@dataclasses.dataclass
class ListPrefixResponse:
    prefix: str
    object_keys: list[str]
    common_prefixes: list[str]

@dataclasses.dataclass
class StoredDocumentOcrRequest:
    bucket_name: str
    object_key: str

@dataclasses.dataclass
class StoredDocumentOcrResponse:
    object_key: str
    extracted_text: str
    job_id: Optional[str] = None

@dataclasses.dataclass
class StoredTextTranslateRequest:
    text: str
    source_language_code: str
    target_language_code: str

@dataclasses.dataclass
class StoredTextTranslateResponse:
    translated_text: str
    source_language_code: str
    target_language_code: str

@dataclasses.dataclass
class StoredAssetSummaryRequest:
    text: str
    language_code: str = "en"
    min_length: int = 20
    max_length: int = 100

@dataclasses.dataclass
class StoredAssetSummaryResponse:
    summary: str

@dataclasses.dataclass
class AssetMetadataEmbeddingRequest:
    text_content: str
    metadata: Dict[str, str]

@dataclasses.dataclass
class AssetMetadataEmbeddingResponse:
    embedding: list[float]
    combined_text: str
