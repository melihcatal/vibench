from typing import Dict, Any, Optional, List, Union
import io

class UploadObjectRequest:
    def __init__(self, object_key: str, data: Union[bytes, io.BytesIO], metadata: Optional[Dict[str, Any]] = None):
        self.object_key = object_key
        self.data = data
        self.metadata = metadata or {}

class UploadObjectResponse:
    def __init__(self, success: bool, object_key: Optional[str] = None, error_message: Optional[str] = None):
        self.success = success
        self.object_key = object_key
        self.error_message = error_message

class PresignedDownloadRequest:
    def __init__(self, object_key: str, expires_in_seconds: int = 3600):
        self.object_key = object_key
        self.expires_in_seconds = expires_in_seconds

class PresignedDownloadResponse:
    def __init__(self, success: bool, url: Optional[str] = None, object_key: Optional[str] = None, error_message: Optional[str] = None):
        self.success = success
        self.url = url
        self.object_key = object_key
        self.error_message = error_message

class ObjectMetadataRequest:
    def __init__(self, object_key: str):
        self.object_key = object_key

class ObjectMetadataResponse:
    def __init__(self, success: bool, object_key: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None, error_message: Optional[str] = None):
        self.success = success
        self.object_key = object_key
        self.metadata = metadata or {}
        self.error_message = error_message

class ListPrefixRequest:
    def __init__(self, prefix: str = "", max_keys: Optional[int] = None):
        self.prefix = prefix
        self.max_keys = max_keys

class ListedObject:
    def __init__(self, object_key: str, last_modified: Optional[str] = None, size: Optional[int] = None):
        self.object_key = object_key
        self.last_modified = last_modified
        self.size = size

class ListPrefixResponse:
    def __init__(self, success: bool, prefix: str, objects: Optional[List[ListedObject]] = None, error_message: Optional[str] = None):
        self.success = success
        self.prefix = prefix
        self.objects = objects or []
        self.error_message = error_message

class OcrDocumentRequest:
    def __init__(self, object_key: str):
        self.object_key = object_key

class OcrDocumentResponse:
    def __init__(self, success: bool, text_content: Optional[str] = None, error_message: Optional[str] = None):
        self.success = success
        self.text_content = text_content
        self.error_message = error_message

class TranslateTextRequest:
    def __init__(self, text: str, source_language_code: str, target_language_code: str):
        self.text = text
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code

class TranslateTextResponse:
    def __init__(self, success: bool, translated_text: Optional[str] = None, error_message: Optional[str] = None):
        self.success = success
        self.translated_text = translated_text
        self.error_message = error_message

class SummarizeTextRequest:
    def __init__(self, text: str, max_tokens: int = 150):
        self.text = text
        self.max_tokens = max_tokens

class SummarizeTextResponse:
    def __init__(self, success: bool, summary: Optional[str] = None, error_message: Optional[str] = None):
        self.success = success
        self.summary = summary
        self.error_message = error_message

class EmbedTextRequest:
    def __init__(self, text: str):
        self.text = text

class EmbedTextResponse:
    def __init__(self, success: bool, embedding: Optional[List[float]] = None, error_message: Optional[str] = None):
        self.success = success
        self.embedding = embedding
        self.error_message = error_message
