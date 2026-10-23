import io
from typing import Dict, Optional, Union


class UploadObjectRequest:
    def __init__(
        self,
        bucket_name: str,
        object_name: str,
        data: Union[bytes, io.BytesIO],
        content_type: Optional[str] = None,
    ):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.data = data
        self.content_type = content_type


class UploadObjectResponse:
    def __init__(self, bucket_name: str, object_name: str, etag: str, size: int):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.etag = etag
        self.size = size


class PresignedDownloadRequest:
    def __init__(
        self, bucket_name: str, object_name: str, expiration_seconds: int = 3600
    ):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.expiration_seconds = expiration_seconds


class PresignedDownloadResponse:
    def __init__(self, presigned_url: str):
        self.presigned_url = presigned_url


class ObjectMetadataRequest:
    def __init__(self, bucket_name: str, object_name: str):
        self.bucket_name = bucket_name
        self.object_name = object_name


class ObjectMetadataResponse:
    def __init__(
        self,
        bucket_name: str,
        object_name: str,
        size: int,
        content_type: str,
        etag: str,
        last_modified: str,
        metadata: Dict,
    ):
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.size = size
        self.content_type = content_type
        self.etag = etag
        self.last_modified = last_modified
        self.metadata = metadata


class ListPrefixRequest:
    def __init__(
        self, bucket_name: str, prefix: str = "", delimiter: Optional[str] = None
    ):
        self.bucket_name = bucket_name
        self.prefix = prefix
        self.delimiter = delimiter


class ListPrefixResponse:
    def __init__(self, bucket_name: str, objects: list[Dict]):
        self.bucket_name = bucket_name
        self.objects = objects
