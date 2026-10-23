from typing import Dict, Optional, TypedDict


class UploadRequest(TypedDict):
    bucket_name: str
    object_key: str
    body: bytes
    content_type: Optional[str]
    metadata: Optional[Dict[str, str]]


class UploadResponse(TypedDict):
    object_key: str
    etag: str
    version_id: Optional[str]


class PresignedDownloadRequest(TypedDict):
    bucket_name: str
    object_key: str
    expires_in: int


class PresignedDownloadResponse(TypedDict):
    url: str


class ObjectMetadataRequest(TypedDict):
    bucket_name: str
    object_key: str


class ObjectMetadataResponse(TypedDict):
    content_type: Optional[str]
    content_length: int
    etag: str
    last_modified: str
    metadata: Dict[str, str]
    storage_class: str


class ListPrefixRequest(TypedDict):
    bucket_name: str
    prefix: Optional[str]
    max_keys: Optional[int]


class ListPrefixResponse(TypedDict):
    objects: list[str]
    prefixes: list[str]
    is_truncated: bool
    next_marker: Optional[str]
