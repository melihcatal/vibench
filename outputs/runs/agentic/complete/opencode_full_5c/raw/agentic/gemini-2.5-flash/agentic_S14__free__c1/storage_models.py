from typing import Optional, Dict


class UploadObjectRequest:
    def __init__(
        self,
        bucket_name: str,
        object_name: str,
        data: bytes,
        content_type: Optional[str] = None,
    ):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.data = data
        self.content_type = content_type


class PresignedDownloadRequest:
    def __init__(
        self, bucket_name: str, object_name: str, expiration_seconds: int = 3600
    ):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.expiration_seconds = expiration_seconds


class ObjectMetadataRequest:
    def __init__(self, bucket_name: str, object_name: str):
        self.bucket_name = bucket_name
        self.object_name = object_name


class ListPrefixRequest:
    def __init__(
        self, bucket_name: str, prefix: str = "", delimiter: Optional[str] = None
    ):
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.delimiter = delimiter


class ObjectMetadata:
    def __init__(
        self,
        name: str,
        size: int,
        content_type: str,
        etag: str,
        custom_metadata: Optional[Dict[str, str]] = None,
    ):
        self.name = name
        self.size = size
        self.content_type = content_type
        self.etag = etag
        self.custom_metadata = custom_metadata if custom_metadata is not None else {}


class ListedObject:
    def __init__(self, name: str, size: int, updated: str):
        self.name = name
        self.size = size
        self.updated = updated


class OcrRequest:
    def __init__(self, bucket_name: str, object_name: str):
        self.bucket_name = bucket_name
        self.object_name = object_name


class TranslateTextRequest:
    def __init__(
        self, text: str, target_language: str, source_language: Optional[str] = None
    ):
        self.text = text
        self.target_language = target_language
        self.source_language = source_language


class SummarizeTextRequest:
    def __init__(self, text: str):
        self.text = text


class EmbedContentRequest:
    def __init__(self, content: str):
        self.content = content
