from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class MetricWindowRequest:
    metric: str
    start: int
    end: int
    interval: Optional[int] = None
    tags: Optional[List[str]] = None


@dataclass
class MetricSeriesPoint:
    timestamp: int
    value: float


def normalize_points(payload: Dict[str, Any]) -> List[MetricSeriesPoint]:
    points = []
    for item in payload.get("series", []):
        for ts, value in item.get("pointlist", []):
            if value is not None:
                points.append(
                    MetricSeriesPoint(timestamp=int(ts / 1000), value=float(value))
                )
    return points


def serialize_request(request: MetricWindowRequest) -> Dict[str, Any]:
    data = asdict(request)
    return {k: v for k, v in data.items() if v is not None}
