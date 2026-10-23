from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class MetricQuery:
    metric: str
    start_time: float
    end_time: float
    dimensions: Dict[str, str]
    period_seconds: int
    statistics: List[str]


@dataclass
class MetricSeries:
    points: List[Dict[str, float]]
    statistics: List[str]
    metric: str


def normalize_dimensions(dimensions: Optional[Dict[str, str]]) -> Dict[str, str]:
    return {str(k): str(v) for k, v in (dimensions or {}).items()}


def normalize_points(points: List[Dict[str, Any]]) -> List[Dict[str, float]]:
    normalized = []
    for point in points:
        normalized.append({"timestamp": float(point["timestamp"]), "value": float(point["value"])})
    return sorted(normalized, key=lambda p: p["timestamp"])
