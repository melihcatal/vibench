from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional
import copy
import datetime as dt


JsonDict = Dict[str, Any]


@dataclass
class DocumentRecord:
    id: str
    partition_key: str
    content: JsonDict = field(default_factory=dict)
    etag: Optional[str] = None
    timestamp: Optional[str] = None

    def to_cosmos_item(self) -> JsonDict:
        item = copy.deepcopy(self.content)
        item["id"] = self.id
        item.setdefault("partitionKey", self.partition_key)
        return item


@dataclass
class QueryRequest:
    field_name: Optional[str] = None
    field_value: Any = None
    partition_key: Optional[str] = None
    limit: int = 50


@dataclass
class ConditionalUpdateRequest:
    id: str
    partition_key: str
    updates: JsonDict
    expected_etag: Optional[str] = None


def utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def normalize_document(item: JsonDict) -> DocumentRecord:
    payload = copy.deepcopy(item)
    doc_id = str(payload.pop("id"))
    partition_key = str(payload.pop("partitionKey", payload.pop("pk", "")))
    etag = payload.pop("_etag", None)
    timestamp = payload.pop("_ts", None)
    return DocumentRecord(
        id=doc_id,
        partition_key=partition_key,
        content=payload,
        etag=etag,
        timestamp=str(timestamp) if timestamp is not None else None,
    )


def normalize_documents(items: Iterable[JsonDict]) -> List[DocumentRecord]:
    return [normalize_document(item) for item in items]
