from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class MetricWindowRequest:
    metric_name: str
    start: datetime
    end: datetime


@dataclass(frozen=True)
class MetricFilterRequest(MetricWindowRequest):
    filters: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class MetricCompareRequest:
    metric_name: str
    start: datetime
    end: datetime
    left_filters: Dict[str, str] = field(default_factory=dict)
    right_filters: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class MetricSummaryRequest(MetricWindowRequest):
    threshold: float = 0.0


@dataclass(frozen=True)
class NoteTranslationRequest:
    text: str
    target_language: str


@dataclass(frozen=True)
class SafetyCheckRequest:
    text: str
    categories: Optional[List[str]] = None


@dataclass(frozen=True)
class ExportArchiveRequest:
    name: str
    payload: Dict[str, Any]


@dataclass
class MetricPoint:
    timestamp: datetime
    value: float
    dimensions: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeries:
    name: str
    points: List[MetricPoint]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MetricResponse:
    series: List[MetricSeries]
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_time(value: datetime) -> int:
    return int(value.astimezone(timezone.utc).timestamp())


def parse_series_payload(payload: Dict[str, Any]) -> MetricResponse:
    series_list: List[MetricSeries] = []
    for item in payload.get("series", payload.get("data", [])):
        points: List[MetricPoint] = []
        for point in item.get("pointlist", item.get("points", [])):
            if isinstance(point, dict):
                ts = datetime.fromtimestamp(point.get("timestamp", point.get("ts", 0)), tz=timezone.utc)
                value = float(point.get("value", 0.0))
                dims = {str(k): str(v) for k, v in point.get("dimensions", {}).items()}
            else:
                ts = datetime.fromtimestamp(point[0], tz=timezone.utc)
                value = float(point[1])
                dims = {}
            points.append(MetricPoint(timestamp=ts, value=value, dimensions=dims))
        series_list.append(MetricSeries(name=item.get("metric", item.get("name", "metric")), points=points, metadata=item))
    return MetricResponse(series=series_list, raw=payload)


def flatten_values(response: MetricResponse) -> List[float]:
    values: List[float] = []
    for series in response.series:
        values.extend(point.value for point in series.points)
    return values


def to_query(filters: Dict[str, str]) -> str:
    parts = [f"{k}:{v}" for k, v in sorted(filters.items())]
    return "{" + ",".join(parts) + "}" if parts else "*"
