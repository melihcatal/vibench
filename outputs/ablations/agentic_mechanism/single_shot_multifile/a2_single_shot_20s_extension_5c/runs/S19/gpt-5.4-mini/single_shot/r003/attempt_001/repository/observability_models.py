from dataclasses import dataclass, field
from datetime import datetime, timezone
from statistics import mean
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple


def _iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")


def _dimension_selector(dimensions: Dict[str, str]) -> str:
    parts = [f'{k} = "{v}"' for k, v in sorted(dimensions.items())]
    return " AND ".join(parts)


@dataclass
class MetricSeriesRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    filter_expression: Optional[str] = None

    def to_filter(self, project_id: str) -> str:
        base = f'metric.type = "custom.googleapis.com/{self.metric_name}"'
        if self.filter_expression:
            return f"{base} AND {self.filter_expression}"
        return base


@dataclass
class MetricAggregateRequest(MetricSeriesRequest):
    aligner: str = "ALIGN_MEAN"
    reducer: Optional[str] = None
    alignment_period_seconds: int = 60


@dataclass
class DimensionFilterRequest(MetricSeriesRequest):
    dimensions: Dict[str, str] = field(default_factory=dict)

    def to_filter(self, project_id: str) -> str:
        base = super().to_filter(project_id)
        if self.dimensions:
            return f"{base} AND {_dimension_selector(self.dimensions)}"
        return base


@dataclass
class ComparisonRequest(MetricSeriesRequest):
    resource_a: Dict[str, str] = field(default_factory=dict)
    resource_b: Dict[str, str] = field(default_factory=dict)

    def to_filter(self, project_id: str, resource: Dict[str, str]) -> str:
        base = super().to_filter(project_id)
        if resource:
            return f"{base} AND {_dimension_selector(resource)}"
        return base


@dataclass
class MetricSeriesResponse:
    metric_name: str
    points: List[Dict[str, Any]]
    raw: Dict[str, Any]


@dataclass
class MetricAggregateResponse:
    metric_name: str
    statistics: Dict[str, float]
    raw: Dict[str, Any]


@dataclass
class ComparisonResponse:
    metric_name: str
    series_a: List[Dict[str, Any]]
    series_b: List[Dict[str, Any]]
    comparison: Dict[str, float]
    raw: Dict[str, Any]


def normalize_points(time_series: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    points: List[Dict[str, Any]] = []
    for series in time_series:
        metric = series.get("metric", {})
        for point in series.get("points", []):
            value = point.get("value", {})
            number = value.get("doubleValue")
            if number is None:
                number = value.get("int64Value")
            points.append({"metric": metric, "time": point.get("interval", {}).get("endTime"), "value": float(number) if number is not None else None})
    return points


def aggregate_points_from_series(time_series: Sequence[Dict[str, Any]]) -> Dict[str, float]:
    values: List[float] = []
    for point in normalize_points(time_series):
        if point["value"] is not None:
            values.append(float(point["value"]))
    if not values:
        return {"count": 0.0, "min": 0.0, "max": 0.0, "mean": 0.0}
    return {"count": float(len(values)), "min": float(min(values)), "max": float(max(values)), "mean": float(mean(values))}


def compare_point_lists(a: List[Dict[str, Any]], b: List[Dict[str, Any]]) -> Dict[str, float]:
    a_vals = [float(p["value"]) for p in a if p.get("value") is not None]
    b_vals = [float(p["value"]) for p in b if p.get("value") is not None]
    a_mean = mean(a_vals) if a_vals else 0.0
    b_mean = mean(b_vals) if b_vals else 0.0
    return {"mean_a": float(a_mean), "mean_b": float(b_mean), "delta": float(a_mean - b_mean), "ratio": float(a_mean / b_mean) if b_mean else 0.0}
