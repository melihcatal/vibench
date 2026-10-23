from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class MetricWindowRequest:
    metric_type: str
    start_time: datetime
    end_time: datetime
    resource_type: Optional[str] = None
    filter_labels: Dict[str, str] = field(default_factory=dict)

    def normalized_bounds(self) -> tuple[str, str]:
        return _to_rfc3339(self.start_time), _to_rfc3339(self.end_time)


@dataclass(frozen=True)
class MetricPoint:
    timestamp: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class MetricSeriesResponse:
    metric_type: str
    points: List[MetricPoint]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MetricAggregateResponse:
    metric_type: str
    count: int
    minimum: Optional[float]
    maximum: Optional[float]
    average: Optional[float]
    sum: Optional[float]


@dataclass(frozen=True)
class MetricComparisonResponse:
    left: MetricSeriesResponse
    right: MetricSeriesResponse


def _to_rfc3339(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def flatten_numeric_points(points: Iterable[MetricPoint]) -> List[float]:
    return [point.value for point in points]


def summarize_values(values: Iterable[float]) -> Dict[str, Optional[float]]:
    vals = list(values)
    if not vals:
        return {"count": 0, "minimum": None, "maximum": None, "average": None, "sum": None}
    total = float(sum(vals))
    return {
        "count": len(vals),
        "minimum": min(vals),
        "maximum": max(vals),
        "average": total / len(vals),
        "sum": total,
    }
