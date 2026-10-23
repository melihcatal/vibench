from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


def _iso(dt: Any) -> Any:
    if isinstance(dt, datetime):
        return dt.isoformat()
    return dt


def normalize_metric_points(points: Any) -> List[Dict[str, Any]]:
    if points is None:
        return []
    normalized = []
    for point in points:
        if isinstance(point, dict):
            normalized.append({k: _iso(v) for k, v in point.items()})
        elif hasattr(point, "__dict__"):
            normalized.append({k: _iso(v) for k, v in vars(point).items()})
        else:
            normalized.append({"value": point})
    return normalized


@dataclass
class MetricWindowRequest:
    resource: str
    metric_name: str
    start_time: Any
    end_time: Any
    granularity: Optional[str] = None
    aggregation: Optional[str] = None
    dimensions: Optional[Dict[str, str]] = None


@dataclass
class MetricSeriesRequest:
    resource_a: str
    resource_b: str
    metric_name: str
    start_time: Any
    end_time: Any
    dimensions_a: Optional[Dict[str, str]] = None
    dimensions_b: Optional[Dict[str, str]] = None


def serialize_request(payload: Any) -> Dict[str, Any]:
    if hasattr(payload, "__dict__"):
        data = dict(vars(payload))
    elif isinstance(payload, dict):
        data = dict(payload)
    else:
        data = {"value": payload}
    return {k: _iso(v) for k, v in data.items() if v is not None}
