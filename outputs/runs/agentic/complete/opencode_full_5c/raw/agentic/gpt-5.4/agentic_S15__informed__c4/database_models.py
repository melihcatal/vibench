from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any
import json


def _to_decimal(value: Any) -> Any:
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, dict):
        return {k: _to_decimal(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_to_decimal(v) for v in value]
    return value


def _from_decimal(value: Any) -> Any:
    if isinstance(value, Decimal):
        if value == value.to_integral_value():
            return int(value)
        return float(value)
    if isinstance(value, dict):
        return {k: _from_decimal(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_from_decimal(v) for v in value]
    return value


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_document(document: dict[str, Any]) -> dict[str, Any]:
    normalized = _from_decimal(document)
    if "id" in normalized:
        normalized["id"] = str(normalized["id"])
    if "version" in normalized:
        normalized["version"] = int(normalized["version"])
    return normalized


def prepare_document(document: dict[str, Any]) -> dict[str, Any]:
    prepared = dict(document)
    if "id" in prepared:
        prepared["id"] = str(prepared["id"])
    return _to_decimal(prepared)


def canonical_json(value: Any) -> str:
    return json.dumps(
        _from_decimal(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )


@dataclass(slots=True)
class DocumentRequest:
    id: str
    payload: dict[str, Any] = field(default_factory=dict)
    partition_key: str | None = None
    expected_version: int | None = None

    def to_item(self) -> dict[str, Any]:
        item = dict(self.payload)
        item["id"] = str(self.id)
        if self.partition_key is not None:
            item["partition_key"] = self.partition_key
        return prepare_document(item)


@dataclass(slots=True)
class DocumentResponse:
    id: str
    found: bool
    document: dict[str, Any] | None
    version: int | None

    @classmethod
    def from_item(cls, item: dict[str, Any] | None) -> "DocumentResponse":
        if not item:
            return cls(id="", found=False, document=None, version=None)
        normalized = normalize_document(item)
        return cls(
            id=normalized["id"],
            found=True,
            document=normalized,
            version=normalized.get("version"),
        )
