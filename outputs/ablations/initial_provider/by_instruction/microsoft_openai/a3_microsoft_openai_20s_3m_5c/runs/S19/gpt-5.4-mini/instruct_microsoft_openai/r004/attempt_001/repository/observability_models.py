from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


def _parse_iso8601(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def normalize_points(points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for point in points:
        item = dict(point)
        ts = item.get("timestamp") or item.get("time")
        if isinstance(ts, str):
            try:
                item["timestamp"] = _parse_iso8601(ts)
            except Exception:
                item["timestamp"] = ts
        normalized.append(item)
    return normalized


@dataclass
class MetricWindowRequest:
    metric_name: str
    start_time: str
    end_time: str
    resource_filter: Optional[Dict[str, str]] = None
    aggregation: Optional[str] = None


@dataclass
class MetricResponse:
    metric_name: str
    points: List[Dict[str, Any]]
    statistics: Optional[Dict[str, Any]] = None
    source: Optional[str] = None
