from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence


def _iso_utc(value: Any) -> str:
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, (int, float)):
        dt = datetime.fromtimestamp(value, tz=timezone.utc)
    elif isinstance(value, str):
        try:
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return value
    else:
        return str(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalize_scalar(value: Any) -> Any:
    if isinstance(value, datetime):
        return _iso_utc(value)
    if isinstance(value, Mapping):
        return {str(k): _normalize_scalar(v) for k, v in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_normalize_scalar(v) for v in value]
    return value


def normalize_labels(labels: Mapping[str, Any] | None) -> dict[str, str]:
    if not labels:
        return {}
    return {str(k): str(_normalize_scalar(v)) for k, v in labels.items() if v is not None}


def normalize_dimensions(dimensions: Mapping[str, Any] | None) -> dict[str, Any]:
    if not dimensions:
        return {}
    return {str(k): _normalize_scalar(v) for k, v in dimensions.items() if v is not None}


@dataclass(slots=True)
class ManagedMetricsMonitoringRequest:
    service: str
    metric_name: str
    value: float
    timestamp: datetime | str | int | float | None = None
    labels: Mapping[str, Any] | None = None
    dimensions: Mapping[str, Any] | None = None
    attributes: Mapping[str, Any] | None = None

    def to_payload(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "service": self.service,
            "metric_name": self.metric_name,
            "value": self.value,
        }
        if self.timestamp is not None:
            payload["timestamp"] = _iso_utc(self.timestamp)
        if self.labels:
            payload["labels"] = normalize_labels(self.labels)
        if self.dimensions:
            payload["dimensions"] = normalize_dimensions(self.dimensions)
        if self.attributes:
            payload["attributes"] = normalize_dimensions(self.attributes)
        return payload


@dataclass(slots=True)
class ManagedMetricsMonitoringResponse:
    ok: bool
    metric_id: str | None = None
    ingested_at: str | None = None
    normalized: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "ManagedMetricsMonitoringResponse":
        normalized = dict(payload)
        ingested_at = normalized.get("ingested_at")
        if ingested_at is not None:
            normalized["ingested_at"] = _iso_utc(ingested_at)
        return cls(
            ok=bool(normalized.get("ok", True)),
            metric_id=normalized.get("metric_id"),
            ingested_at=normalized.get("ingested_at"),
            normalized=normalized,
            raw=dict(payload),
        )


def normalize_monitoring_event(event: Mapping[str, Any]) -> dict[str, Any]:
    normalized = {str(k): _normalize_scalar(v) for k, v in event.items() if v is not None}
    if "timestamp" in normalized:
        normalized["timestamp"] = _iso_utc(normalized["timestamp"])
    if "labels" in normalized and isinstance(normalized["labels"], Mapping):
        normalized["labels"] = normalize_labels(normalized["labels"])
    if "dimensions" in normalized and isinstance(normalized["dimensions"], Mapping):
        normalized["dimensions"] = normalize_dimensions(normalized["dimensions"])
    return normalized
