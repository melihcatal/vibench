from dataclasses import dataclass
from datetime import datetime
from statistics import mean
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class MetricQueryRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    dimensions: Dict[str, str]


@dataclass(frozen=True)
class MetricWindowResult:
    request: MetricQueryRequest
    series: List[Dict[str, Any]]


@dataclass(frozen=True)
class MetricAggregateResult:
    request: MetricQueryRequest
    stats: Dict[str, float]


@dataclass(frozen=True)
class ComparisonResult:
    request: MetricQueryRequest
    left: Dict[str, float]
    right: Dict[str, float]
    difference: float


def normalize_points(points: Iterable[Any]) -> List[Dict[str, Any]]:
    normalized = []
    for point in points:
        value = None
        if getattr(point, "value", None) is not None:
            for field in ("double_value", "int64_value", "distribution_value"):
                if hasattr(point.value, field):
                    value = getattr(point.value, field)
                    break
        normalized.append({"interval_end": getattr(getattr(point, "interval", None), "end_time", None), "value": value})
    return normalized


def summarize_series(points: List[Dict[str, Any]]) -> Dict[str, float]:
    values = [float(p["value"]) for p in points if p.get("value") is not None and isinstance(p["value"], (int, float))]
    if not values:
        return {"count": 0.0, "mean": 0.0, "min": 0.0, "max": 0.0}
    return {"count": float(len(values)), "mean": float(mean(values)), "min": float(min(values)), "max": float(max(values))}


def aggregate_points(points: List[Dict[str, Any]]) -> Dict[str, float]:
    return summarize_series(points)
