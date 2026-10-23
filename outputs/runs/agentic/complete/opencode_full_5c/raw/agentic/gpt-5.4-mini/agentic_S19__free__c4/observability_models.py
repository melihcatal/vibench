from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def normalize_time(value: Any) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, datetime):
        return int(value.replace(tzinfo=timezone.utc).timestamp())
    if isinstance(value, str):
        return int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp())
    raise ValueError("unsupported time value")


def normalize_points(points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for point in points:
        normalized.append(
            {
                "ts": normalize_time(
                    point.get("ts") or point.get("time") or point.get("timestamp")
                ),
                "value": point.get("value"),
            }
        )
    return normalized


@dataclass
class MetricWindowRequest:
    metric: str
    start: int
    end: int
    scope: Optional[str] = None
    tags: Optional[List[str]] = None


@dataclass
class MetricSeriesComparison:
    left: List[Dict[str, Any]]
    right: List[Dict[str, Any]]
    delta: List[Dict[str, Any]]
