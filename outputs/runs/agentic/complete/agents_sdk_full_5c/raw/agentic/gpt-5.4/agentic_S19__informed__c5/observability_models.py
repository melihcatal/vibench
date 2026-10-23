from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from statistics import mean
from typing import Any, Dict, List, Optional


@dataclass
class MetricWindowRequest:
    project_id: str
    metric_type: str
    minutes: int = 15
    resource_type: Optional[str] = None
    alignment_period_seconds: int = 60


@dataclass
class DimensionFilterRequest:
    project_id: str
    metric_type: str
    minutes: int = 15
    resource_type: Optional[str] = None
    resource_labels: Dict[str, str] = field(default_factory=dict)
    metric_labels: Dict[str, str] = field(default_factory=dict)
    alignment_period_seconds: int = 60


@dataclass
class CompareMetricSeriesRequest:
    project_id: str
    metric_type: str
    minutes: int = 15
    left_resource_labels: Dict[str, str] = field(default_factory=dict)
    right_resource_labels: Dict[str, str] = field(default_factory=dict)
    resource_type: Optional[str] = None
    alignment_period_seconds: int = 60


@dataclass
class MetricPoint:
    timestamp: str
    value: float
    resource_labels: Dict[str, str] = field(default_factory=dict)
    metric_labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeries:
    metric_type: str
    points: List[MetricPoint]
    unit: Optional[str] = None


@dataclass
class MetricStatistics:
    metric_type: str
    count: int
    minimum: Optional[float]
    maximum: Optional[float]
    average: Optional[float]
    latest: Optional[float]



def _to_rfc3339(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")



def normalize_timestamp(ts: Any) -> str:
    if hasattr(ts, "timestamp"):
        dt = datetime.fromtimestamp(ts.timestamp(), tz=timezone.utc)
        return _to_rfc3339(dt)
    if isinstance(ts, datetime):
        return _to_rfc3339(ts)
    return str(ts)



def normalize_numeric_typed_value(typed_value: Any) -> Optional[float]:
    if typed_value is None:
        return None
    for attr in ("double_value", "int64_value", "bool_value"):
        if hasattr(typed_value, attr):
            value = getattr(typed_value, attr)
            if value is not None:
                if attr == "bool_value":
                    return 1.0 if bool(value) else 0.0
                return float(value)
    return None



def build_metric_point(point: Any, resource_labels: Optional[Dict[str, str]] = None, metric_labels: Optional[Dict[str, str]] = None) -> Optional[MetricPoint]:
    value = normalize_numeric_typed_value(getattr(point, "value", None))
    interval = getattr(point, "interval", None)
    end_time = getattr(interval, "end_time", None) if interval else None
    if value is None or end_time is None:
        return None
    return MetricPoint(
        timestamp=normalize_timestamp(end_time),
        value=value,
        resource_labels=resource_labels or {},
        metric_labels=metric_labels or {},
    )



def summarize_points(metric_type: str, points: List[MetricPoint]) -> MetricStatistics:
    if not points:
        return MetricStatistics(metric_type=metric_type, count=0, minimum=None, maximum=None, average=None, latest=None)
    values = [p.value for p in points]
    return MetricStatistics(
        metric_type=metric_type,
        count=len(values),
        minimum=min(values),
        maximum=max(values),
        average=mean(values),
        latest=points[0].value,
    )



def as_dict(obj: Any) -> Dict[str, Any]:
    if hasattr(obj, "__dict__"):
        return dict(obj.__dict__)
    if isinstance(obj, dict):
        return obj
    raise TypeError(f"Unsupported object type: {type(obj)!r}")
