from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Mapping, MutableMapping, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_document(doc: Mapping[str, Any]) -> Dict[str, Any]:
    normalized = dict(doc)
    if "document_id" in normalized:
        normalized["document_id"] = str(normalized["document_id"])
    if "updated_at" not in normalized:
        normalized["updated_at"] = utc_now_iso()
    return normalized


@dataclass
class DocumentUpsertRequest:
    document_id: str
    document: Dict[str, Any]
    sort_key: Optional[str] = None

    def to_item(self) -> Dict[str, Any]:
        item = normalize_document(self.document)
        item["document_id"] = self.document_id
        if self.sort_key is not None:
            item["sort_key"] = self.sort_key
        return item


@dataclass
class DocumentFetchResponse:
    found: bool
    document: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentQueryRequest:
    field_name: str
    field_value: Any
    index_name: Optional[str] = None


@dataclass
class DocumentQueryResponse:
    items: list[Dict[str, Any]]
    count: int


@dataclass
class DocumentConditionalUpdateRequest:
    document_id: str
    updates: Dict[str, Any]
    expected_version: Optional[int] = None
    sort_key: Optional[str] = None


@dataclass
class DocumentConditionalUpdateResponse:
    updated: bool
    document: Dict[str, Any] = field(default_factory=dict)


def merge_updates(existing: MutableMapping[str, Any], updates: Mapping[str, Any]) -> Dict[str, Any]:
    merged = dict(existing)
    merged.update(updates)
    merged["updated_at"] = utc_now_iso()
    return merged
