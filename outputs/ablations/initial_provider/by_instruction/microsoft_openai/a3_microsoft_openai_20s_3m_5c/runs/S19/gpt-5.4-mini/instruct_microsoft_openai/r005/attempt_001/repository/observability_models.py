from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass
class MetricWindowRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    resource: Optional[str] = None
    dimensions: Dict[str, str] = field(default_factory=dict)
    aggregation: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "metric_name": self.metric_name,
            "start_time": _iso(self.start_time),
            "end_time": _iso(self.end_time),
        }
        if self.resource is not None:
            payload["resource"] = self.resource
        if self.dimensions:
            payload["dimensions"] = self.dimensions
        if self.aggregation is not None:
            payload["aggregation"] = self.aggregation
        return payload


@dataclass
class MetricPoint:
    timestamp: str
    value: float
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeriesResponse:
    metric_name: str
    points: List[MetricPoint]
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "MetricSeriesResponse":
        points = [MetricPoint(timestamp=p["timestamp"], value=float(p["value"]), labels=p.get("labels", {})) for p in payload.get("points", [])]
        return cls(metric_name=payload.get("metric_name", ""), points=points, metadata=payload.get("metadata", {}))


def normalize_dimensions(dimensions: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not dimensions:
        return {}
    return {str(k): str(v) for k, v in dimensions.items() if v is not None}
