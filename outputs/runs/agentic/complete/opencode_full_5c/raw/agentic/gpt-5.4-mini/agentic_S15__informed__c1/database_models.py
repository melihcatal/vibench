from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_document_id(document_id: Any) -> str:
    value = str(document_id).strip()
    if not value:
        raise ValueError("document_id is required")
    return value


def normalize_payload(payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if payload is None:
        return {}
    if not isinstance(payload, dict):
        raise TypeError("payload must be a mapping")
    return payload


@dataclass
class DocumentUpsertResult:
    document_id: str
    created: bool
    version: Optional[int]
    data: Dict[str, Any]


@dataclass
class DocumentFetchResult:
    found: bool
    document_id: str
    data: Dict[str, Any]


@dataclass
class DocumentQueryResult:
    documents: list


@dataclass
class ConditionalUpdateResult:
    document_id: str
    updated: bool
    version: Optional[int]
    data: Dict[str, Any]
