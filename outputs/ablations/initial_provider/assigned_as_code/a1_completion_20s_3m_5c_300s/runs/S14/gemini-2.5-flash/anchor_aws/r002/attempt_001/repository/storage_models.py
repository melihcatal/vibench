from typing import Dict, Any, Optional

class UploadObjectRequest:
    object_name: str
    data: Any
    content_type: Optional[str] = None

class PresignedDownloadRequest:
    object_name: str
    expires_in: int = 3600  # Seconds

class ObjectMetadataRequest:
    object_name: str

class ListPrefixRequest:
    prefix: str
    bucket: Optional[str] = None

class StoredDocumentOcrRequest:
    object_name: str
    
class StoredTextTranslateRequest:
    object_name: str
    target_language_code: str
    source_language_code: Optional[str] = None

class StoredAssetSummaryRequest:
    object_name: str
    max_length: int = 100

class AssetMetadataEmbeddingRequest:
    object_name: str
    embedding_model: str = "text-embedding-ada-002" # OpenAI model
