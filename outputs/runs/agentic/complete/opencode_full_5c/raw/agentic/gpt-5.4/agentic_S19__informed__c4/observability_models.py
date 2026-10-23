from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from statistics import mean
from typing import Any, Dict, List, Optional


def _to_epoch_seconds(value: datetime | int | float | str) -> int:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return int(value.timestamp())
    if isinstance(value, str):
        return int(datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp())
    return int(value)


def _to_iso8601(epoch_seconds: int) -> str:
    return (
        datetime.fromtimestamp(epoch_seconds, tz=timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


@dataclass
class MetricWindowRequest:
    metric: str
    start_time: datetime | int | float | str
    end_time: datetime | int | float | str
    namespace: str = "AWS/EC2"
    period: int = 60
    stat: str = "Average"
    dimensions: Dict[str, str] = field(default_factory=dict)
    unit: Optional[str] = None

    def start_epoch(self) -> int:
        return _to_epoch_seconds(self.start_time)

    def end_epoch(self) -> int:
        return _to_epoch_seconds(self.end_time)

    def start_iso(self) -> str:
        return _to_iso8601(self.start_epoch())

    def end_iso(self) -> str:
        return _to_iso8601(self.end_epoch())


@dataclass
class MetricPoint:
    timestamp: str
    value: float
    unit: Optional[str] = None
    dimensions: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeriesResponse:
    metric: str
    namespace: str
    stat: str
    points: List[MetricPoint]

    def values(self) -> List[float]:
        return [point.value for point in self.points]


@dataclass
class MetricStatsResponse:
    metric: str
    namespace: str
    start_time: str
    end_time: str
    sample_count: int
    minimum: Optional[float]
    maximum: Optional[float]
    average: Optional[float]
    sum: Optional[float]
    unit: Optional[str] = None


def normalize_dimensions(dimensions: Optional[Dict[str, Any]]) -> Dict[str, str]:
    return {
        str(key): str(value)
        for key, value in (dimensions or {}).items()
        if value is not None
    }


def build_dimensions_list(dimensions: Optional[Dict[str, Any]]) -> List[Dict[str, str]]:
    return [
        {"Name": str(key), "Value": str(value)}
        for key, value in normalize_dimensions(dimensions).items()
    ]


def build_points_from_datapoints(
    datapoints: List[Dict[str, Any]],
    stat: str,
    dimensions: Optional[Dict[str, str]] = None,
) -> List[MetricPoint]:
    normalized_points: List[MetricPoint] = []
    for item in sorted(datapoints, key=lambda entry: entry["Timestamp"]):
        value = item.get(stat)
        if value is None:
            continue
        timestamp = item["Timestamp"]
        if isinstance(timestamp, datetime):
            timestamp_text = (
                timestamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
            )
        else:
            timestamp_text = str(timestamp)
        normalized_points.append(
            MetricPoint(
                timestamp=timestamp_text,
                value=float(value),
                unit=item.get("Unit"),
                dimensions=normalize_dimensions(dimensions),
            )
        )
    return normalized_points


def aggregate_points(
    metric: str,
    namespace: str,
    start_time: str,
    end_time: str,
    points: List[MetricPoint],
) -> MetricStatsResponse:
    values = [point.value for point in points]
    if not values:
        return MetricStatsResponse(
            metric=metric,
            namespace=namespace,
            start_time=start_time,
            end_time=end_time,
            sample_count=0,
            minimum=None,
            maximum=None,
            average=None,
            sum=None,
            unit=None,
        )
    return MetricStatsResponse(
        metric=metric,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
        sample_count=len(values),
        minimum=min(values),
        maximum=max(values),
        average=mean(values),
        sum=float(sum(values)),
        unit=points[0].unit,
    )


def summarize_change(
    series_a: MetricSeriesResponse, series_b: MetricSeriesResponse
) -> Dict[str, Any]:
    values_a = series_a.values()
    values_b = series_b.values()
    avg_a = mean(values_a) if values_a else None
    avg_b = mean(values_b) if values_b else None
    delta = (avg_a - avg_b) if avg_a is not None and avg_b is not None else None
    ratio = (avg_a / avg_b) if avg_a is not None and avg_b not in (None, 0) else None
    return {
        "left_metric": series_a.metric,
        "right_metric": series_b.metric,
        "left_average": avg_a,
        "right_average": avg_b,
        "average_delta": delta,
        "average_ratio": ratio,
    }
