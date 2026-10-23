from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class MetricWindowRequest:
    metric_type: str
    start_time: datetime
    end_time: datetime
    filter_expression: Optional[str] = None
    resource_labels: Optional[Dict[str, str]] = None


@dataclass
class MetricSeriesPoint:
    timestamp: datetime
    value: float
    labels: Dict[str, str]


@dataclass
class MetricSeriesResponse:
    metric_type: str
    points: List[MetricSeriesPoint]
    summary: Dict[str, Any]


@dataclass
class MetricStatsResponse:
    metric_type: str
    count: int
    minimum: Optional[float]
    maximum: Optional[float]
    mean: Optional[float]
    p50: Optional[float]
    p95: Optional[float]


@dataclass
class ComparisonResponse:
    left_metric_type: str
    right_metric_type: str
    left_points: List[MetricSeriesPoint]
    right_points: List[MetricSeriesPoint]


@dataclass
class ArchiveResult:
    bucket: str
    object_name: str
    bytes_written: int


def dt_to_rfc3339(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_point(ts: datetime, value: float, labels: Optional[Dict[str, str]] = None) -> MetricSeriesPoint:
    return MetricSeriesPoint(timestamp=ts, value=float(value), labels=labels or {})


def dataclass_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)


def percentile(values: Iterable[float], pct: float) -> Optional[float]:
    ordered = sorted(float(v) for v in values)
    if not ordered:
        return None
    if len(ordered) == 1:
        return ordered[0]
    idx = (len(ordered) - 1) * pct
    lower = int(idx)
    upper = min(lower + 1, len(ordered) - 1)
    frac = idx - lower
    return ordered[lower] * (1 - frac) + ordered[upper] * frac
