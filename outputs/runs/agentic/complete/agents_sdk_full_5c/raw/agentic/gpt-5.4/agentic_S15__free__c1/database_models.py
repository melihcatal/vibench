from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import copy


@dataclass
class DocumentRecord:
    id: str
    partition_key: str
    content: Dict[str, Any]
    etag: Optional[str] = None
    ts: Optional[int] = None

    @classmethod
    def from_cosmos_item(cls, item: Dict[str, Any], partition_key_field: str = "partition_key") -> "DocumentRecord":
        data = copy.deepcopy(item)
        identifier = str(data.get("id", ""))
        partition_key = str(data.get(partition_key_field) or data.get("partitionKey") or data.get("pk") or "")
        etag = data.get("_etag")
        ts = data.get("_ts")
        return cls(id=identifier, partition_key=partition_key, content=data, etag=etag, ts=ts)

    def to_cosmos_item(self, partition_key_field: str = "partition_key") -> Dict[str, Any]:
        item = copy.deepcopy(self.content)
        item["id"] = self.id
        item[partition_key_field] = self.partition_key
        return item


@dataclass
class QueryRequest:
    field_name: Optional[str] = None
    field_value: Any = None
    partition_key: Optional[str] = None
    limit: int = 25


@dataclass
class UpdateResult:
    id: str
    updated: bool
    etag: Optional[str] = None
    document: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


@dataclass
class SummaryResult:
    id: str
    summary: str
    model: str


@dataclass
class SafetyResult:
    id: str
    flagged: bool
    category_scores: Dict[str, Any] = field(default_factory=dict)
    provider: str = "OpenAI Moderations"


@dataclass
class TranslationResult:
    id: str
    translated_fields: Dict[str, str]
    target_language: str
    model: str


@dataclass
class ArchiveResult:
    id: str
    bucket: str
    key: str
    version_id: Optional[str] = None
    archived_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def normalize_document_payload(document: Dict[str, Any], primary_id: str, partition_key: Optional[str] = None, partition_key_field: str = "partition_key") -> Dict[str, Any]:
    payload = copy.deepcopy(document)
    payload["id"] = str(primary_id)
    if partition_key is not None:
        payload[partition_key_field] = str(partition_key)
    elif partition_key_field not in payload:
        payload[partition_key_field] = str(primary_id)
    return payload


def extract_text_fields(document: Dict[str, Any], field_names: Optional[List[str]] = None) -> Dict[str, str]:
    if field_names:
        return {name: str(document[name]) for name in field_names if name in document and document[name] is not None}
    extracted: Dict[str, str] = {}
    for key, value in document.items():
        if isinstance(value, str) and not key.startswith("_"):
            extracted[key] = value
    return extracted
