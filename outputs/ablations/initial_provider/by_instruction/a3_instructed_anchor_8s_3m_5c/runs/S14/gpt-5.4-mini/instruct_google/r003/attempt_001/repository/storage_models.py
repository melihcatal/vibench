from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class UploadObjectRequest:
    bucket: str
    object_name: str
    data: Any
    content_type: Optional[str] = None


@dataclass(frozen=True)
class ObjectReference:
    bucket: str
    object_name: str


def normalize_prefix(prefix: Optional[str]) -> str:
    return "" if prefix is None else prefix.lstrip("/")


def normalize_blob_metadata(blob: Any) -> Dict[str, Any]:
    return {
        "bucket": blob.bucket.name,
        "name": blob.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "updated": blob.updated.isoformat() if blob.updated else None,
        "md5_hash": blob.md5_hash,
        "crc32c": blob.crc32c,
        "generation": blob.generation,
        "metageneration": blob.metageneration,
    }


def normalize_blob_list(blobs: Iterable[Any]) -> List[Dict[str, Any]]:
    return [normalize_blob_metadata(blob) for blob in blobs]
