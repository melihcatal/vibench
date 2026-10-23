from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, BinaryIO, Dict, Iterable, List, Optional, Union


@dataclass(frozen=True)
class UploadResult:
    bucket: str
    key: str
    size: int
    etag: Optional[str]


@dataclass(frozen=True)
class PresignedURL:
    url: str
    expires_in_seconds: int


@dataclass(frozen=True)
class StorageObject:
    key: str
    size: Optional[int] = None
    last_modified: Optional[str] = None
    etag: Optional[str] = None


def read_bytes_source(source: Union[str, bytes, bytearray, BinaryIO]) -> bytes:
    if isinstance(source, (bytes, bytearray)):
        return bytes(source)
    if isinstance(source, str):
        return Path(source).read_bytes()
    data = source.read()
    return data if isinstance(data, bytes) else bytes(data)


def normalize_head_object_response(response: Dict[str, Any], bucket: str, key: str) -> Dict[str, Any]:
    return {
        "bucket": bucket,
        "key": key,
        "content_length": response.get("ContentLength"),
        "content_type": response.get("ContentType"),
        "etag": response.get("ETag"),
        "last_modified": response.get("LastModified").isoformat() if response.get("LastModified") else None,
        "metadata": response.get("Metadata", {}),
        "storage_class": response.get("StorageClass"),
    }


def normalize_list_objects_response(response: Dict[str, Any], bucket: str, prefix: str) -> Dict[str, Any]:
    contents = response.get("Contents", []) or []
    objects: List[Dict[str, Any]] = []
    for item in contents:
        objects.append(
            {
                "key": item.get("Key"),
                "size": item.get("Size"),
                "last_modified": item.get("LastModified").isoformat() if item.get("LastModified") else None,
                "etag": item.get("ETag"),
                "storage_class": item.get("StorageClass"),
            }
        )
    return {
        "bucket": bucket,
        "prefix": prefix,
        "key_count": response.get("KeyCount", len(objects)),
        "is_truncated": response.get("IsTruncated", False),
        "next_continuation_token": response.get("NextContinuationToken"),
        "objects": objects,
    }
