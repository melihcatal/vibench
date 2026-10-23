from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, MutableMapping, Optional
import re


def _now_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _is_mapping(value: Any) -> bool:
    return isinstance(value, Mapping)


def _normalize_key(key: Any) -> str:
    text = str(key).strip()
    if not text:
        raise ValueError("document keys must be non-empty")
    return text


def _normalize_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return { _normalize_key(k): _normalize_value(v) for k, v in value.items() }
    if isinstance(value, list):
        return [_normalize_value(v) for v in value]
    if isinstance(value, tuple):
        return [_normalize_value(v) for v in value]
    if isinstance(value, set):
        return sorted((_normalize_value(v) for v in value), key=lambda x: repr(x))
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    return value


def normalize_document(document: Mapping[str, Any]) -> dict[str, Any]:
    if not _is_mapping(document):
        raise TypeError("document must be a mapping")
    normalized = { _normalize_key(k): _normalize_value(v) for k, v in document.items() }
    if "id" in normalized:
        normalized["id"] = str(normalized["id"])
    if "created_at" not in normalized:
        normalized["created_at"] = _now_utc_iso()
    normalized.setdefault("updated_at", normalized["created_at"])
    return normalized


@dataclass(frozen=True)
class NoSQLDocumentRequest:
    collection: str
    document: Mapping[str, Any]
    document_id: Optional[str] = None
    upsert: bool = False
    merge: bool = True
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def normalized(self) -> dict[str, Any]:
        payload = {
            "collection": self.collection.strip(),
            "document": normalize_document(self.document),
            "upsert": self.upsert,
            "merge": self.merge,
            "metadata": _normalize_value(self.metadata),
        }
        if self.document_id is not None:
            payload["document_id"] = str(self.document_id).strip()
        return payload


@dataclass(frozen=True)
class NoSQLDocumentResponse:
    ok: bool
    collection: str
    document: Mapping[str, Any] = field(default_factory=dict)
    document_id: Optional[str] = None
    etag: Optional[str] = None
    revision: Optional[int] = None
    error: Optional[str] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_raw(cls, raw: Mapping[str, Any]) -> "NoSQLDocumentResponse":
        if not _is_mapping(raw):
            raise TypeError("raw must be a mapping")
        return cls(
            ok=bool(raw.get("ok", raw.get("success", False))),
            collection=str(raw.get("collection", "")).strip(),
            document=raw.get("document", {}) if _is_mapping(raw.get("document", {})) else {},
            document_id=None if raw.get("document_id") is None else str(raw.get("document_id")),
            etag=None if raw.get("etag") is None else str(raw.get("etag")),
            revision=None if raw.get("revision") is None else int(raw.get("revision")),
            error=None if raw.get("error") is None else str(raw.get("error")),
            metadata=raw.get("metadata", {}) if _is_mapping(raw.get("metadata", {})) else {},
        )

    def normalized(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "collection": self.collection,
            "document": normalize_document(self.document) if self.document else {},
            "document_id": self.document_id,
            "etag": self.etag,
            "revision": self.revision,
            "error": self.error,
            "metadata": _normalize_value(self.metadata),
        }


def normalize_query_filter(query: Mapping[str, Any]) -> dict[str, Any]:
    if not _is_mapping(query):
        raise TypeError("query must be a mapping")
    return { _normalize_key(k): _normalize_value(v) for k, v in query.items() }


def normalize_projection(fields: Any) -> list[str]:
    if fields is None:
        return []
    if isinstance(fields, str):
        fields = [f for f in re.split(r"[\s,]+", fields.strip()) if f]
    if not isinstance(fields, (list, tuple, set)):
        raise TypeError("fields must be a string or an iterable of strings")
    return [str(field).strip() for field in fields if str(field).strip()]


def normalize_sort(sort: Any) -> list[dict[str, Any]]:
    if sort is None:
        return []
    if isinstance(sort, str):
        items = [item for item in re.split(r"[\s,]+", sort.strip()) if item]
        return [{"field": item.lstrip("-").strip(), "direction": -1 if item.startswith("-") else 1} for item in items]
    if not isinstance(sort, (list, tuple)):
        raise TypeError("sort must be a string or a sequence")
    normalized = []
    for item in sort:
        if isinstance(item, str):
            normalized.append({"field": item.lstrip("-").strip(), "direction": -1 if item.startswith("-") else 1})
        elif isinstance(item, Mapping):
            field = str(item.get("field", "")).strip()
            if not field:
                raise ValueError("sort field must be non-empty")
            normalized.append({"field": field, "direction": -1 if int(item.get("direction", 1)) < 0 else 1})
        else:
            raise TypeError("invalid sort item")
    return normalized
