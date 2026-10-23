from typing import Optional, Dict, Any


class UploadObjectRequest:
    def __init__(
        self,
        container_name: str,
        blob_name: str,
        data: Any,
        content_settings: Optional[Dict[str, Any]] = None,
    ):
        self.container_name = container_name
        self.blob_name = blob_name
        self.data = data
        self.content_settings = content_settings


class UploadObjectResponse:
    def __init__(self, etag: str, last_modified: str):
        self.etag = etag
        self.last_modified = last_modified


class PresignedDownloadRequest:
    def __init__(self, container_name: str, blob_name: str, expiry_minutes: int = 60):
        self.container_name = container_name
        self.blob_name = blob_name
        self.expiry_minutes = expiry_minutes


class PresignedDownloadResponse:
    def __init__(self, url: str):
        self.url = url


class ObjectMetadataRequest:
    def __init__(self, container_name: str, blob_name: str):
        self.container_name = container_name
        self.blob_name = blob_name


class ObjectMetadataResponse:
    def __init__(
        self,
        name: str,
        etag: str,
        last_modified: str,
        size: int,
        content_type: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ):
        self.name = name
        self.etag = etag
        self.last_modified = last_modified
        self.size = size
        self.content_type = content_type
        self.metadata = metadata


class ListPrefixRequest:
    def __init__(self, container_name: str, prefix: Optional[str] = None):
        self.container_name = container_name
        self.prefix = prefix


class ListPrefixResponse:
    def __init__(self, blob_names: list[str]):
        self.blob_names = blob_names
