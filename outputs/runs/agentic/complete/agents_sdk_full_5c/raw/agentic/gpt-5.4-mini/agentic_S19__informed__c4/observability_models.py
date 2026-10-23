from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence


def _to_utc_iso(value: Any) -> str:
    if value is None:
        return datetime.now(timezone.utc).isoformat()
    if isinstance(value, datetime):
        dt = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    return str(value)


@dataclass
class MetricWindowRequest:
    metric_name: str
    start_time: Any
    end_time: Any
    resource_filter: Optional[Dict[str, str]] = None
    statistics: Sequence[str] = ("avg", "min", "max")
    limit: int = 500

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "metric_name": self.metric_name,
            "start_time": _to_utc_iso(self.start_time),
            "end_time": _to_utc_iso(self.end_time),
            "statistics": list(self.statistics),
            "limit": self.limit,
        }
        if self.resource_filter:
            payload["resource_filter"] = dict(self.resource_filter)
        return payload


@dataclass
class MetricPoint:
    timestamp: str
    value: float
    dimensions: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, item: Mapping[str, Any]) -> "MetricPoint":
        return cls(
            timestamp=str(item.get("timestamp") or item.get("time") or item.get("ts") or ""),
            value=float(item.get("value", 0.0)),
            dimensions={str(k): str(v) for k, v in dict(item.get("dimensions", {})).items()},
        )


@dataclass
class MetricSeriesResponse:
    metric_name: str
    points: List[MetricPoint] = field(default_factory=list)
    provider: str = "datadog"

    @classmethod
    def from_api(cls, metric_name: str, payload: Mapping[str, Any]) -> "MetricSeriesResponse":
        points = [MetricPoint.from_mapping(item) for item in payload.get("points", [])]
        return cls(metric_name=metric_name, points=points, provider=str(payload.get("provider", "datadog")))


@dataclass
class MetricStatsResponse:
    metric_name: str
    statistics: Dict[str, float] = field(default_factory=dict)
    provider: str = "datadog"

    @classmethod
    def from_api(cls, metric_name: str, payload: Mapping[str, Any]) -> "MetricStatsResponse":
        stats = {str(k): float(v) for k, v in dict(payload.get("statistics", {})).items()}
        return cls(metric_name=metric_name, statistics=stats, provider=str(payload.get("provider", "datadog")))


@dataclass
class MetricComparisonResponse:
    metric_name: str
    left: MetricSeriesResponse
    right: MetricSeriesResponse


@dataclass
class MetricSummary:
    metric_name: str
    trend: str
    anomaly_score: float
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ArchivedObjectResult:
    bucket: str
    key: str
    etag: Optional[str] = None
    version_id: Optional[str] = None


@dataclass
class NormalizedTextResult:
    text: str
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyResult:
    unsafe: bool
    score: float
    categories: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)
