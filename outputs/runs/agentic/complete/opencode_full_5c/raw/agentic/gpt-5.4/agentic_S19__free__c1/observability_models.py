from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def isoformat_utc(value: datetime) -> str:
    return _ensure_utc(value).isoformat().replace("+00:00", "Z")


def parse_rfc3339(value: str) -> datetime:
    normalized = value.replace("Z", "+00:00")
    return _ensure_utc(datetime.fromisoformat(normalized))


@dataclass
class MetricWindowRequest:
    project_id: str
    metric_type: str
    start_time: datetime
    end_time: datetime
    alignment_period_seconds: int = 300
    per_series_aligner: str = "ALIGN_MEAN"
    cross_series_reducer: Optional[str] = None
    group_by_fields: List[str] = field(default_factory=list)
    resource_type: Optional[str] = None
    resource_labels: Dict[str, str] = field(default_factory=dict)
    metric_labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricPoint:
    interval_end: datetime
    value: Optional[float]
    unit: Optional[str]
    metric_labels: Dict[str, str]
    resource_labels: Dict[str, str]


@dataclass
class MetricSeries:
    metric_type: str
    resource_type: str
    metric_labels: Dict[str, str]
    resource_labels: Dict[str, str]
    points: List[MetricPoint]


@dataclass
class AggregateStats:
    metric_type: str
    window_start: datetime
    window_end: datetime
    series_count: int
    point_count: int
    minimum: Optional[float]
    maximum: Optional[float]
    average: Optional[float]
    total: Optional[float]
    latest: Optional[float]
    unit: Optional[str]


@dataclass
class MetricComparison:
    left_label: str
    right_label: str
    window_start: datetime
    window_end: datetime
    left_latest: Optional[float]
    right_latest: Optional[float]
    absolute_delta: Optional[float]
    percent_delta: Optional[float]
    unit: Optional[str]


@dataclass
class MetricSummary:
    metric_type: str
    window_start: datetime
    window_end: datetime
    average: Optional[float]
    latest: Optional[float]
    trend: str
    anomaly_detected: bool
    summary_text: str


def extract_numeric_value(point_value: Dict[str, Any]) -> Optional[float]:
    if not point_value:
        return None
    for key in ("doubleValue", "int64Value"):
        if key in point_value:
            return float(point_value[key])
    if "distributionValue" in point_value:
        distribution = point_value["distributionValue"] or {}
        count = float(distribution.get("count", 0) or 0)
        mean = distribution.get("mean")
        if mean is not None:
            return float(mean)
        if count:
            return count
    return None


def normalize_time_series(series: Dict[str, Any]) -> MetricSeries:
    metric = series.get("metric", {})
    resource = series.get("resource", {})
    unit = series.get("unit")
    points = []
    for point in series.get("points", []):
        interval = point.get("interval", {})
        points.append(
            MetricPoint(
                interval_end=parse_rfc3339(interval["endTime"]),
                value=extract_numeric_value(point.get("value", {})),
                unit=unit,
                metric_labels=dict(metric.get("labels", {})),
                resource_labels=dict(resource.get("labels", {})),
            )
        )
    return MetricSeries(
        metric_type=metric.get("type", ""),
        resource_type=resource.get("type", ""),
        metric_labels=dict(metric.get("labels", {})),
        resource_labels=dict(resource.get("labels", {})),
        points=points,
    )


def flatten_values(series_list: List[MetricSeries]) -> List[float]:
    values: List[float] = []
    for series in series_list:
        for point in series.points:
            if point.value is not None:
                values.append(point.value)
    return values


def compute_stats(
    metric_type: str,
    start_time: datetime,
    end_time: datetime,
    series_list: List[MetricSeries],
) -> AggregateStats:
    values = flatten_values(series_list)
    unit = None
    latest = None
    latest_ts = None
    point_count = 0
    for series in series_list:
        for point in series.points:
            point_count += 1
            if unit is None:
                unit = point.unit
            if point.value is not None and (
                latest_ts is None or point.interval_end > latest_ts
            ):
                latest_ts = point.interval_end
                latest = point.value
    average = sum(values) / len(values) if values else None
    total = sum(values) if values else None
    minimum = min(values) if values else None
    maximum = max(values) if values else None
    return AggregateStats(
        metric_type=metric_type,
        window_start=_ensure_utc(start_time),
        window_end=_ensure_utc(end_time),
        series_count=len(series_list),
        point_count=point_count,
        minimum=minimum,
        maximum=maximum,
        average=average,
        total=total,
        latest=latest,
        unit=unit,
    )
