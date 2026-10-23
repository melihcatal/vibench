import dataclasses

@dataclasses.dataclass
class UploadObjectRequest:
    container_name: str
    blob_name: str
    data: bytes
    content_type: str = "application/octet-stream"

@dataclasses.dataclass
class UploadObjectResponse:
    message: str
    url: str

@dataclasses.dataclass
class PresignedDownloadRequest:
    container_name: str
    blob_name: str
    expiry_minutes: int = 60

@dataclasses.dataclass
class PresignedDownloadResponse:
    url: str

@dataclasses.dataclass
class ObjectMetadataRequest:
    container_name: str
    blob_name: str

@dataclasses.dataclass
class ObjectMetadataResponse:
    name: str
    size: int
    content_settings: dict
    metadata: dict

@dataclasses.dataclass
class ListPrefixRequest:
    container_name: str
    prefix: str = ""

@dataclasses.dataclass
class ListPrefixResponse:
    blobs: list[str]

@dataclasses.dataclass
class StoredDocumentOcrRequest:
    container_name: str
    blob_name: str

@dataclasses.dataclass
class StoredDocumentOcrResponse:
    text: str

@dataclasses.dataclass
class StoredTextTranslateRequest:
    text: str
    target_language: str
    source_language: str = "en"

@dataclasses.dataclass
class StoredTextTranslateResponse:
    translated_text: str

@dataclasses.dataclass
class StoredAssetSummaryRequest:
    text: str
    summary_length: int = 100

@dataclasses.dataclass
class StoredAssetSummaryResponse:
    summary: str

@dataclasses.dataclass
class AssetMetadataEmbeddingRequest:
    text_content: str
    metadata: dict

@dataclasses.dataclass
class AssetMetadataEmbeddingResponse:
    embedding: list[float]
