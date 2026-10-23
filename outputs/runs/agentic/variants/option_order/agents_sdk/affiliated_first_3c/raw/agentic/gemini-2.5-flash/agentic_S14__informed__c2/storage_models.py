
from typing import Optional, Dict, Any

class ObjectStorageUploadRequest:
    def __init__(self, bucket_name: str, object_key: str, data: bytes, content_type: Optional[str] = None):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.data = data
        self.content_type = content_type

class ObjectStorageUploadResponse:
    def __init__(self, e_tag: str, version_id: Optional[str] = None):
        self.e_tag = e_tag
        self.version_id = version_id

class ObjectMetadataRequest:
    def __init__(self, bucket_name: str, object_key: str):
        self.bucket_name = bucket_name
        self.object_key = object_key

class ObjectMetadataResponse:
    def __init__(self, content_type: str, content_length: int, last_modified: str, etag: str, metadata: Dict[str, str]):
        self.content_type = content_type
        self.content_length = content_length
        self.last_modified = last_modified
        self.etag = etag
        self.metadata = metadata

class PresignedDownloadRequest:
    def __init__(self, bucket_name: str, object_key: str, expiration_seconds: int = 3600):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.expiration_seconds = expiration_seconds

class PresignedDownloadResponse:
    def __init__(self, url: str):
        self.url = url

class ListObjectsRequest:
    def __init__(self, bucket_name: str, prefix: Optional[str] = None, max_keys: Optional[int] = None):
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.max_keys = max_keys

class ListObjectsResponse:
    def __init__(self, object_keys: list[str], common_prefixes: list[str]):
        self.object_keys = object_keys
        self.common_prefixes = common_prefixes

class OCRDocumentRequest:
    def __init__(self, bucket_name: str, object_key: str):
        self.bucket_name = bucket_name
        self.object_key = object_key

class OCRDocumentResponse:
    def __init__(self, full_text: str, pages: list[str], raw_response: Dict[str, Any]):
        self.full_text = full_text
        self.pages = pages
        self.raw_response = raw_response

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

class SummarizeContentRequest:
    def __init__(self, text_content: str, max_tokens: int = 500):
        self.text_content = text_content
        self.max_tokens = max_tokens

class SummarizeContentResponse:
    def __init__(self, summary_text: str):
        self.summary_text = summary_text

class EmbedContentRequest:
    def __init__(self, content: str):
        self.content = content

class EmbedContentResponse:
    def __init__(self, embedding: list[float]):
        self.embedding = embedding
