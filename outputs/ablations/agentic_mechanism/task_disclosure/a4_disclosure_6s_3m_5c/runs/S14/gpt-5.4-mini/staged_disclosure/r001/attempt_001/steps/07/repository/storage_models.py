from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union


def _to_utc_iso(value: Optional[Union[str, datetime]]) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalize_metadata(value: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not value:
        return {}
    return {str(k): str(v) for k, v in value.items() if v is not None}


@dataclass(frozen=True)
class StorageObjectRequest:
    bucket: str
    key: str
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    cache_control: Optional[str] = None

    def normalize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"bucket": self.bucket, "key": self.key}
        if self.content_type is not None:
            data["content_type"] = self.content_type
        if self.cache_control is not None:
            data["cache_control"] = self.cache_control
        meta = _normalize_metadata(self.metadata)
        if meta:
            data["metadata"] = meta
        return data


@dataclass(frozen=True)
class StorageObjectResponse:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None
    size: Optional[int] = None
    content_type: Optional[str] = None
    last_modified: Optional[Union[str, datetime]] = None
    metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "StorageObjectResponse":
        return cls(
            bucket=str(payload.get("bucket", "")),
            key=str(payload.get("key", "")),
            etag=payload.get("etag"),
            version_id=payload.get("version_id"),
            size=payload.get("size"),
            content_type=payload.get("content_type"),
            last_modified=payload.get("last_modified"),
            metadata=payload.get("metadata") or {},
        )

    def normalize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"bucket": self.bucket, "key": self.key}
        if self.etag is not None:
            data["etag"] = self.etag
        if self.version_id is not None:
            data["version_id"] = self.version_id
        if self.size is not None:
            data["size"] = int(self.size)
        if self.content_type is not None:
            data["content_type"] = self.content_type
        last_modified = _to_utc_iso(self.last_modified)
        if last_modified is not None:
            data["last_modified"] = last_modified
        meta = _normalize_metadata(self.metadata)
        if meta:
            data["metadata"] = meta
        return data


@dataclass(frozen=True)
class BucketListResponse:
    buckets: List[str]

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "BucketListResponse":
        buckets = payload.get("buckets") or []
        return cls(buckets=[str(bucket) for bucket in buckets])

    def normalize(self) -> Dict[str, Any]:
        return {"buckets": list(self.buckets)}


@dataclass(frozen=True)
class ObjectListItem:
    key: str
    size: Optional[int] = None
    etag: Optional[str] = None
    last_modified: Optional[Union[str, datetime]] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "ObjectListItem":
        return cls(
            key=str(payload.get("key", "")),
            size=payload.get("size"),
            etag=payload.get("etag"),
            last_modified=payload.get("last_modified"),
        )

    def normalize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"key": self.key}
        if self.size is not None:
            data["size"] = int(self.size)
        if self.etag is not None:
            data["etag"] = self.etag
        last_modified = _to_utc_iso(self.last_modified)
        if last_modified is not None:
            data["last_modified"] = last_modified
        return data


@dataclass(frozen=True)
class ObjectListResponse:
    bucket: str
    objects: List[ObjectListItem]
    next_token: Optional[str] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "ObjectListResponse":
        objects = [ObjectListItem.from_dict(item) for item in (payload.get("objects") or [])]
        return cls(
            bucket=str(payload.get("bucket", "")),
            objects=objects,
            next_token=payload.get("next_token"),
        )

    def normalize(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "bucket": self.bucket,
            "objects": [item.normalize() for item in self.objects],
        }
        if self.next_token is not None:
            data["next_token"] = self.next_token
        return data
