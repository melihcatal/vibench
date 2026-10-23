from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class MetricWindowRequest:
    metric_name: str
    start_time: str
    end_time: str
    resource_filter: Optional[Dict[str, str]] = None


@dataclass
class MetricResult:
    metric_name: str
    points: List[Dict[str, Any]]
    summary: Dict[str, Any]


def normalize_points(points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for point in points:
        normalized.append({k: point.get(k) for k in sorted(point.keys())})
    return normalized


def make_metric_result(metric_name: str, points: List[Dict[str, Any]], summary: Optional[Dict[str, Any]] = None) -> MetricResult:
    return MetricResult(metric_name=metric_name, points=normalize_points(points), summary=summary or {})
