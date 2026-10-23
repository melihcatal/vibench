from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional
import copy


DocumentDict = Dict[str, Any]


@dataclass
class DocumentRecord:
    id: str
    partition_key: str
    body: DocumentDict = field(default_factory=dict)
    etag: Optional[str] = None
    ts: Optional[int] = None

    def to_cosmos_item(self) -> DocumentDict:
        item = copy.deepcopy(self.body)
        item["id"] = self.id
        item.setdefault("partitionKey", self.partition_key)
        return item


@dataclass
class QueryRequest:
    field_name: Optional[str] = None
    field_value: Any = None
    partition_key: Optional[str] = None
    max_items: int = 50


@dataclass
class UpdateRequest:
    id: str
    partition_key: str
    updates: DocumentDict
    etag: Optional[str] = None


@dataclass
class OperationResult:
    ok: bool
    item: Optional[DocumentDict] = None
    items: Optional[List[DocumentDict]] = None
    etag: Optional[str] = None
    status_code: Optional[int] = None
    message: Optional[str] = None


SYSTEM_FIELDS = {"_etag", "_rid", "_self", "_attachments", "_ts"}


def normalize_document(item: Optional[DocumentDict]) -> Optional[DocumentDict]:
    if item is None:
        return None
    normalized = {k: v for k, v in item.items() if k not in SYSTEM_FIELDS}
    if "_ts" in item:
        normalized["updated_at"] = datetime.fromtimestamp(item["_ts"], tz=timezone.utc).isoformat()
    if "_etag" in item:
        normalized["etag"] = item["_etag"]
    return normalized


def normalize_documents(items: Iterable[DocumentDict]) -> List[DocumentDict]:
    return [doc for doc in (normalize_document(item) for item in items) if doc is not None]
