from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


RFC3339_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class MetricWindowRequest:
    project_id: str
    metric_type: str
    minutes: int = 15
    interval_seconds: int = 60
    filter_expression: Optional[str] = None
    aggregation_aligner: Optional[str] = None
    aggregation_reducer: Optional[str] = None
    group_by_fields: List[str] = field(default_factory=list)


@dataclass
class MetricPoint:
    timestamp: str
    value: float
    resource_labels: Dict[str, str] = field(default_factory=dict)
    metric_labels: Dict[str, str] = field(default_factory=dict)
    series_name: Optional[str] = None


@dataclass
class MetricWindowResponse:
    metric_type: str
    points: List[MetricPoint]


@dataclass
class MetricStatistics:
    metric_type: str
    point_count: int
    minimum: Optional[float]
    maximum: Optional[float]
    average: Optional[float]
    sum: Optional[float]


@dataclass
class MetricComparison:
    left_label: str
    right_label: str
    left_average: Optional[float]
    right_average: Optional[float]
    absolute_delta: Optional[float]
    percent_delta: Optional[float]


@dataclass
class TrendSummary:
    summary: str
    anomaly_detected: bool
    datapoint_count: int


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def to_rfc3339(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime(RFC3339_FORMAT)


def coerce_numeric_typed_value(typed_value: Any) -> float:
    if typed_value is None:
        return 0.0
    for attr in ("double_value", "int64_value", "bool_value"):
        if hasattr(typed_value, attr):
            current = getattr(typed_value, attr)
            if current is not None:
                return float(current)
    if hasattr(typed_value, "distribution_value") and getattr(typed_value, "distribution_value") is not None:
        distribution = getattr(typed_value, "distribution_value")
        if getattr(distribution, "mean", None) is not None:
            return float(distribution.mean)
    return 0.0


def timestamp_to_rfc3339(ts: Any) -> str:
    if ts is None:
        return ""
    if hasattr(ts, "ToDatetime"):
        return to_rfc3339(ts.ToDatetime().replace(tzinfo=timezone.utc))
    if isinstance(ts, datetime):
        return to_rfc3339(ts)
    return str(ts)


def normalize_time_series(series_iterable: Iterable[Any]) -> List[MetricPoint]:
    normalized: List[MetricPoint] = []
    for series in series_iterable:
        resource_labels = dict(getattr(getattr(series, "resource", None), "labels", {}) or {})
        metric_labels = dict(getattr(getattr(series, "metric", None), "labels", {}) or {})
        series_name = resource_labels.get("instance_id") or resource_labels.get("pod_name") or metric_labels.get("instance_name")
        for point in getattr(series, "points", []) or []:
            interval = getattr(point, "interval", None)
            end_time = getattr(interval, "end_time", None) if interval else None
            value = coerce_numeric_typed_value(getattr(point, "value", None))
            normalized.append(
                MetricPoint(
                    timestamp=timestamp_to_rfc3339(end_time),
                    value=value,
                    resource_labels=resource_labels,
                    metric_labels=metric_labels,
                    series_name=series_name,
                )
            )
    normalized.sort(key=lambda item: item.timestamp)
    return normalized


def compute_basic_stats(points: List[MetricPoint], metric_type: str) -> MetricStatistics:
    values = [point.value for point in points]
    if not values:
        return MetricStatistics(metric_type=metric_type, point_count=0, minimum=None, maximum=None, average=None, sum=None)
    total = float(sum(values))
    return MetricStatistics(
        metric_type=metric_type,
        point_count=len(values),
        minimum=min(values),
        maximum=max(values),
        average=total / len(values),
        sum=total,
    )
