from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from statistics import mean
from typing import Any, Dict, List, Optional


RFC3339_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class MetricWindowRequest:
    project_id: str
    metric_type: str
    minutes: int = 15
    alignment_period_seconds: int = 60
    per_series_aligner: str = "ALIGN_MEAN"
    resource_type: Optional[str] = None
    resource_labels: Dict[str, str] = field(default_factory=dict)
    metric_labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricPoint:
    interval_end: str
    value: float
    resource_labels: Dict[str, str] = field(default_factory=dict)
    metric_labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeriesResult:
    metric_type: str
    points: List[MetricPoint]
    unit: Optional[str] = None


@dataclass
class AggregateStats:
    metric_type: str
    count: int
    minimum: Optional[float]
    maximum: Optional[float]
    average: Optional[float]
    sum_value: Optional[float]


@dataclass
class ComparisonResult:
    left_label: str
    right_label: str
    left_average: Optional[float]
    right_average: Optional[float]
    delta: Optional[float]
    ratio: Optional[float]


@dataclass
class TrendSummary:
    metric_type: str
    point_count: int
    latest_value: Optional[float]
    average_value: Optional[float]
    min_value: Optional[float]
    max_value: Optional[float]
    trend: str
    anomaly_detected: bool


@dataclass
class ExportArchiveResult:
    bucket: str
    object_name: str
    generation: Optional[int]
    size: int
    content_type: str


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def to_rfc3339(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime(RFC3339_FORMAT)


def numeric_value_from_point(point: Dict[str, Any]) -> float:
    value = point.get("value", {})
    for key in ("doubleValue", "int64Value"):
        if key in value:
            return float(value[key])
    if "distributionValue" in value:
        distribution = value["distributionValue"]
        return float(distribution.get("mean", 0.0))
    raise ValueError("Unsupported Monitoring point value payload")


def extract_labels(series: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    resource = series.get("resource", {})
    metric = series.get("metric", {})
    return {
        "resource_labels": resource.get("labels", {}) or {},
        "metric_labels": metric.get("labels", {}) or {},
    }


def normalize_time_series(metric_type: str, series_list: List[Dict[str, Any]]) -> MetricSeriesResult:
    points: List[MetricPoint] = []
    unit: Optional[str] = None
    for series in series_list:
        labels = extract_labels(series)
        unit = unit or series.get("unit")
        for point in series.get("points", []):
            points.append(
                MetricPoint(
                    interval_end=point.get("interval", {}).get("endTime", ""),
                    value=numeric_value_from_point(point),
                    resource_labels=labels["resource_labels"],
                    metric_labels=labels["metric_labels"],
                )
            )
    points.sort(key=lambda item: item.interval_end)
    return MetricSeriesResult(metric_type=metric_type, points=points, unit=unit)


def compute_aggregate_stats(metric_type: str, points: List[MetricPoint]) -> AggregateStats:
    if not points:
        return AggregateStats(metric_type=metric_type, count=0, minimum=None, maximum=None, average=None, sum_value=None)
    values = [point.value for point in points]
    return AggregateStats(
        metric_type=metric_type,
        count=len(values),
        minimum=min(values),
        maximum=max(values),
        average=mean(values),
        sum_value=sum(values),
    )


def summarize_trend(metric_type: str, points: List[MetricPoint]) -> TrendSummary:
    stats = compute_aggregate_stats(metric_type, points)
    latest_value = points[-1].value if points else None
    trend = "flat"
    anomaly_detected = False
    if len(points) >= 2:
        start = points[0].value
        end = points[-1].value
        if end > start:
            trend = "up"
        elif end < start:
            trend = "down"
        avg = stats.average or 0.0
        if avg != 0.0 and abs(end - avg) / abs(avg) > 0.5:
            anomaly_detected = True
    return TrendSummary(
        metric_type=metric_type,
        point_count=stats.count,
        latest_value=latest_value,
        average_value=stats.average,
        min_value=stats.minimum,
        max_value=stats.maximum,
        trend=trend,
        anomaly_detected=anomaly_detected,
    )
