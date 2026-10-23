from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class DocumentRecord:
    document_id: str
    partition_key: Optional[str] = None
    version: int = 1
    data: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_item(self) -> Dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        created_at = self.created_at or now
        updated_at = self.updated_at or now
        item: Dict[str, Any] = {
            "id": self.document_id,
            "version": self.version,
            "created_at": created_at,
            "updated_at": updated_at,
        }
        if self.partition_key is not None:
            item["partition_key"] = self.partition_key
        item.update(self.data)
        return item


@dataclass
class QueryRequest:
    field_name: str
    field_value: Any
    limit: int = 25


@dataclass
class UpdateResult:
    success: bool
    document: Optional[Dict[str, Any]] = None
    message: str = ""



def normalize_document(document: Optional[Mapping[str, Any]]) -> Optional[Dict[str, Any]]:
    if document is None:
        return None
    return dict(document)



def normalize_documents(documents: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    return [dict(document) for document in documents]
