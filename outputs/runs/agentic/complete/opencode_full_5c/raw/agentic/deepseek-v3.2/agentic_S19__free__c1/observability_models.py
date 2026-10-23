from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class MetricAggregation(Enum):
    MEAN = "ALIGN_MEAN"
    MAX = "ALIGN_MAX"
    MIN = "ALIGN_MIN"
    SUM = "ALIGN_SUM"
    COUNT = "ALIGN_COUNT"


class TimeWindow:
    """Represents a time window for metric queries."""

    def __init__(self, start: datetime, end: datetime):
        self.start = start
        self.end = end

    @classmethod
    def from_minutes_ago(cls, minutes_ago: int, end_minutes_ago: int = 0):
        """Create a time window relative to now."""
        end_time = datetime.utcnow() - timedelta(minutes=end_minutes_ago)
        start_time = datetime.utcnow() - timedelta(minutes=minutes_ago)
        return cls(start_time, end_time)

    def duration_minutes(self) -> float:
        """Get duration in minutes."""
        return (self.end - self.start).total_seconds() / 60


@dataclass
class MetricPoint:
    """Represents a single metric data point."""

    timestamp: datetime
    value: float
    metric_type: str
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "metric_type": self.metric_type,
            "resource_labels": self.resource_labels,
            "metric_labels": self.metric_labels,
        }


@dataclass
class MetricQuery:
    """Represents a metric query request."""

    metric_type: str
    time_window: TimeWindow
    filters: Dict[str, str]
    aggregation: Optional[MetricAggregation] = None
    aggregation_period_minutes: int = 5

    def validate(self) -> bool:
        """Validate the query parameters."""
        if not self.metric_type:
            return False
        if self.time_window.end <= self.time_window.start:
            return False
        return True


@dataclass
class MetricSeries:
    """Represents a series of metric points."""

    points: List[MetricPoint]
    query: MetricQuery

    def average_value(self) -> float:
        """Calculate average value of the series."""
        if not self.points:
            return 0.0
        return sum(p.value for p in self.points) / len(self.points)

    def max_value(self) -> float:
        """Get maximum value in the series."""
        if not self.points:
            return 0.0
        return max(p.value for p in self.points)

    def min_value(self) -> float:
        """Get minimum value in the series."""
        if not self.points:
            return 0.0
        return min(p.value for p in self.points)


@dataclass
class MetricComparison:
    """Represents comparison between two metric series."""

    series_a: MetricSeries
    series_b: MetricSeries
    time_window: TimeWindow

    def ratio(self) -> float:
        """Calculate ratio of average values (A/B)."""
        avg_a = self.series_a.average_value()
        avg_b = self.series_b.average_value()
        if avg_b == 0:
            return 0.0
        return avg_a / avg_b

    def difference(self) -> float:
        """Calculate difference in average values (A - B)."""
        return self.series_a.average_value() - self.series_b.average_value()


def normalize_google_cloud_point(point, time_series) -> MetricPoint:
    """Normalize Google Cloud Monitoring point to MetricPoint."""
    from google.protobuf.timestamp_pb2 import Timestamp

    value = 0.0
    if point.value.HasField("double_value"):
        value = point.value.double_value
    elif point.value.HasField("int64_value"):
        value = float(point.value.int64_value)

    timestamp = point.interval.end_time.ToDatetime()

    return MetricPoint(
        timestamp=timestamp,
        value=value,
        metric_type=time_series.metric.type,
        resource_labels=dict(time_series.resource.labels),
        metric_labels=dict(time_series.metric.labels),
    )
