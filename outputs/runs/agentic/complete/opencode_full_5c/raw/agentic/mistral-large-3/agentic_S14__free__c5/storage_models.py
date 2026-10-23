from typing import TypedDict, Optional, List
from datetime import datetime


class ObjectMetadata(TypedDict):
    """
    Represents metadata for an object stored in Google Cloud Storage.
    """

    name: str
    size: int
    content_type: Optional[str]
    time_created: datetime
    updated: datetime
    metadata: dict
    etag: Optional[str]
    generation: Optional[int]


class ListPrefixResponse(TypedDict):
    """
    Represents a response from listing objects under a prefix.
    """

    objects: List[ObjectMetadata]
    prefixes: Optional[List[str]]


class UploadRequest(TypedDict, total=False):
    """
    Represents a request to upload an object to Google Cloud Storage.
    """

    bucket_name: str
    object_name: str
    data: bytes
    content_type: Optional[str]
    metadata: Optional[dict]


class UploadResponse(TypedDict):
    """
    Represents a response from uploading an object to Google Cloud Storage.
    """

    object_url: str


class PresignedDownloadRequest(TypedDict):
    """
    Represents a request to generate a presigned download URL.
    """

    bucket_name: str
    object_name: str
    expiration_hours: int


class PresignedDownloadResponse(TypedDict):
    """
    Represents a response from generating a presigned download URL.
    """

    download_url: str
