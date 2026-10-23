from typing import Dict, Any, List, Optional
from datetime import datetime

class ObjectUploadRequest:
    def __init__(self, bucket_name: str, object_key: str, file_path: Optional[str] = None, data_bytes: Optional[bytes] = None):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.file_path = file_path
        self.data_bytes = data_bytes

class ObjectUploadResponse:
    def __init__(self, etag: str, version_id: Optional[str] = None):
        self.etag = etag
        self.version_id = version_id

class PresignedDownloadRequest:
    def __init__(self, bucket_name: str, object_key: str, expires_in_seconds: int = 3600):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.expires_in_seconds = expires_in_seconds

class PresignedDownloadResponse:
    def __init__(self, url: str):
        self.url = url

class ObjectMetadataRequest:
    def __init__(self, bucket_name: str, object_key: str):
        self.bucket_name = bucket_name
        self.object_key = object_key

class ObjectMetadataResponse:
    def __init__(self, content_type: str, content_length: int, last_modified: datetime, etag: str, custom_metadata: Dict[str, str]):
        self.content_type = content_type
        self.content_length = content_length
        self.last_modified = last_modified
        self.etag = etag
        self.custom_metadata = custom_metadata

class ListPrefixRequest:
    def __init__(self, bucket_name: str, prefix: str = "", max_keys: int = 1000):
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.max_keys = max_keys

class ListPrefixResponse:
    def __init__(self, object_keys: List[str]):
        self.object_keys = object_keys

class OCRDocumentRequest:
    def __init__(self, bucket_name: str, object_key: str):
        self.bucket_name = bucket_name
        self.object_key = object_key

class OCRDocumentResponse:
    def __init__(self, extracted_text: str, detected_languages: List[str]):
        self.extracted_text = extracted_text
        self.detected_languages = detected_languages

class TranslateTextRequest:
    def __init__(self, text: str, source_language_code: str, target_language_code: str):
        self.text = text
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code

class TranslateTextResponse:
    def __init__(self, translated_text: str, source_language_code: str, target_language_code: str):
        self.translated_text = translated_text
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code

class SummarizeAssetRequest:
    def __init__(self, text_content: str, max_tokens: int = 200):
        self.text_content = text_content
        self.max_tokens = max_tokens

class SummarizeAssetResponse:
    def __init__(self, summary: str):
        self.summary = summary

class EmbeddingsRequest:
    def __init__(self, text_to_embed: List[str]):
        self.text_to_embed = text_to_embed

class EmbeddingsResponse:
    def __init__(self, embeddings: List[List[float]]):
        self.embeddings = embeddings
