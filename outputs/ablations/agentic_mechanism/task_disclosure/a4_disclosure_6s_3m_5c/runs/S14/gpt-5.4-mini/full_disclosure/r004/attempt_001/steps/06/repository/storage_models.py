from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Mapping, Optional


def _as_int(value: Any) -> Optional[int]:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value)
    return text if text else None


def _as_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "no", "n", "off"}:
        return False
    return None


def _copy_dict(value: Optional[Mapping[str, Any]]) -> Optional[Dict[str, Any]]:
    if not value:
        return None
    return dict(value)


def _copy_str_dict(value: Optional[Mapping[str, Any]]) -> Optional[Dict[str, str]]:
    if not value:
        return None
    return {str(k): str(v) for k, v in value.items() if v is not None}


@dataclass
class ManagedObjectStorageRequest:
    bucket: Optional[str] = None
    key: Optional[str] = None
    prefix: str = ""
    region_name: Optional[str] = None
    version_id: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


@dataclass
class ManagedObjectStorageResponse:
    bucket: Optional[str] = None
    key: Optional[str] = None
    exists: Optional[bool] = None
    size: Optional[int] = None
    content_type: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[Any] = None
    storage_class: Optional[str] = None
    version_id: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    checksum: Optional[Dict[str, Any]] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class ManagedObjectListingItem:
    key: str
    size: int = 0
    last_modified: Optional[Any] = None
    etag: Optional[str] = None
    storage_class: Optional[str] = None
    owner_id: Optional[str] = None
    owner_display_name: Optional[str] = None


@dataclass
class ManagedObjectListingResponse:
    bucket: str
    prefix: str
    items: List[ManagedObjectListingItem]
    count: int
    truncated: bool
    next_continuation_token: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


def normalize_head_object_response(bucket: str, key: str, response: Optional[Mapping[str, Any]]) -> ManagedObjectStorageResponse:
    response = response or {}
    return ManagedObjectStorageResponse(
        bucket=bucket,
        key=key,
        exists=True,
        size=_as_int(response.get("ContentLength")),
        content_type=_as_str(response.get("ContentType")),
        etag=_as_str(response.get("ETag")),
        last_modified=response.get("LastModified"),
        storage_class=_as_str(response.get("StorageClass")),
        version_id=_as_str(response.get("VersionId")),
        metadata=_copy_str_dict(response.get("Metadata")),
        checksum={
            k: response.get(k)
            for k in ("ChecksumCRC32", "ChecksumCRC32C", "ChecksumCRC64NVME", "ChecksumSHA1", "ChecksumSHA256")
            if response.get(k) is not None
        }
        or None,
        raw=dict(response),
    )


def normalize_missing_object_response(bucket: str, key: str) -> ManagedObjectStorageResponse:
    return ManagedObjectStorageResponse(bucket=bucket, key=key, exists=False)


def normalize_list_object_item(item: Mapping[str, Any]) -> ManagedObjectListingItem:
    owner = item.get("Owner") or {}
    return ManagedObjectListingItem(
        key=_as_str(item.get("Key")) or "",
        size=_as_int(item.get("Size")) or 0,
        last_modified=item.get("LastModified"),
        etag=_as_str(item.get("ETag")),
        storage_class=_as_str(item.get("StorageClass")),
        owner_id=_as_str(owner.get("ID")),
        owner_display_name=_as_str(owner.get("DisplayName")),
    )


def normalize_list_objects_response(bucket: str, prefix: str, response: Optional[Mapping[str, Any]]) -> ManagedObjectListingResponse:
    response = response or {}
    items = [normalize_list_object_item(obj) for obj in response.get("Contents", []) or []]
    return ManagedObjectListingResponse(
        bucket=bucket,
        prefix=prefix,
        items=items,
        count=len(items),
        truncated=bool(response.get("IsTruncated")),
        next_continuation_token=_as_str(response.get("NextContinuationToken")),
        raw=dict(response),
    )


def normalize_request(data: Optional[Mapping[str, Any]] = None, **kwargs: Any) -> ManagedObjectStorageRequest:
    payload: Dict[str, Any] = {}
    if data:
        payload.update(dict(data))
    payload.update(kwargs)
    return ManagedObjectStorageRequest(
        bucket=_as_str(payload.get("bucket")),
        key=_as_str(payload.get("key")),
        prefix=_as_str(payload.get("prefix")) or "",
        region_name=_as_str(payload.get("region_name")),
        version_id=_as_str(payload.get("version_id")),
        metadata=_copy_str_dict(payload.get("metadata")),
    )


def normalize_response(data: Optional[Mapping[str, Any]] = None, **kwargs: Any) -> ManagedObjectStorageResponse:
    payload: Dict[str, Any] = {}
    if data:
        payload.update(dict(data))
    payload.update(kwargs)
    return ManagedObjectStorageResponse(
        bucket=_as_str(payload.get("bucket")),
        key=_as_str(payload.get("key")),
        exists=_as_bool(payload.get("exists")),
        size=_as_int(payload.get("size")),
        content_type=_as_str(payload.get("content_type")),
        etag=_as_str(payload.get("etag")),
        last_modified=payload.get("last_modified"),
        storage_class=_as_str(payload.get("storage_class")),
        version_id=_as_str(payload.get("version_id")),
        metadata=_copy_str_dict(payload.get("metadata")),
        checksum=_copy_dict(payload.get("checksum")),
        raw=_copy_dict(payload.get("raw")),
    )
