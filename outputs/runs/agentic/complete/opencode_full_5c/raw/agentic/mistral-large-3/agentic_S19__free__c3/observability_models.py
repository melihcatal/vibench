from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MetricPoint:
    value: Union[int, float]
    timestamp: datetime
    dimensions: Dict[str, str]


@dataclass
class MetricStats:
    metric_name: str
    count: int
    mean: float
    min: float
    max: float
    stddev: Optional[float] = None


@dataclass
class MetricSeries:
    metric_name: str
    points: List[MetricPoint]


class MetricNormalizer:
    """Normalizes Google Cloud Monitoring responses to local models."""

    @staticmethod
    def normalize_point(point: dict, metric_labels: dict) -> MetricPoint:
        value = point.value.double_value or point.value.int64_value
        timestamp = datetime.fromtimestamp(
            point.interval.end_time.seconds + point.interval.end_time.nanos / 1e9
        )
        return MetricPoint(value=value, timestamp=timestamp, dimensions=metric_labels)

    @staticmethod
    def normalize_series(series: dict) -> MetricSeries:
        metric_name = series.metric.type
        points = [
            MetricNormalizer.normalize_point(point, series.metric.labels)
            for point in series.points
        ]
        return MetricSeries(metric_name=metric_name, points=points)
