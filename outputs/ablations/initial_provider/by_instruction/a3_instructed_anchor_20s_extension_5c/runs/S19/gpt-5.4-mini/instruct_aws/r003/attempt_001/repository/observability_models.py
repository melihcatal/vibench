from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def _to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def isoformat_utc(dt: datetime) -> str:
    return _to_utc(dt).isoformat().replace("+00:00", "Z")


def normalize_dimensions(dimensions: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not dimensions:
        return {}
    return {str(k): str(v) for k, v in dimensions.items() if v is not None}


@dataclass
class MetricWindowRequest:
    namespace: str
    metric_name: str
    start_time: datetime
    end_time: datetime
    period: int = 60
    statistics: Optional[List[str]] = None
    dimensions: Optional[Dict[str, Any]] = None

    def to_cloudwatch_kwargs(self) -> Dict[str, Any]:
        kwargs = {
            "Namespace": self.namespace,
            "MetricName": self.metric_name,
            "StartTime": _to_utc(self.start_time),
            "EndTime": _to_utc(self.end_time),
            "Period": int(self.period),
        }
        if self.statistics:
            kwargs["Statistics"] = list(self.statistics)
        dims = normalize_dimensions(self.dimensions)
        if dims:
            kwargs["Dimensions"] = [{"Name": k, "Value": v} for k, v in dims.items()]
        return kwargs


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
    unit: Optional[str] = None
    dimensions: Optional[Dict[str, str]] = None


def parse_cloudwatch_datapoints(datapoints: List[Dict[str, Any]], statistic: str) -> List[MetricSeriesPoint]:
    points: List[MetricSeriesPoint] = []
    for item in datapoints:
        value = item.get(statistic)
        if value is None:
            continue
        timestamp = item.get("Timestamp")
        if isinstance(timestamp, datetime):
            timestamp = isoformat_utc(timestamp)
        else:
            timestamp = str(timestamp)
        points.append(MetricSeriesPoint(timestamp=timestamp, value=float(value), statistic=statistic))
    points.sort(key=lambda p: p.timestamp)
    return points
