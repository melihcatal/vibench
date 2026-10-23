from dataclasses import dataclass
from typing import Any, Optional


def normalize_object_name(payload: dict[str, Any]) -> str:
    return payload.get('object_name') or payload.get('blob_name') or payload['name']


def normalize_container(config: dict[str, Any]) -> str:
    return config.get('container') or config['bucket']


@dataclass
class ObjectReference:
    container: str
    object_name: str


@dataclass
class StoredObjectMetadata:
    object_name: str
    container: str
    size: Optional[int] = None
    content_type: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    metadata: Optional[dict[str, Any]] = None


@dataclass
class TextExtractionResult:
    object_name: str
    text: str
    language: Optional[str] = None
