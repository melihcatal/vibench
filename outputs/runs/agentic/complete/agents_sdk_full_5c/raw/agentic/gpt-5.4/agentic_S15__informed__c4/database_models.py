from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass(slots=True)
class DocumentRecord:
    document_id: str
    payload: Dict[str, Any]
    partition_key: Optional[str] = None
    etag: Optional[str] = None
    last_updated: Optional[str] = None

    def to_cosmos_item(self) -> Dict[str, Any]:
        item = dict(self.payload)
        item["id"] = self.document_id
        if self.partition_key is not None:
            item.setdefault("partitionKey", self.partition_key)
        if self.last_updated is None:
            item["lastUpdated"] = datetime.now(timezone.utc).isoformat()
        else:
            item["lastUpdated"] = self.last_updated
        return item


@dataclass(slots=True)
class QueryRequest:
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None
    limit: int = 50


@dataclass(slots=True)
class OperationResult:
    success: bool
    document: Optional[Dict[str, Any]] = None
    documents: List[Dict[str, Any]] = field(default_factory=list)
    etag: Optional[str] = None
    status_message: str = ""


SYSTEM_FIELDS = {"_rid", "_self", "_etag", "_attachments", "_ts"}


def normalize_document(item: Optional[Mapping[str, Any]]) -> Optional[Dict[str, Any]]:
    if item is None:
        return None
    normalized = {k: v for k, v in dict(item).items() if k not in SYSTEM_FIELDS}
    if "id" in normalized:
        normalized["document_id"] = normalized.pop("id")
    if "partitionKey" in normalized:
        normalized["partition_key"] = normalized["partitionKey"]
    return normalized


def normalize_documents(items: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    return [doc for doc in (normalize_document(item) for item in items) if doc is not None]
