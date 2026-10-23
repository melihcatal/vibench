from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


RFC3339_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def to_rfc3339(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).strftime(RFC3339_FORMAT)


@dataclass(slots=True)
class MetricWindowRequest:
    project_id: str
    metric_type: str
    start_time: datetime
    end_time: datetime
    alignment_period_seconds: int = 60
    per_series_aligner: str = "ALIGN_MEAN"
    resource_type: Optional[str] = None
    resource_labels: Dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class MetricPoint:
    interval_end: str
    value: float
    resource_type: Optional[str] = None
    metric_labels: Dict[str, str] = field(default_factory=dict)
    resource_labels: Dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class MetricSeriesResult:
    metric_type: str
    points: List[MetricPoint]
    series_count: int


@dataclass(slots=True)
class MetricStatsResult:
    metric_type: str
    statistic: str
    value: float
    start_time: str
    end_time: str


@dataclass(slots=True)
class SeriesComparisonResult:
    metric_type: str
    left_label: str
    right_label: str
    left_points: List[MetricPoint]
    right_points: List[MetricPoint]
    left_average: float
    right_average: float
    average_delta: float


def extract_numeric_value(point_value: Dict[str, Any]) -> float:
    if "doubleValue" in point_value:
        return float(point_value["doubleValue"])
    if "int64Value" in point_value:
        return float(point_value["int64Value"])
    if "boolValue" in point_value:
        return 1.0 if point_value["boolValue"] else 0.0
    if "distributionValue" in point_value:
        distribution = point_value["distributionValue"]
        count = float(distribution.get("count", 0.0))
        mean = float(distribution.get("mean", 0.0))
        return mean if count else 0.0
    raise ValueError(f"Unsupported Monitoring point value: {point_value}")


def normalize_time_series_point(series: Dict[str, Any], point: Dict[str, Any]) -> MetricPoint:
    interval = point.get("interval", {})
    return MetricPoint(
        interval_end=interval.get("endTime", ""),
        value=extract_numeric_value(point.get("value", {})),
        resource_type=series.get("resource", {}).get("type"),
        metric_labels=dict(series.get("metric", {}).get("labels", {})),
        resource_labels=dict(series.get("resource", {}).get("labels", {})),
    )


def average_point_value(points: List[MetricPoint]) -> float:
    if not points:
        return 0.0
    return sum(point.value for point in points) / len(points)
