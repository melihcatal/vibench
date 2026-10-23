from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class MetricType(Enum):
    GAUGE = "gauge"
    DELTA = "delta"
    CUMULATIVE = "cumulative"


@dataclass
class MetricPoint:
    timestamp: datetime
    value: float
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]


@dataclass
class MetricSeries:
    metric_type: str
    points: List[MetricPoint]
    unit: str


@dataclass
class AggregatedStats:
    mean: float
    min: float
    max: float
    count: int
    stddev: Optional[float] = None


def normalize_metric_response(raw_response: Any) -> List[MetricSeries]:
    series_list = []
    for series in raw_response:
        points = []
        for point in series.points:
            points.append(
                MetricPoint(
                    timestamp=point.interval.end_time.ToDatetime(),
                    value=float(point.value.double_value),
                    resource_labels=dict(series.resource.labels),
                    metric_labels=dict(series.metric.labels),
                )
            )
        series_list.append(
            MetricSeries(
                metric_type=series.metric.type, points=points, unit=series.metric.unit
            )
        )
    return series_list


def calculate_stats(series: MetricSeries) -> AggregatedStats:
    values = [point.value for point in series.points]
    if not values:
        return AggregatedStats(mean=0.0, min=0.0, max=0.0, count=0)

    mean = sum(values) / len(values)
    min_val = min(values)
    max_val = max(values)
    count = len(values)

    variance = sum((x - mean) ** 2 for x in values) / count
    stddev = variance**0.5

    return AggregatedStats(
        mean=mean, min=min_val, max=max_val, count=count, stddev=stddev
    )
