from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class MetricWindowRequest:
    metric_name: str
    start: datetime
    end: datetime
    query: Optional[str] = None


@dataclass
class MetricSeries:
    name: str
    points: List[Dict[str, Any]]
    tags: List[str]


def isoformat(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat() + "Z"


def normalize_points(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    series = payload.get("series", [])
    points: List[Dict[str, Any]] = []
    for item in series:
        for point in item.get("pointlist", []):
            points.append(
                {"timestamp": point[0], "value": point[1], "tags": item.get("tags", [])}
            )
    return points
