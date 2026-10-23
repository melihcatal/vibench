from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class MetricWindowRequest:
    metric_type: str
    start_time: datetime
    end_time: datetime
    dimensions: Optional[Dict[str, str]] = None


@dataclass(frozen=True)
class MetricSeriesPoint:
    timestamp: datetime
    value: float
    labels: Dict[str, str]


@dataclass(frozen=True)
class MetricAggregateStats:
    count: int
    minimum: float
    maximum: float
    mean: float
    sum: float


def point_from_time_series_point(point: Any) -> MetricSeriesPoint:
    ts = point.interval.end_time
    value = 0.0
    if point.value.string_value:
        value = float(point.value.string_value)
    elif point.value.int64_value:
        value = float(point.value.int64_value)
    elif point.value.double_value:
        value = float(point.value.double_value)
    return MetricSeriesPoint(timestamp=ts, value=value, labels={})


def stats_from_values(values: List[float]) -> MetricAggregateStats:
    if not values:
        return MetricAggregateStats(
            count=0, minimum=0.0, maximum=0.0, mean=0.0, sum=0.0
        )
    total = sum(values)
    return MetricAggregateStats(
        count=len(values),
        minimum=min(values),
        maximum=max(values),
        mean=total / len(values),
        sum=total,
    )
