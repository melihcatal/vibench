from typing import Optional, Dict, Any


class ObjectUploadRequest:
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


class ObjectUploadResponse:
    def __init__(self, e_tag: str, version_id: Optional[str] = None):
        self.e_tag = e_tag
        self.version_id = version_id


class PresignedDownloadRequest:
    def __init__(self, bucket_name: str, object_key: str, expiration: int = 3600):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.expiration = expiration


class PresignedDownloadResponse:
    def __init__(self, url: str):
        self.url = url


class ObjectMetadataRequest:
    def __init__(self, bucket_name: str, object_key: str):
        self.bucket_name = bucket_name
        self.object_key = object_key


class ObjectMetadataResponse:
    def __init__(
        self,
        metadata: Dict[str, Any],
        content_type: Optional[str] = None,
        content_length: Optional[int] = None,
    ):
        self.metadata = metadata
        self.content_type = content_type
        self.content_length = content_length


class ListPrefixRequest:
    def __init__(
        self, bucket_name: str, prefix: Optional[str] = None, max_keys: int = 1000
    ):
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.max_keys = max_keys


class ListedObject:
    def __init__(self, key: str, last_modified: Any, e_tag: str, size: int):
        self.key = key
        self.last_modified = last_modified
        self.e_tag = e_tag
        self.size = size


class ListPrefixResponse:
    def __init__(
        self, objects: list[ListedObject], common_prefixes: Optional[list[str]] = None
    ):
        self.objects = objects
        self.common_prefixes = common_prefixes if common_prefixes is not None else []


class OCRDocumentRequest:
    def __init__(self, bucket_name: str, object_key: str):
        self.bucket_name = bucket_name
        self.object_key = object_key


class OCRDocumentResponse:
    def __init__(self, text_content: str, raw_response: Dict[str, Any]):
        self.text_content = text_content
        self.raw_response = raw_response


class TextTranslateRequest:
    def __init__(self, text: str, source_language: str, target_language: str):
        self.text = text
        self.source_language = source_language
        self.target_language = target_language


class TextTranslateResponse:
    def __init__(self, translated_text: str, raw_response: Dict[str, Any]):
        self.translated_text = translated_text
        self.raw_response = raw_response


class AssetSummaryRequest:
    def __init__(
        self,
        text_content: str,
        prompt_template: str,
        model_id: str = "anthropic.claude-v2",
    ):
        self.text_content = text_content
        self.prompt_template = prompt_template
        self.model_id = model_id


class AssetSummaryResponse:
    def __init__(self, summary: str, raw_response: Dict[str, Any]):
        self.summary = summary
        self.raw_response = raw_response


class EmbeddingRequest:
    def __init__(self, text: str, model_id: str = "amazon.titan-embed-text-v1"):
        self.text = text
        self.model_id = model_id


class EmbeddingResponse:
    def __init__(self, embedding: list[float], raw_response: Dict[str, Any]):
        self.embedding = embedding
        self.raw_response = raw_response
