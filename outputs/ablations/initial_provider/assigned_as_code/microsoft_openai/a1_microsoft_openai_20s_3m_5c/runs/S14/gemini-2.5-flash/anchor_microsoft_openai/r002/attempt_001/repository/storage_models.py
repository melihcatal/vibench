from typing import Optional, Dict, Any

class UploadObjectRequest:
    object_name: str
    data: bytes
    content_type: Optional[str] = None

class PresignedDownloadRequest:
    object_name: str
    expiry_minutes: int = 60

class ObjectMetadataRequest:
    object_name: str

class ListPrefixRequest:
    prefix: Optional[str] = None
    max_results: Optional[int] = None

class StoredDocumentOcrRequest:
    object_name: str

class StoredTextTranslateRequest:
    text_content: str
    target_language: str
    source_language: Optional[str] = None

class StoredAssetSummaryRequest:
    text_content: str

class AssetMetadataEmbeddingRequest:
    object_name: str
    extracted_text: Optional[str] = None
