from dataclasses import dataclass
from typing import Any


@dataclass
class ObjectTarget:
    bucket: str
    key: str


@dataclass
class UploadResult:
    bucket: str
    key: str
    etag: str | None = None
    version_id: str | None = None


def normalize_metadata(metadata: dict[str, Any] | None) -> dict[str, str]:
    if not metadata:
        return {}
    return {str(k): str(v) for k, v in metadata.items()}


def normalize_body(body: bytes | bytearray | memoryview | str) -> bytes:
    if isinstance(body, str):
        return body.encode("utf-8")
    return bytes(body)
