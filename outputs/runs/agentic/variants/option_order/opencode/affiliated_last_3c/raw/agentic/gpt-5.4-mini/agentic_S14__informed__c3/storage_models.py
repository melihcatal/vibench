from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class StorageObjectInput:
    bucket: str
    key: str
    content_type: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)
    body: Any = None


@dataclass
class StorageObjectResult:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    content_length: Optional[int] = None
    content_type: Optional[str] = None
    last_modified: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StorageListItem:
    key: str
    size: Optional[int] = None
    last_modified: Optional[str] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None


@dataclass
class StorageListResult:
    bucket: str
    prefix: str
    items: List[StorageListItem] = field(default_factory=list)
    is_truncated: bool = False
    next_token: Optional[str] = None


def _normalize_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not metadata:
        return {}
    return {str(k): v for k, v in metadata.items()}


def normalize_upload_result(
    bucket: str, key: str, response: Dict[str, Any]
) -> StorageObjectResult:
    return StorageObjectResult(
        bucket=bucket,
        key=key,
        etag=response.get("ETag") or response.get("etag"),
        version_id=response.get("VersionId") or response.get("version_id"),
        metadata=_normalize_metadata(
            response.get("Metadata") or response.get("metadata")
        ),
        extra={
            k: v
            for k, v in response.items()
            if k
            not in {"ETag", "etag", "VersionId", "version_id", "Metadata", "metadata"}
        },
    )


def normalize_head_result(
    bucket: str, key: str, response: Dict[str, Any]
) -> StorageObjectResult:
    return StorageObjectResult(
        bucket=bucket,
        key=key,
        etag=response.get("ETag") or response.get("etag"),
        version_id=response.get("VersionId") or response.get("version_id"),
        content_length=response.get("ContentLength") or response.get("content_length"),
        content_type=response.get("ContentType") or response.get("content_type"),
        last_modified=str(
            response.get("LastModified") or response.get("last_modified") or ""
        )
        or None,
        metadata=_normalize_metadata(
            response.get("Metadata") or response.get("metadata")
        ),
        extra={
            k: v
            for k, v in response.items()
            if k
            not in {
                "ETag",
                "etag",
                "VersionId",
                "version_id",
                "ContentLength",
                "content_length",
                "ContentType",
                "content_type",
                "LastModified",
                "last_modified",
                "Metadata",
                "metadata",
            }
        },
    )


def normalize_list_result(
    bucket: str, prefix: str, response: Dict[str, Any]
) -> StorageListResult:
    contents = response.get("Contents") or response.get("contents") or []
    items = [
        StorageListItem(
            key=item.get("Key") or item.get("key") or "",
            size=item.get("Size") or item.get("size"),
            last_modified=str(
                item.get("LastModified") or item.get("last_modified") or ""
            )
            or None,
            etag=item.get("ETag") or item.get("etag"),
            storage_class=item.get("StorageClass") or item.get("storage_class"),
        )
        for item in contents
    ]
    return StorageListResult(
        bucket=bucket,
        prefix=prefix,
        items=items,
        is_truncated=bool(
            response.get("IsTruncated") or response.get("is_truncated") or False
        ),
        next_token=response.get("NextContinuationToken")
        or response.get("next_token")
        or response.get("NextMarker")
        or response.get("next_marker"),
    )
