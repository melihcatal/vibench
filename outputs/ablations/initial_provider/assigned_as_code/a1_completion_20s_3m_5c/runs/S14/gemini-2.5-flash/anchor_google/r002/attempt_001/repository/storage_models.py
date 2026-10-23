import dataclasses
from typing import Optional

@dataclasses.dataclass
class StorageConfig:
    project_id: str
    bucket_name: str

@dataclasses.dataclass
class UploadObjectPayload:
    object_name: str
    data: bytes
    content_type: Optional[str] = "application/octet-stream"

@dataclasses.dataclass
class PresignedDownloadPayload:
    object_name: str
    expiration_seconds: int = 3600

@dataclasses.dataclass
class ObjectMetadataPayload:
    object_name: str

@dataclasses.dataclass
class ListPrefixPayload:
    prefix: str
    delimiter: Optional[str] = None

@dataclasses.dataclass
class StoredDocumentOcrPayload:
    object_name: str
    language_hints: Optional[list[str]] = None

@dataclasses.dataclass
class StoredTextTranslatePayload:
    text: str
    source_language_code: str
    target_language_code: str

@dataclasses.dataclass
class StoredAssetSummaryPayload:
    object_name: str
    max_output_tokens: Optional[int] = 1024

@dataclasses.dataclass
class AssetMetadataEmbeddingPayload:
    object_name: str
    text_content: Optional[str] = None
