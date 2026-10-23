from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class StorageUploadRequest:
    bucket: str
    object_key: str
    file_path: Optional[str] = None
    data: Optional[bytes] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    storage_class: Optional[str] = None


@dataclass
class StorageUploadResponse:
    success: bool
    object_key: str
    bucket: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    size: Optional[int] = None
    error: Optional[str] = None


@dataclass
class PresignedUrlRequest:
    bucket: str
    object_key: str
    expires_in_seconds: int = 3600
    http_method: str = "GET"


@dataclass
class PresignedUrlResponse:
    success: bool
    url: Optional[str] = None
    expires_at: Optional[datetime] = None
    error: Optional[str] = None


@dataclass
class ObjectMetadataRequest:
    bucket: str
    object_key: str


@dataclass
class ObjectMetadataResponse:
    success: bool
    object_key: str
    bucket: str
    content_type: Optional[str] = None
    content_length: Optional[int] = None
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None
    metadata: Optional[Dict[str, str]] = field(default_factory=dict)
    error: Optional[str] = None


@dataclass
class ListPrefixRequest:
    bucket: str
    prefix: str = ""
    delimiter: Optional[str] = None
    max_keys: int = 1000
    marker: Optional[str] = None


@dataclass
class ObjectInfo:
    key: str
    size: int
    last_modified: Optional[datetime] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None


@dataclass
class ListPrefixResponse:
    success: bool
    objects: List[ObjectInfo] = field(default_factory=list)
    common_prefixes: List[str] = field(default_factory=list)
    is_truncated: bool = False
    next_marker: Optional[str] = None
    error: Optional[str] = None


def normalize_oss_metadata_to_response(head_result) -> ObjectMetadataResponse:
    return ObjectMetadataResponse(
        success=True,
        object_key=head_result.key,
        bucket=head_result.bucket_name,
        content_type=head_result.content_type,
        content_length=head_result.content_length,
        last_modified=head_result.last_modified,
        etag=head_result.etag,
        storage_class=head_result.storage_class,
        metadata=dict(head_result.user_metadata)
        if hasattr(head_result, "user_metadata") and head_result.user_metadata
        else {},
    )


def normalize_oss_object_to_info(obj) -> ObjectInfo:
    return ObjectInfo(
        key=obj.key,
        size=obj.size,
        last_modified=obj.last_modified,
        etag=obj.etag,
        storage_class=obj.storage_class,
    )


def to_dict(response_obj):
    return asdict(response_obj)
