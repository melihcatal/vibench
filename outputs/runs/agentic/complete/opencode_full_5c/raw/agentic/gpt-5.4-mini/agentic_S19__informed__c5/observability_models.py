from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def normalize_time(value: Any) -> str:
    if value is None:
        return datetime.now(timezone.utc).isoformat()
    if isinstance(value, datetime):
        dt = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    return str(value)


def normalize_dimensions(dimensions: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not dimensions:
        return {}
    return {str(k): str(v) for k, v in dimensions.items() if v is not None}


@dataclass
class MetricWindowRequest:
    metric_name: str
    start_time: Any
    end_time: Any
    dimensions: Optional[Dict[str, Any]] = None


@dataclass
class MetricAggregationRequest:
    metric_name: str
    start_time: Any
    end_time: Any
    aggregation: str = "avg"
    dimensions: Optional[Dict[str, Any]] = None


@dataclass
class MetricComparisonRequest:
    metric_name: str
    start_time: Any
    end_time: Any
    left_dimensions: Optional[Dict[str, Any]] = None
    right_dimensions: Optional[Dict[str, Any]] = None


def metric_query_payload(
    metric_name: str,
    start_time: Any,
    end_time: Any,
    dimensions: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    return {
        "metric": metric_name,
        "start_time": normalize_time(start_time),
        "end_time": normalize_time(end_time),
        "dimensions": normalize_dimensions(dimensions),
    }


def extract_metric_points(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    series = payload.get("data", payload.get("series", []))
    if isinstance(series, dict):
        series = [series]
    points: List[Dict[str, Any]] = []
    for item in series or []:
        if isinstance(item, dict):
            points.extend(item.get("points", item.get("datapoints", [])) or [])
    return points
