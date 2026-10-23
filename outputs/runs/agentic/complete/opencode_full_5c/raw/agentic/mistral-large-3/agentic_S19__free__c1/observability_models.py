from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from google.api import metric_pb2 as ga_metric
from google.api import monitor_pb2 as ga_monitor


@dataclass
class MetricQuery:
    metric_type: str
    filter_str: Optional[str] = None
    hours: int = 1


@dataclass
class MetricDataPoint:
    value: Union[int, float]
    timestamp: int
    labels: Dict[str, str]


@dataclass
class MetricSeries:
    metric_type: str
    points: List[MetricDataPoint]


@dataclass
class AggregatedMetricStats:
    metric_type: str
    count: int
    mean: float
    sum: float
    min: float
    max: float
    stddev: float


def normalize_gcp_metric_response(response) -> List[MetricSeries]:
    series_map = {}

    for result in response.time_series:
        metric_type = result.metric.type
        labels = dict(result.metric.labels)

        if metric_type not in series_map:
            series_map[metric_type] = MetricSeries(metric_type=metric_type, points=[])

        for point in result.points:
            value = point.value.double_value or point.value.int64_value
            timestamp = point.interval.end_time.ToSeconds()
            series_map[metric_type].points.append(
                MetricDataPoint(value=value, timestamp=timestamp, labels=labels)
            )

    return list(series_map.values())
