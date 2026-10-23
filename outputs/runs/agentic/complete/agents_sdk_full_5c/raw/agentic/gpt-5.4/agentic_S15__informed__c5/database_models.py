from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


DocumentData = Dict[str, Any]


@dataclass(slots=True)
class DocumentRecord:
    id: str
    payload: DocumentData
    partition_key: Optional[str] = None
    etag: Optional[str] = None
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_item(self) -> DocumentData:
        item: DocumentData = dict(self.payload)
        item["id"] = self.id
        if self.partition_key is not None:
            item.setdefault("partitionKey", self.partition_key)
        item["updatedAt"] = item.get("updatedAt", self.updated_at)
        return item


@dataclass(slots=True)
class QueryRequest:
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None
    limit: int = 100


@dataclass(slots=True)
class UpdateResult:
    id: str
    status: str
    etag: Optional[str]
    document: DocumentData


def normalize_document(raw: Optional[Mapping[str, Any]]) -> Optional[DocumentData]:
    if raw is None:
        return None
    normalized = dict(raw)
    if "_etag" in normalized and "etag" not in normalized:
        normalized["etag"] = normalized["_etag"]
    return normalized



def normalize_documents(items: Iterable[Mapping[str, Any]]) -> List[DocumentData]:
    return [normalize_document(item) for item in items if item is not None]
