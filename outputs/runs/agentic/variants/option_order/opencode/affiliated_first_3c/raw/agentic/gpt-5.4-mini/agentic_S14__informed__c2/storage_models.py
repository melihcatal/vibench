from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class StorageObjectReference:
    bucket: str
    key: str


@dataclass(frozen=True)
class UploadResult:
    bucket: str
    key: str
    etag: str | None
    version_id: str | None


def normalize_metadata(metadata: dict[str, Any] | None) -> dict[str, str]:
    if not metadata:
        return {}
    return {str(k): str(v) for k, v in metadata.items() if v is not None}
