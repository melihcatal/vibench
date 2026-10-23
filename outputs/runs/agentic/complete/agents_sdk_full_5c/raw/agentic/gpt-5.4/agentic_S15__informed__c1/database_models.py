from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import copy


JsonDict = Dict[str, Any]


@dataclass
class DocumentInput:
    document_id: str
    payload: JsonDict
    partition_key: Optional[str] = None

    def to_item(self) -> JsonDict:
        item = copy.deepcopy(self.payload)
        item["id"] = self.document_id
        if self.partition_key is not None:
            item["partition_key"] = self.partition_key
        item.setdefault("updated_at", utc_now_iso())
        return item


@dataclass
class QueryRequest:
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None
    limit: int = 25


@dataclass
class DocumentRecord:
    document_id: str
    data: JsonDict
    etag: Optional[str] = None

    @classmethod
    def from_cosmos_item(cls, item: JsonDict) -> "DocumentRecord":
        normalized = normalize_document(item)
        return cls(
            document_id=str(normalized.get("id")),
            data=normalized,
            etag=item.get("_etag"),
        )


@dataclass
class QueryResponse:
    records: List[DocumentRecord] = field(default_factory=list)
    count: int = 0


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_document(item: JsonDict) -> JsonDict:
    normalized = copy.deepcopy(item)
    normalized.pop("_rid", None)
    normalized.pop("_self", None)
    normalized.pop("_attachments", None)
    normalized.pop("_ts", None)
    return normalized


def ensure_partition_key(data: JsonDict, fallback: Optional[str] = None) -> str:
    if "partition_key" in data and data["partition_key"] is not None:
        return str(data["partition_key"])
    if fallback is not None:
        return str(fallback)
    return str(data.get("id", "default"))
