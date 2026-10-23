from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def isoformat(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_dimensions(dimensions: Optional[Dict[str, str]] = None, labels: Optional[Dict[str, str]] = None) -> List[Dict[str, str]]:
    data = dimensions if dimensions is not None else labels or {}
    return [{"Name": str(k), "Value": str(v)} for k, v in data.items()]


def normalize_datapoints(datapoints: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    items = []
    for point in datapoints:
        item = dict(point)
        ts = item.get("Timestamp")
        if hasattr(ts, "astimezone"):
            item["Timestamp"] = isoformat(ts)
        items.append(item)
    return items


@dataclass
class MetricWindowRequest:
    namespace: str
    metric_name: str
    start_time: datetime
    end_time: datetime
    period: int = 60
    statistics: Optional[List[str]] = None
    dimensions: Optional[Dict[str, str]] = None


@dataclass
class MetricWindowResponse:
    namespace: str
    metric_name: str
    start_time: str
    end_time: str
    period: int
    statistics: List[str]
    datapoints: List[Dict[str, Any]]
