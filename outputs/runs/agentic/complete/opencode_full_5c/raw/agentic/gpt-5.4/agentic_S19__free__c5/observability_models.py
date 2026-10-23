from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _to_rfc3339(value: datetime | str) -> str:
    if isinstance(value, str):
        return value
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass
class MetricWindowRequest:
    metric_type: str
    start_time: datetime | str
    end_time: datetime | str
    project_id: Optional[str] = None
    alignment_period_seconds: int = 300
    per_series_aligner: str = "ALIGN_MEAN"
    filter_expression: Optional[str] = None
    view: str = "FULL"

    def start_rfc3339(self) -> str:
        return _to_rfc3339(self.start_time)

    def end_rfc3339(self) -> str:
        return _to_rfc3339(self.end_time)


@dataclass
class MetricDimensionsRequest(MetricWindowRequest):
    resource_type: Optional[str] = None
    metric_labels: Dict[str, str] = field(default_factory=dict)
    resource_labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricPoint:
    series_name: str
    timestamp: str
    value: float
    unit: Optional[str] = None
    metric_labels: Dict[str, str] = field(default_factory=dict)
    resource_labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeries:
    series_name: str
    metric_type: str
    resource_type: Optional[str]
    metric_labels: Dict[str, str]
    resource_labels: Dict[str, str]
    points: List[MetricPoint]


@dataclass
class MetricStatistics:
    metric_type: str
    start_time: str
    end_time: str
    count: int
    minimum: Optional[float]
    maximum: Optional[float]
    average: Optional[float]
    sum: Optional[float]


@dataclass
class MetricComparison:
    metric_type: str
    left_filter: str
    right_filter: str
    left_average: Optional[float]
    right_average: Optional[float]
    absolute_difference: Optional[float]
    percent_difference: Optional[float]


@dataclass
class MetricSummary:
    metric_type: str
    trend: str
    anomaly_detected: bool
    latest_value: Optional[float]
    baseline_average: Optional[float]
    message: str


def normalize_numeric_typed_value(value: Dict[str, Any]) -> Optional[float]:
    if not value:
        return None
    if "doubleValue" in value:
        return float(value["doubleValue"])
    if "int64Value" in value:
        return float(value["int64Value"])
    if "boolValue" in value:
        return 1.0 if value["boolValue"] else 0.0
    if "distributionValue" in value:
        distribution = value["distributionValue"]
        count = float(distribution.get("count", 0) or 0)
        mean = distribution.get("mean")
        if mean is not None:
            return float(mean)
        return count
    return None


def build_filter(
    metric_type: str,
    resource_type: Optional[str] = None,
    metric_labels: Optional[Dict[str, str]] = None,
    resource_labels: Optional[Dict[str, str]] = None,
    extra_filter: Optional[str] = None,
) -> str:
    clauses = [f'metric.type = "{metric_type}"']
    if resource_type:
        clauses.append(f'resource.type = "{resource_type}"')
    for key, value in (metric_labels or {}).items():
        clauses.append(f'metric.labels.{key} = "{value}"')
    for key, value in (resource_labels or {}).items():
        clauses.append(f'resource.labels.{key} = "{value}"')
    if extra_filter:
        clauses.append(f"({extra_filter})")
    return " AND ".join(clauses)
