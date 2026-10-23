from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_config(config: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return dict(config or {})


def normalize_object_name(payload: Dict[str, Any]) -> str:
    return payload["object_name"]


def normalize_prefix(payload: Dict[str, Any]) -> str:
    return payload.get("prefix", "")


def normalize_document_text(payload: Dict[str, Any]) -> str:
    return payload.get("text", "")


@dataclass
class MetadataResult:
    object_name: str
    size: int
    content_type: Optional[str] = None
    etag: Optional[str] = None


@dataclass
class ListResult:
    objects: list
