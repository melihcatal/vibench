from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class DocumentRequest:
    document: Dict[str, Any]
    database_name: str = "documents"
    container_name: str = "records"


@dataclass
class DocumentLookup:
    identifier: str
    partition_key: Optional[str] = None
    database_name: str = "documents"
    container_name: str = "records"


@dataclass
class UpdateCondition:
    identifier: str
    partition_key: Optional[str] = None
    etag: Optional[str] = None
    expected_version: Optional[int] = None
    patch: Dict[str, Any] = field(default_factory=dict)
    database_name: str = "documents"
    container_name: str = "records"


@dataclass
class NormalizedResponse:
    ok: bool
    data: Dict[str, Any]
    etag: Optional[str] = None
    request_charge: Optional[float] = None


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(document)
    if "id" not in normalized:
        for candidate in ("document_id", "record_id", "primary_id"):
            if candidate in normalized and normalized[candidate] not in (None, ""):
                normalized["id"] = str(normalized[candidate])
                break
    if "id" in normalized:
        normalized["id"] = str(normalized["id"])
    return normalized
