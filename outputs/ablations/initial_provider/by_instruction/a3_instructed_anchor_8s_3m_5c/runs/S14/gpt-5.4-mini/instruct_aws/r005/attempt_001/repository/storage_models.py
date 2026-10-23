from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


def normalize_bucket_name(bucket: str) -> str:
    return bucket.strip()


def normalize_object_key(key: str) -> str:
    return key.lstrip("/")


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")
    return str(value)


@dataclass
class UploadResult:
    bucket: str
    key: str
    etag: str
    version_id: Optional[str] = None


@dataclass
class HeadResult:
    bucket: str
    key: str
    metadata: Dict[str, Any]


@dataclass
class ListedObject:
    key: str
    size: int
    last_modified: Optional[str] = None


def normalize_listed_objects(items: Iterable[Dict[str, Any]]) -> List[ListedObject]:
    normalized: List[ListedObject] = []
    for item in items:
        normalized.append(
            ListedObject(
                key=normalize_object_key(item.get("Key", "")),
                size=int(item.get("Size", 0) or 0),
                last_modified=normalize_text(item.get("LastModified")) or None,
            )
        )
    return normalized
