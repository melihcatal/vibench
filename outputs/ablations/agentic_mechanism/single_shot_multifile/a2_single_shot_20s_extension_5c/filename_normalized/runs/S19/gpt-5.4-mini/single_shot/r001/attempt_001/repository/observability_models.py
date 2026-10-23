from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from statistics import mean
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence


@dataclass
class MetricWindowQuery:
    metric_name: str
    start_time: datetime
    end_time: datetime
    resource_type: Optional[str]
    points: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "resource_type": self.resource_type,
            "points": self.points,
        }


@dataclass
class AggregateMetricStats:
    metric_name: str
    start_time: datetime
    end_time: datetime
    resource_type: Optional[str]
    point_count: int
    min_value: Optional[float]
    max_value: Optional[float]
    mean_value: Optional[float]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "resource_type": self.resource_type,
            "point_count": self.point_count,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "mean_value": self.mean_value,
        }


@dataclass
class DimensionFilteredMetric:
    metric_name: str
    start_time: datetime
    end_time: datetime
    dimensions: Dict[str, str]
    series: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "dimensions": self.dimensions,
            "series": self.series,
        }


def _extract_numeric(point: Any) -> Optional[float]:
    value = getattr(point, "value", None)
    if value is None:
        return None
    for attr in ("double_value", "int64_value", "distribution_value"):
        v = getattr(value, attr, None)
        if v is not None and attr != "distribution_value":
            return float(v)
    return None


def normalize_points(series: Iterable[Any]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for ts in series:
        metric = getattr(ts, "metric", None)
        resource = getattr(ts, "resource", None)
        for point in getattr(ts, "points", []):
            interval = getattr(point, "interval", None)
            normalized.append(
                {
                    "metric": dict(metric.labels) if metric and getattr(metric, "labels", None) else {},
                    "resource": dict(resource.labels) if resource and getattr(resource, "labels", None) else {},
                    "end_time": getattr(getattr(interval, "end_time", None), "isoformat", lambda: None)(),
                    "value": _extract_numeric(point),
                }
            )
    return normalized


def normalize_points_with_dimensions(series: Iterable[Any]) -> List[Dict[str, Any]]:
    return normalize_points(series)


def summarize_time_series(series: Iterable[Any]) -> Dict[str, Any]:
    values: List[float] = []
    count = 0
    for ts in series:
        for point in getattr(ts, "points", []):
            count += 1
            numeric = _extract_numeric(point)
            if numeric is not None:
                values.append(numeric)
    return {
        "point_count": count,
        "min_value": min(values) if values else None,
        "max_value": max(values) if values else None,
        "mean_value": mean(values) if values else None,
    }


def compare_series(metric_name: str, start_time: datetime, end_time: datetime, left_series: Iterable[Any], right_series: Iterable[Any], left_filter: Mapping[str, str], right_filter: Mapping[str, str]) -> Dict[str, Any]:
    left = summarize_time_series(left_series)
    right = summarize_time_series(right_series)
    return {
        "metric_name": metric_name,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "left_filter": dict(left_filter),
        "right_filter": dict(right_filter),
        "left": left,
        "right": right,
    }
