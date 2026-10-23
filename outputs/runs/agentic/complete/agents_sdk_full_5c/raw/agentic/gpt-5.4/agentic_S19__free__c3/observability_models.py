from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from statistics import mean
from typing import Any, Dict, Iterable, List, Optional


RFC3339_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def ensure_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def to_rfc3339(dt: datetime) -> str:
    return ensure_utc(dt).strftime(RFC3339_FORMAT)


def parse_rfc3339(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value).astimezone(timezone.utc)


@dataclass
class MetricWindowRequest:
    project_id: str
    metric_type: str
    minutes: int = 60
    alignment_period_seconds: int = 60
    per_series_aligner: str = "ALIGN_MEAN"
    filter_text: Optional[str] = None


@dataclass
class MetricPoint:
    interval_end: datetime
    value: float
    metric_labels: Dict[str, str] = field(default_factory=dict)
    resource_labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricWindowResponse:
    metric_type: str
    points: List[MetricPoint]

    def values(self) -> List[float]:
        return [point.value for point in self.points]

    def avg(self) -> Optional[float]:
        vals = self.values()
        return mean(vals) if vals else None


@dataclass
class MetricStatsResponse:
    metric_type: str
    statistic: str
    value: Optional[float]
    samples: int


@dataclass
class MetricComparisonResult:
    left_label: str
    right_label: str
    left_average: Optional[float]
    right_average: Optional[float]
    delta: Optional[float]
    ratio: Optional[float]


@dataclass
class MetricSummaryResult:
    metric_type: str
    sample_count: int
    average: Optional[float]
    minimum: Optional[float]
    maximum: Optional[float]
    trend: str
    anomaly_detected: bool


def _typed_value_to_float(point_value: Dict[str, Any]) -> Optional[float]:
    if "doubleValue" in point_value:
        return float(point_value["doubleValue"])
    if "int64Value" in point_value:
        return float(point_value["int64Value"])
    if "distributionValue" in point_value:
        distribution = point_value["distributionValue"]
        count = float(distribution.get("count", 0) or 0)
        mean_value = float(distribution.get("mean", 0.0) or 0.0)
        return mean_value if count else 0.0
    return None


def normalize_time_series_points(time_series: Iterable[Dict[str, Any]]) -> List[MetricPoint]:
    normalized: List[MetricPoint] = []
    for series in time_series:
        metric_labels = dict(series.get("metric", {}).get("labels", {}))
        resource_labels = dict(series.get("resource", {}).get("labels", {}))
        for point in series.get("points", []):
            value = _typed_value_to_float(point.get("value", {}))
            if value is None:
                continue
            interval_end = parse_rfc3339(point["interval"]["endTime"])
            normalized.append(
                MetricPoint(
                    interval_end=interval_end,
                    value=value,
                    metric_labels=metric_labels,
                    resource_labels=resource_labels,
                )
            )
    normalized.sort(key=lambda item: item.interval_end)
    return normalized
