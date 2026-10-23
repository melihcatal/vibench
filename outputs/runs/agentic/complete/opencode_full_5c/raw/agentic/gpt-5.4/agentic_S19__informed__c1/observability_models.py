from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


def _to_iso8601(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


@dataclass
class MetricWindowRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    namespace: str = "AWS/EC2"
    period: int = 300
    stat: str = "Average"
    dimensions: Dict[str, str] = field(default_factory=dict)
    unit: Optional[str] = None

    def as_cloudwatch_kwargs(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "Namespace": self.namespace,
            "MetricName": self.metric_name,
            "Dimensions": [{"Name": k, "Value": v} for k, v in self.dimensions.items()],
            "StartTime": ensure_utc(self.start_time),
            "EndTime": ensure_utc(self.end_time),
            "Period": self.period,
            "Statistics": [self.stat],
        }
        if self.unit:
            payload["Unit"] = self.unit
        return payload


@dataclass
class MetricPoint:
    timestamp: str
    value: Optional[float]
    unit: Optional[str] = None
    dimensions: Dict[str, str] = field(default_factory=dict)
    label: Optional[str] = None


@dataclass
class MetricSeriesResponse:
    metric_name: str
    namespace: str
    stat: str
    start_time: str
    end_time: str
    period: int
    points: List[MetricPoint]


@dataclass
class AggregatedMetricStats:
    metric_name: str
    namespace: str
    sample_count: int
    minimum: Optional[float]
    maximum: Optional[float]
    average: Optional[float]
    sum: Optional[float]
    unit: Optional[str]
    start_time: str
    end_time: str


def normalize_datapoints(
    datapoints: Iterable[Mapping[str, Any]],
    stat: str,
    dimensions: Optional[Dict[str, str]] = None,
    label: Optional[str] = None,
) -> List[MetricPoint]:
    normalized: List[MetricPoint] = []
    for item in sorted(datapoints, key=lambda d: d.get("Timestamp")):
        value = item.get(stat)
        timestamp = item.get("Timestamp")
        timestamp_str = (
            _to_iso8601(timestamp)
            if isinstance(timestamp, datetime)
            else str(timestamp)
        )
        normalized.append(
            MetricPoint(
                timestamp=timestamp_str,
                value=float(value) if value is not None else None,
                unit=item.get("Unit"),
                dimensions=dict(dimensions or {}),
                label=label,
            )
        )
    return normalized


def aggregate_points(
    metric_name: str,
    namespace: str,
    datapoints: Iterable[Mapping[str, Any]],
    start_time: datetime,
    end_time: datetime,
) -> AggregatedMetricStats:
    points = list(datapoints)
    values = [
        float(point["Average"]) for point in points if point.get("Average") is not None
    ]
    sample_count = len(values)
    total_sum = sum(values) if values else None
    average = (total_sum / sample_count) if values else None
    minimum = min(values) if values else None
    maximum = max(values) if values else None
    unit = next((point.get("Unit") for point in points if point.get("Unit")), None)
    return AggregatedMetricStats(
        metric_name=metric_name,
        namespace=namespace,
        sample_count=sample_count,
        minimum=minimum,
        maximum=maximum,
        average=average,
        sum=total_sum,
        unit=unit,
        start_time=_to_iso8601(start_time),
        end_time=_to_iso8601(end_time),
    )


def as_series_response(
    metric_name: str,
    namespace: str,
    stat: str,
    start_time: datetime,
    end_time: datetime,
    period: int,
    datapoints: Iterable[Mapping[str, Any]],
    dimensions: Optional[Dict[str, str]] = None,
    label: Optional[str] = None,
) -> MetricSeriesResponse:
    return MetricSeriesResponse(
        metric_name=metric_name,
        namespace=namespace,
        stat=stat,
        start_time=_to_iso8601(start_time),
        end_time=_to_iso8601(end_time),
        period=period,
        points=normalize_datapoints(
            datapoints, stat=stat, dimensions=dimensions, label=label
        ),
    )
