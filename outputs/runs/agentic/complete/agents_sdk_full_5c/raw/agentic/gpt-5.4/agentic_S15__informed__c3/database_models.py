from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional
import copy


DocumentBody = Dict[str, Any]


@dataclass
class DocumentKey:
    id: str
    partition_key: Optional[str] = None


@dataclass
class UpsertRequest:
    document: Mapping[str, Any]
    id_field: str = "id"
    partition_field: Optional[str] = None


@dataclass
class QueryRequest:
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None
    max_items: int = 100


@dataclass
class ConditionalUpdateRequest:
    key: DocumentKey
    updates: Mapping[str, Any] = field(default_factory=dict)
    expected_etag: Optional[str] = None


@dataclass
class DocumentResponse:
    id: str
    partition_key: Optional[str]
    etag: Optional[str]
    document: DocumentBody



def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()



def normalize_document(document: Mapping[str, Any], id_field: str = "id") -> DocumentBody:
    normalized = copy.deepcopy(dict(document))
    if id_field != "id" and id_field in normalized and "id" not in normalized:
        normalized["id"] = str(normalized[id_field])
    if "id" not in normalized:
        raise ValueError("Document must contain an 'id' field or a configured id_field")
    normalized["id"] = str(normalized["id"])
    if "updated_at" not in normalized:
        normalized["updated_at"] = utc_now_iso()
    return normalized



def extract_partition_key(document: Mapping[str, Any], partition_field: Optional[str]) -> Optional[str]:
    if not partition_field:
        return None
    value = document.get(partition_field)
    return None if value is None else str(value)



def normalize_updates(updates: Mapping[str, Any]) -> Dict[str, Any]:
    payload = copy.deepcopy(dict(updates))
    payload["updated_at"] = utc_now_iso()
    return payload



def response_from_cosmos_item(item: Mapping[str, Any], partition_field: Optional[str] = None) -> DocumentResponse:
    document = dict(item)
    return DocumentResponse(
        id=str(document.get("id")),
        partition_key=str(document.get(partition_field)) if partition_field and document.get(partition_field) is not None else None,
        etag=document.get("_etag"),
        document=document,
    )



def responses_from_items(items: Iterable[Mapping[str, Any]], partition_field: Optional[str] = None) -> List[DocumentResponse]:
    return [response_from_cosmos_item(item, partition_field=partition_field) for item in items]
