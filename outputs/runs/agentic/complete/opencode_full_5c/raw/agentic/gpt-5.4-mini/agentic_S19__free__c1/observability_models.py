from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional


def parse_iso8601(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def to_iso8601(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def normalize_dimensions(dimensions: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not dimensions:
        return {}
    return {str(k): str(v) for k, v in dimensions.items() if v is not None}


def normalize_points(points: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for point in points:
        item = dict(point)
        ts = item.get("timestamp") or item.get("time")
        if isinstance(ts, datetime):
            item["timestamp"] = to_iso8601(ts)
        elif isinstance(ts, str):
            item["timestamp"] = ts
        value = item.get("value")
        if value is not None:
            item["value"] = float(value)
        normalized.append(item)
    return normalized


@dataclass
class MetricWindowRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    dimensions: Optional[Dict[str, str]] = None


@dataclass
class MetricSeriesComparisonRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    left_dimensions: Optional[Dict[str, str]] = None
    right_dimensions: Optional[Dict[str, str]] = None
