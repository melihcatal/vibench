from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional, Union


Payload = Union[bytes, bytearray, memoryview, str]


def normalize_bytes(data: Payload) -> bytes:
    if isinstance(data, bytes):
        return data
    if isinstance(data, bytearray):
        return bytes(data)
    if isinstance(data, memoryview):
        return data.tobytes()
    return data.encode("utf-8")


def normalize_metadata(metadata: Optional[Mapping[str, Any]]) -> Dict[str, str]:
    if not metadata:
        return {}
    return {str(k): str(v) for k, v in metadata.items()}


@dataclass
class StorageObjectRef:
    bucket: str
    name: str


@dataclass
class UploadRequest:
    bucket: str
    name: str
    data: Payload
    content_type: Optional[str] = None
    metadata: Optional[Mapping[str, Any]] = None


@dataclass
class DownloadUrlRequest:
    bucket: str
    name: str
    expiration_seconds: int = 900


@dataclass
class ObjectMetadataRequest:
    bucket: str
    name: str


@dataclass
class ListPrefixRequest:
    bucket: str
    prefix: str = ""
