from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import copy


DocumentDict = Dict[str, Any]


@dataclass
class DocumentRecord:
    id: str
    partition_key: str
    content: DocumentDict = field(default_factory=dict)
    version: Optional[str] = None
    etag: Optional[str] = None
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_item(self) -> DocumentDict:
        item = copy.deepcopy(self.content)
        item["id"] = self.id
        item["partitionKey"] = self.partition_key
        item["updatedAt"] = self.updated_at
        if self.version is not None:
            item["version"] = self.version
        if self.etag is not None:
            item["_etag"] = self.etag
        return item


@dataclass
class QueryRequest:
    field_name: Optional[str] = None
    field_value: Optional[Any] = None
    partition_key: Optional[str] = None
    limit: int = 50


@dataclass
class OperationResult:
    ok: bool
    item: Optional[DocumentDict] = None
    items: Optional[List[DocumentDict]] = None
    message: Optional[str] = None
    etag: Optional[str] = None
    request_charge: Optional[float] = None


def normalize_document(payload: DocumentDict) -> DocumentDict:
    item = copy.deepcopy(payload)
    if "id" not in item or not item["id"]:
        raise ValueError("document payload must include a non-empty 'id'")
    if "partitionKey" not in item or not item["partitionKey"]:
        raise ValueError("document payload must include a non-empty 'partitionKey'")
    return item


def normalize_records(items: List[DocumentDict]) -> List[DocumentDict]:
    normalized: List[DocumentDict] = []
    for item in items:
        clone = copy.deepcopy(item)
        clone.setdefault("id", "")
        clone.setdefault("partitionKey", "")
        normalized.append(clone)
    return normalized
