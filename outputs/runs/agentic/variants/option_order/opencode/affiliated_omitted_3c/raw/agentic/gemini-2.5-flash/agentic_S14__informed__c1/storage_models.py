from typing import Dict, Any, Optional


class UploadObjectRequest:
    def __init__(
        self,
        bucket_name: str,
        object_key: str,
        data,
        metadata: Optional[Dict[str, str]] = None,
    ):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.data = data
        self.metadata = metadata if metadata is not None else {}


class UploadObjectResponse:
    def __init__(self, etag: str, version_id: Optional[str] = None):
        self.etag = etag
        self.version_id = version_id


class PresignedDownloadRequest:
    def __init__(
        self, bucket_name: str, object_key: str, expiration_seconds: int = 3600
    ):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.expiration_seconds = expiration_seconds


class PresignedDownloadResponse:
    def __init__(self, url: str):
        self.url = url


class ObjectMetadataRequest:
    def __init__(self, bucket_name: str, object_key: str):
        self.bucket_name = bucket_name
        self.object_key = object_key


class ObjectMetadataResponse:
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata


class ListPrefixRequest:
    def __init__(self, bucket_name: str, prefix: str = "", max_keys: int = 1000):
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.max_keys = max_keys


class ListPrefixResponse:
    def __init__(self, object_keys: list[str], common_prefixes: list[str]):
        self.object_keys = object_keys
        self.common_prefixes = common_prefixes


class DocumentOcrRequest:
    def __init__(self, bucket_name: str, object_key: str):
        self.bucket_name = bucket_name
        self.object_key = object_key


class DocumentOcrResponse:
    def __init__(self, text_detections: list[str]):
        self.text_detections = text_detections


class TextTranslateRequest:
    def __init__(self, text: str, source_language_code: str, target_language_code: str):
        self.text = text
        self.source_language_code = source_language_code
        self.target_language_code = target_language_code


class TextTranslateResponse:
    def __init__(self, translated_text: str):
        self.translated_text = translated_text


class AssetSummaryRequest:
    def __init__(self, text_content: str, max_tokens: int = 200):
        self.text_content = text_content
        self.max_tokens = max_tokens


class AssetSummaryResponse:
    def __init__(self, summary_text: str):
        self.summary_text = summary_text


class MetadataEmbeddingRequest:
    def __init__(self, text: str):
        self.text = text


class MetadataEmbeddingResponse:
    def __init__(self, embedding: list[float]):
        self.embedding = embedding
