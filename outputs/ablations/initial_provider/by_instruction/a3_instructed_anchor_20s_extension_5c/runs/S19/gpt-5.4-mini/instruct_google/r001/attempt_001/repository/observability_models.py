from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _to_iso(ts: datetime) -> str:
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    return ts.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_dimensions(dimensions: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not dimensions:
        return {}
    return {str(k): str(v) for k, v in dimensions.items() if v is not None}


@dataclass
class MetricWindowRequest:
    metric_type: str
    start_time: datetime
    end_time: datetime
    interval_seconds: int = 60
    dimensions: Optional[Dict[str, Any]] = None

    def to_google_filter(self) -> str:
        parts = [f'metric.type = "{self.metric_type}"']
        for key, value in normalize_dimensions(self.dimensions).items():
            parts.append(f'resource.labels."{key}" = "{value}"')
        return " AND ".join(parts)

    def to_google_interval(self) -> Dict[str, str]:
        return {"startTime": _to_iso(self.start_time), "endTime": _to_iso(self.end_time)}


@dataclass
class MetricPoint:
    value: Any
    timestamp: Optional[str] = None
    labels: Optional[Dict[str, Any]] = None


def parse_timeseries(timeseries: List[Dict[str, Any]]) -> List[MetricPoint]:
    points: List[MetricPoint] = []
    for series in timeseries:
        labels = series.get("metric", {}).get("labels") or series.get("resource", {}).get("labels")
        for point in series.get("points", []):
            points.append(MetricPoint(value=point.get("value"), timestamp=point.get("interval", {}).get("endTime"), labels=labels))
    return points
