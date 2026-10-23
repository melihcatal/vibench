from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class MetricQuery:
    metric_namespace: str
    metric_name: str
    start_time: str
    end_time: str
    aggregation: Optional[str] = None
    filter_expression: Optional[str] = None
    resource_id: Optional[str] = None


@dataclass
class MetricPoint:
    timestamp: str
    value: float
    dimensions: Dict[str, Any]


@dataclass
class MetricSeries:
    metric_name: str
    metric_namespace: str
    points: List[MetricPoint]
    summary: Dict[str, Any]


def normalize_metric_point(payload: Dict[str, Any]) -> MetricPoint:
    return MetricPoint(
        timestamp=str(payload.get("timestamp") or payload.get("time") or ""),
        value=float(payload.get("value") or payload.get("count") or 0.0),
        dimensions=dict(payload.get("dimensions") or payload.get("labels") or {}),
    )


def normalize_series(payload: Dict[str, Any]) -> MetricSeries:
    points = [normalize_metric_point(item) for item in payload.get("points", [])]
    return MetricSeries(
        metric_name=str(payload.get("metric_name") or payload.get("name") or ""),
        metric_namespace=str(payload.get("metric_namespace") or payload.get("namespace") or ""),
        points=points,
        summary=dict(payload.get("summary") or {}),
    )
