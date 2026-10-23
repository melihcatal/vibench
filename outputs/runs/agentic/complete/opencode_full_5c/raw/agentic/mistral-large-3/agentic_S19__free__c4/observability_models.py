from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MetricPoint:
    """Normalized metric datapoint."""

    timestamp: datetime
    value: Union[int, float]
    labels: Dict[str, str]


@dataclass
class MetricStats:
    """Normalized metric statistics."""

    count: int
    mean: float
    min: float
    max: float
    sum: float
    stddev: Optional[float] = None


@dataclass
class MetricSeries:
    """Normalized metric series."""

    metric_type: str
    points: List[MetricPoint]
    resource_type: str
    resource_labels: Dict[str, str]


def normalize_metric_point(point) -> MetricPoint:
    """Normalize a Google Cloud Monitoring point."""
    return MetricPoint(
        timestamp=datetime.fromtimestamp(
            point.interval.end_time.timestamp(), datetime.timezone.utc
        ),
        value=point.value.int64_value
        if point.value.int64_value is not None
        else point.value.double_value,
        labels={
            **point.value.labels,
            **getattr(point, "resource", {}).labels,
        },
    )
