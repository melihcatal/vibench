from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


RFC3339_ZULU = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class MetricWindowRequest:
    project_id: str
    metric_type: str
    minutes: int = 15
    alignment_period_seconds: int = 60
    resource_type: Optional[str] = None
    resource_labels: Dict[str, str] = field(default_factory=dict)
    metric_labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeriesPoint:
    timestamp: str
    value: float
    unit: Optional[str] = None
    metric_labels: Dict[str, str] = field(default_factory=dict)
    resource_labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeriesResponse:
    metric_type: str
    interval_start: str
    interval_end: str
    points: List[MetricSeriesPoint]


@dataclass
class AggregateStatsResponse:
    metric_type: str
    interval_start: str
    interval_end: str
    aggregation: str
    value: float
    sample_count: int


@dataclass
class ComparisonResult:
    metric_type: str
    interval_start: str
    interval_end: str
    left_label: str
    right_label: str
    left_points: List[MetricSeriesPoint]
    right_points: List[MetricSeriesPoint]
    left_average: float
    right_average: float
    difference: float


@dataclass
class MetricSummary:
    metric_type: str
    interval_start: str
    interval_end: str
    sample_count: int
    average: float
    minimum: float
    maximum: float
    trend: str
    anomaly_detected: bool
    anomaly_reason: Optional[str] = None


@dataclass
class ExportArchiveResult:
    bucket: str
    object_name: str
    generation: Optional[int]
    content_type: str
    size_bytes: int


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def format_rfc3339(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime(RFC3339_ZULU)


def parse_numeric_typed_value(typed_value: Any) -> float:
    if typed_value is None:
        return 0.0
    for attr in ("double_value", "int64_value", "bool_value"):
        if hasattr(typed_value, attr):
            value = getattr(typed_value, attr)
            if value not in (None, ""):
                return float(value)
    if hasattr(typed_value, "distribution_value") and typed_value.distribution_value:
        distribution = typed_value.distribution_value
        if getattr(distribution, "mean", None) is not None:
            return float(distribution.mean)
    return 0.0


def average(values: Iterable[float]) -> float:
    nums = list(values)
    return sum(nums) / len(nums) if nums else 0.0


def detect_trend(values: List[float]) -> str:
    if len(values) < 2:
        return "flat"
    if values[-1] > values[0]:
        return "up"
    if values[-1] < values[0]:
        return "down"
    return "flat"


def build_filter(metric_type: str, resource_type: Optional[str] = None, resource_labels: Optional[Dict[str, str]] = None, metric_labels: Optional[Dict[str, str]] = None) -> str:
    clauses = [f'metric.type = "{metric_type}"']
    if resource_type:
        clauses.append(f'resource.type = "{resource_type}"')
    for key, value in (resource_labels or {}).items():
        clauses.append(f'resource.labels.{key} = "{value}"')
    for key, value in (metric_labels or {}).items():
        clauses.append(f'metric.labels.{key} = "{value}"')
    return " AND ".join(clauses)
