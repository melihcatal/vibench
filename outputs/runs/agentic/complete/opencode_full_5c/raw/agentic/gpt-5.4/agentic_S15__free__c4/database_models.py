from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


def normalize_document(document: Mapping[str, Any]) -> Dict[str, Any]:
    normalized = dict(document)
    if "id" in normalized and normalized["id"] is not None:
        normalized["id"] = str(normalized["id"])
    if "pk" in normalized and normalized["pk"] is not None:
        normalized["pk"] = str(normalized["pk"])
    return normalized


@dataclass
class DocumentUpsertRequest:
    document: Dict[str, Any]

    def normalized(self) -> Dict[str, Any]:
        return normalize_document(self.document)


@dataclass
class DocumentFetchRequest:
    document_id: str
    partition_key: Optional[str] = None


@dataclass
class DocumentQueryRequest:
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None
    limit: int = 50


@dataclass
class DocumentConditionalUpdateRequest:
    document_id: str
    patch_operations: List[Dict[str, Any]] = field(default_factory=list)
    partition_key: Optional[str] = None
    etag: Optional[str] = None


@dataclass
class ManagedDocument:
    id: str
    partition_key: Optional[str]
    body: Dict[str, Any]
    etag: Optional[str] = None


def parse_document_response(payload: Mapping[str, Any]) -> ManagedDocument:
    body = normalize_document(payload)
    return ManagedDocument(
        id=str(body.get("id", "")),
        partition_key=body.get("pk") or body.get("partitionKey"),
        body=body,
        etag=body.get("_etag"),
    )


def parse_document_list(items: Iterable[Mapping[str, Any]]) -> List[ManagedDocument]:
    return [parse_document_response(item) for item in items]


def extract_text_fields(
    document: Mapping[str, Any], field_names: Optional[Iterable[str]] = None
) -> Dict[str, str]:
    if field_names is None:
        candidates = document.items()
    else:
        candidates = ((name, document.get(name)) for name in field_names)
    extracted: Dict[str, str] = {}
    for key, value in candidates:
        if isinstance(value, str) and value.strip():
            extracted[str(key)] = value
    return extracted
