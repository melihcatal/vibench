import dataclasses
from typing import Optional, Dict, Any

@dataclasses.dataclass
class UploadObjectRequest:
    bucket_name: str
    object_name: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    metadata: Optional[Dict[str, str]] = None

@dataclasses.dataclass
class UploadObjectResponse:
    e_tag: str
    version_id: Optional[str] = None
    
@dataclasses.dataclass
class PresignedDownloadRequest:
    bucket_name: str
    object_name: str
    expires_in: int = 3600 # seconds

@dataclasses.dataclass
class PresignedDownloadResponse:
    url: str

@dataclasses.dataclass
class ObjectMetadataRequest:
    bucket_name: str
    object_name: str

@dataclasses.dataclass
class ObjectMetadataResponse:
    metadata: Dict[str, Any]

@dataclasses.dataclass
class ListPrefixRequest:
    bucket_name: str
    prefix: str
    max_keys: int = 1000

@dataclasses.dataclass
class ListPrefixResponse:
    object_names: list[str]
    
@dataclasses.dataclass
class StoredDocumentOcrRequest:
    bucket_name: str
    object_name: str

@dataclasses.dataclass
class StoredDocumentOcrResponse:
    extracted_text: str

@dataclasses.dataclass
class StoredTextTranslateRequest:
    text: str
    source_language: str
    target_language: str

@dataclasses.dataclass
class StoredTextTranslateResponse:
    translated_text: str

@dataclasses.dataclass
class StoredAssetSummaryRequest:
    text: str
    
@dataclasses.dataclass
class StoredAssetSummaryResponse:
    summary: str

@dataclasses.dataclass
class AssetMetadataEmbeddingRequest:
    metadata: Dict[str, Any]
    extracted_text: Optional[str] = None

@dataclasses.dataclass
class AssetMetadataEmbeddingResponse:
    embedding: list[float]
