from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(document)
    if "id" not in normalized and "document_id" in normalized:
        normalized["id"] = str(normalized["document_id"])
    if "version" in normalized and normalized["version"] is not None:
        normalized["version"] = int(normalized["version"])
    return normalized


@dataclass
class DocumentRequest:
    document: Dict[str, Any]


@dataclass
class DocumentIdRequest:
    document_id: str


@dataclass
class DocumentFieldQuery:
    field_name: str
    field_value: Any


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    changes: Dict[str, Any]
    expected_version: Optional[int] = None
