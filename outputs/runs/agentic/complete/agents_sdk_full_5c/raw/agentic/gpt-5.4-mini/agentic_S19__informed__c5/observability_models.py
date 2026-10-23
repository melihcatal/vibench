from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Iterable, Mapping, Sequence


def iso_utc(value: datetime | None) -> str:
    if value is None:
        value = datetime.now(timezone.utc)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


def window_bounds(minutes: int = 60, end: datetime | None = None) -> tuple[str, str]:
    end_dt = end or datetime.now(timezone.utc)
    start_dt = end_dt - timedelta(minutes=minutes)
    return iso_utc(start_dt), iso_utc(end_dt)


def compact_mapping(items: Mapping[str, Any] | None) -> dict[str, Any]:
    return {str(k): v for k, v in (items or {}).items() if v is not None}


def normalize_points(points: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    normalized: list[dict[str, Any]] = []
    for point in points:
        normalized.append(
            {
                "timestamp": point.get("timestamp") or point.get("time") or point.get("interval", {}).get("endTime"),
                "value": point.get("value") or point.get("avg") or point.get("sum") or point.get("maximum") or point.get("minimum"),
                "dimensions": compact_mapping(point.get("dimensions") or point.get("labels") or point.get("resource")),
            }
        )
    return normalized


@dataclass(slots=True)
class MetricWindowRequest:
    metric_name: str
    minutes: int = 60
    resource: str | None = None
    dimensions: dict[str, str] = field(default_factory=dict)
    aggregation: str = "avg"

    def to_query(self) -> dict[str, Any]:
        start, end = window_bounds(self.minutes)
        query = {
            "metric": self.metric_name,
            "start_time": start,
            "end_time": end,
            "aggregation": self.aggregation,
        }
        if self.resource:
            query["resource"] = self.resource
        if self.dimensions:
            query.update({f"dimension_{k}": v for k, v in self.dimensions.items()})
        return query


@dataclass(slots=True)
class MetricSeriesResponse:
    metric_name: str
    provider: str
    points: list[dict[str, Any]]
    raw: Any = None

    @classmethod
    def from_provider_payload(cls, provider: str, metric_name: str, payload: Any, point_selector: Callable[[Any], Sequence[Mapping[str, Any]]] | None = None) -> "MetricSeriesResponse":
        selector = point_selector or (lambda p: p.get("data", []) if isinstance(p, Mapping) else [])
        points = normalize_points(selector(payload))
        return cls(metric_name=metric_name, provider=provider, points=points, raw=payload)


@dataclass(slots=True)
class MetricSummary:
    metric_name: str
    provider: str
    count: int
    minimum: float | None
    maximum: float | None
    average: float | None
    anomaly_score: float | None = None


@dataclass(slots=True)
class SafetyVerdict:
    provider: str
    is_safe: bool
    score: float | None = None
    reasons: list[str] = field(default_factory=list)


@dataclass(slots=True)
class TranslationRequest:
    text: str
    target_language: str
    source_language: str | None = None


@dataclass(slots=True)
class ArchiveRequest:
    bucket: str
    key: str
    payload: bytes
    content_type: str = "application/json"
