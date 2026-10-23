from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


def normalize_rfc3339(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    if value.endswith("Z"):
        return value[:-1] + "+00:00"
    return value


def to_rfc3339(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat().replace("+00:00", "Z")


@dataclass
class MetricWindowRequest:
    metric_type: str
    start_time: str
    end_time: str
    filter_expr: Optional[str] = None
    project: Optional[str] = None

    def to_params(self) -> Dict[str, Any]:
        params = {"filter": self.filter_expr or f'metric.type="{self.metric_type}"'}
        return params


@dataclass
class MetricAggregateRequest(MetricWindowRequest):
    aggregation: Optional[str] = None


@dataclass
class MetricSeriesComparisonRequest:
    metric_type: str
    start_time: str
    end_time: str
    filter_a: str
    filter_b: str
    project: Optional[str] = None


@dataclass
class MetricSeriesPoint:
    timestamp: str
    value: float
    labels: Dict[str, str]


@dataclass
class MetricSeriesResponse:
    points: List[MetricSeriesPoint]
    raw: Dict[str, Any]

    @classmethod
    def from_response(cls, payload: Dict[str, Any]) -> "MetricSeriesResponse":
        points = []
        for item in payload.get("timeSeries", payload.get("data", [])):
            pts = item.get("points", [])
            if pts:
                point = pts[0]
                ts = point.get("interval", {}).get("endTime", "")
                val = point.get("value", {}).get("doubleValue", point.get("value", {}).get("int64Value", 0))
                labels = item.get("metric", {})
                points.append(MetricSeriesPoint(timestamp=ts, value=float(val), labels=labels))
        return cls(points=points, raw=payload)
