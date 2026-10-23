import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional


def isoformat_utc(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat()


def parse_iso8601(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def window_start(minutes: int = 60) -> datetime:
    return datetime.now(timezone.utc) - timedelta(minutes=minutes)


def normalize_dimensions(dimensions: Optional[Dict[str, str]] = None) -> List[Dict[str, str]]:
    items = dimensions or {}
    return [{"Name": str(k), "Value": str(v)} for k, v in sorted(items.items())]


@dataclass
class MetricWindowRequest:
    namespace: str
    metric_name: str
    start_time: datetime
    end_time: datetime
    period: int = 60
    statistics: List[str] = field(default_factory=lambda: ["Average"])
    dimensions: Dict[str, str] = field(default_factory=dict)
    unit: Optional[str] = None


@dataclass
class MetricSeriesPoint:
    timestamp: str
    value: float
    statistic: str


@dataclass
class MetricWindowResponse:
    namespace: str
    metric_name: str
    points: List[MetricSeriesPoint]
    raw: Dict[str, Any]


def parse_metric_data_results(results: List[Dict[str, Any]]) -> MetricWindowResponse:
    points: List[MetricSeriesPoint] = []
    namespace = ""
    metric_name = ""
    raw: Dict[str, Any] = {"MetricDataResults": results}
    for result in results:
        if not metric_name:
            metric_name = str(result.get("Label", ""))
        timestamps = result.get("Timestamps", []) or []
        values = result.get("Values", []) or []
        stat = str(result.get("Id", ""))
        for ts, val in zip(timestamps, values):
            if isinstance(ts, datetime):
                ts = isoformat_utc(ts)
            points.append(MetricSeriesPoint(timestamp=str(ts), value=float(val), statistic=stat))
    return MetricWindowResponse(namespace=namespace, metric_name=metric_name, points=points, raw=raw)


def dumps(obj: Any) -> str:
    return json.dumps(obj, default=str, sort_keys=True)
