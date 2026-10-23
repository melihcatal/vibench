from dataclasses import dataclass
from typing import Any


@dataclass
class ObjectReference:
    bucket: str
    name: str


def normalize_prefix(prefix: str | None) -> str:
    return (prefix or "").lstrip("/")


def normalize_metadata(metadata: dict[str, Any] | None) -> dict[str, str]:
    return {str(k): str(v) for k, v in (metadata or {}).items()}
