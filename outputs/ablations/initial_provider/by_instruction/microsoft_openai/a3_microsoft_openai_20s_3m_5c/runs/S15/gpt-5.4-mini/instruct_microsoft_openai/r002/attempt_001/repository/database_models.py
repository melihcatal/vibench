import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _as_dict(value: Any) -> Dict[str, Any]:
    return value if isinstance(value, dict) else {}


def normalize_document(document: Any, primary_key: str = "id") -> Dict[str, Any]:
    data = _as_dict(document).copy()
    if primary_key not in data and "id" in data:
        data[primary_key] = data["id"]
    if "id" not in data and primary_key in data:
        data["id"] = data[primary_key]
    return data


@dataclass
class DocumentUpsertRequest:
    document: Dict[str, Any]
    primary_key: str = "id"


@dataclass
class DocumentFetchRequest:
    document_id: str
    partition_key: Optional[str] = None


@dataclass
class DocumentQueryRequest:
    field_name: str
    field_value: Any


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    patch: Dict[str, Any]
    version: Optional[int] = None


@dataclass
class DocumentResponse:
    ok: bool
    document: Optional[Dict[str, Any]] = None
    documents: Optional[List[Dict[str, Any]]] = None
    raw: Optional[Any] = None


def env(name: str, default: str = "") -> str:
    return os.getenv(name, default)
