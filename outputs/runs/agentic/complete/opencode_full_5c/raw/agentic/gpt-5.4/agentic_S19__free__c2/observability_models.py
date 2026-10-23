from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def ensure_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def isoformat_z(dt: datetime) -> str:
    return ensure_utc(dt).isoformat().replace("+00:00", "Z")


@dataclass
class MetricWindowRequest:
    project_id: str
    metric_type: str
    start_time: datetime
    end_time: datetime
    alignment_period_seconds: int = 60
    per_series_aligner: str = "ALIGN_MEAN"
    resource_type: Optional[str] = None
    filter_clauses: List[str] = field(default_factory=list)
    page_size: int = 100

    def build_filter(self) -> str:
        clauses = [f'metric.type = "{self.metric_type}"']
        if self.resource_type:
            clauses.append(f'resource.type = "{self.resource_type}"')
        clauses.extend(self.filter_clauses)
        return " AND ".join(clauses)


@dataclass
class MetricPoint:
    interval_end: str
    value: float
    series_name: Optional[str] = None
    resource_labels: Dict[str, str] = field(default_factory=dict)
    metric_labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeries:
    series_name: str
    resource_type: str
    metric_type: str
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]
    points: List[MetricPoint]


@dataclass
class MetricWindowResponse:
    project_id: str
    metric_type: str
    start_time: str
    end_time: str
    series: List[MetricSeries]


@dataclass
class AggregatedMetricStats:
    metric_type: str
    start_time: str
    end_time: str
    point_count: int
    min_value: Optional[float]
    max_value: Optional[float]
    mean_value: Optional[float]
    sum_value: Optional[float]


@dataclass
class MetricComparisonResult:
    metric_type: str
    left_filter: str
    right_filter: str
    start_time: str
    end_time: str
    left_mean: Optional[float]
    right_mean: Optional[float]
    absolute_delta: Optional[float]
    percent_delta: Optional[float]


def numeric_typed_value(point_value: Any) -> Optional[float]:
    if point_value is None:
        return None
    for field_name in ("double_value", "int64_value", "distribution_value"):
        if hasattr(point_value, field_name):
            value = getattr(point_value, field_name)
            if field_name == "distribution_value" and value is not None:
                if (
                    getattr(value, "count", 0)
                    and getattr(value, "mean", None) is not None
                ):
                    return float(value.mean)
                return None
            if value is not None:
                return float(value)
    return None


def labels_dict(label_obj: Any) -> Dict[str, str]:
    if label_obj is None:
        return {}
    if hasattr(label_obj, "labels"):
        return {str(k): str(v) for k, v in dict(label_obj.labels).items()}
    if isinstance(label_obj, dict):
        return {str(k): str(v) for k, v in label_obj.items()}
    return {}


def series_to_model(series: Any) -> MetricSeries:
    points: List[MetricPoint] = []
    for point in getattr(series, "points", []):
        value = numeric_typed_value(getattr(point, "value", None))
        if value is None:
            continue
        interval = getattr(point, "interval", None)
        interval_end = ""
        if interval is not None and getattr(interval, "end_time", None) is not None:
            end_time = interval.end_time
            if hasattr(end_time, "ToDatetime"):
                interval_end = isoformat_z(end_time.ToDatetime())
        points.append(
            MetricPoint(
                interval_end=interval_end,
                value=value,
                series_name=getattr(series, "name", None),
                resource_labels=labels_dict(getattr(series, "resource", None)),
                metric_labels=labels_dict(getattr(series, "metric", None)),
            )
        )
    resource = getattr(series, "resource", None)
    metric = getattr(series, "metric", None)
    return MetricSeries(
        series_name=getattr(series, "name", ""),
        resource_type=getattr(resource, "type", ""),
        metric_type=getattr(metric, "type", ""),
        resource_labels=labels_dict(resource),
        metric_labels=labels_dict(metric),
        points=points,
    )


def flatten_values(series_list: List[MetricSeries]) -> List[float]:
    values: List[float] = []
    for series in series_list:
        values.extend(point.value for point in series.points)
    return values
