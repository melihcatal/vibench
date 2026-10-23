from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class MetricKind(Enum):
    """Metric kind enumeration matching Google Cloud Monitoring."""

    GAUGE = "GAUGE"
    DELTA = "DELTA"
    CUMULATIVE = "CUMULATIVE"


class ValueType(Enum):
    """Value type enumeration matching Google Cloud Monitoring."""

    DOUBLE = "DOUBLE"
    INT64 = "INT64"
    DISTRIBUTION = "DISTRIBUTION"
    STRING = "STRING"
    BOOL = "BOOL"


@dataclass
class MetricPoint:
    """Represents a single metric data point."""

    timestamp: datetime
    value: Optional[float]
    metric_type: str
    resource_type: str
    resource_labels: Dict[str, str] = field(default_factory=dict)
    metric_labels: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "metric_type": self.metric_type,
            "resource_type": self.resource_type,
            "resource_labels": self.resource_labels,
            "metric_labels": self.metric_labels,
        }


@dataclass
class MetricStats:
    """Aggregated statistics for a metric series."""

    count: int
    mean: Optional[float]
    min: Optional[float]
    max: Optional[float]
    p50: Optional[float] = None
    p95: Optional[float] = None
    p99: Optional[float] = None
    sum: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "count": self.count,
            "mean": self.mean,
            "min": self.min,
            "max": self.max,
            "p50": self.p50,
            "p95": self.p95,
            "p99": self.p99,
            "sum": self.sum,
        }


@dataclass
class MetricQueryRequest:
    """Request model for metric queries."""

    metric_type: str
    window_minutes: int = 60
    resource_filters: Dict[str, str] = field(default_factory=dict)
    metric_filters: Dict[str, str] = field(default_factory=dict)
    aggregation_period_minutes: Optional[int] = None
    aligner: Optional[str] = None

    def validate(self) -> List[str]:
        """Validate the request parameters."""
        errors = []

        if not self.metric_type:
            errors.append("metric_type is required")

        if self.window_minutes <= 0:
            errors.append("window_minutes must be positive")

        if self.aggregation_period_minutes and self.aggregation_period_minutes <= 0:
            errors.append("aggregation_period_minutes must be positive if provided")

        return errors


@dataclass
class MetricQueryResponse:
    """Response model for metric queries."""

    success: bool
    data: List[MetricPoint]
    stats: Optional[MetricStats] = None
    error_message: Optional[str] = None
    query_duration_ms: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "success": self.success,
            "data_count": len(self.data),
            "query_duration_ms": self.query_duration_ms,
        }

        if self.stats:
            result["stats"] = self.stats.to_dict()

        if self.error_message:
            result["error_message"] = self.error_message

        if self.data and len(self.data) <= 10:
            result["sample_data"] = [point.to_dict() for point in self.data[:5]]

        return result


@dataclass
class MetricComparison:
    """Comparison results between two metric series."""

    series_a: List[MetricPoint]
    series_b: List[MetricPoint]
    stats_a: MetricStats
    stats_b: MetricStats
    filter_a: Dict[str, str]
    filter_b: Dict[str, str]
    window_minutes: int
    metric_type: str

    @property
    def mean_difference(self) -> Optional[float]:
        """Calculate the difference in means between series."""
        if self.stats_a.mean is not None and self.stats_b.mean is not None:
            return self.stats_a.mean - self.stats_b.mean
        return None

    @property
    def relative_difference_percent(self) -> Optional[float]:
        """Calculate relative difference as percentage."""
        if (
            self.stats_a.mean is not None
            and self.stats_b.mean is not None
            and self.stats_b.mean != 0
        ):
            return (self.stats_a.mean - self.stats_b.mean) / self.stats_b.mean * 100
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "metric_type": self.metric_type,
            "window_minutes": self.window_minutes,
            "series_a": {
                "filter": self.filter_a,
                "count": len(self.series_a),
                "stats": self.stats_a.to_dict(),
            },
            "series_b": {
                "filter": self.filter_b,
                "count": len(self.series_b),
                "stats": self.stats_b.to_dict(),
            },
            "comparison": {
                "mean_difference": self.mean_difference,
                "relative_difference_percent": self.relative_difference_percent,
            },
        }


def normalize_google_cloud_point(point, time_series) -> MetricPoint:
    """
    Normalize a Google Cloud Monitoring point to our model.

    Args:
        point: Google Cloud Monitoring Point
        time_series: Google Cloud Monitoring TimeSeries

    Returns:
        Normalized MetricPoint
    """
    from google.protobuf.timestamp_pb2 import Timestamp

    timestamp = point.interval.end_time.ToDatetime()

    value = None
    if point.value.HasField("double_value"):
        value = point.value.double_value
    elif point.value.HasField("int64_value"):
        value = float(point.value.int64_value)
    elif point.value.HasField("distribution_value"):
        value = point.value.distribution_value.mean

    return MetricPoint(
        timestamp=timestamp,
        value=value,
        metric_type=time_series.metric.type,
        resource_type=time_series.resource.type,
        resource_labels=dict(time_series.resource.labels),
        metric_labels=dict(time_series.metric.labels),
    )


def calculate_stats_from_points(points: List[MetricPoint]) -> MetricStats:
    """
    Calculate statistics from a list of metric points.

    Args:
        points: List of MetricPoint objects

    Returns:
        MetricStats object
    """
    if not points:
        return MetricStats(count=0, mean=None, min=None, max=None)

    values = [p.value for p in points if p.value is not None]

    if not values:
        return MetricStats(count=len(points), mean=None, min=None, max=None)

    sorted_values = sorted(values)
    count = len(values)

    return MetricStats(
        count=count,
        mean=sum(values) / count,
        min=min(values),
        max=max(values),
        p50=sorted_values[int(count * 0.5) - 1] if count >= 2 else sorted_values[0],
        p95=sorted_values[int(count * 0.95) - 1] if count >= 2 else sorted_values[0],
        p99=sorted_values[int(count * 0.99) - 1] if count >= 2 else sorted_values[0],
        sum=sum(values),
    )
