from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum


class MetricAggregation(Enum):
    """Enum for metric aggregation types."""

    MEAN = "ALIGN_MEAN"
    MAX = "ALIGN_MAX"
    MIN = "ALIGN_MIN"
    SUM = "ALIGN_SUM"
    COUNT = "ALIGN_COUNT"
    PERCENTILE_50 = "ALIGN_PERCENTILE_50"
    PERCENTILE_95 = "ALIGN_PERCENTILE_95"
    PERCENTILE_99 = "ALIGN_PERCENTILE_99"


@dataclass
class MetricPoint:
    """Represents a single metric data point."""

    timestamp: datetime
    value: float
    labels: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "labels": self.labels,
        }


@dataclass
class MetricSeries:
    """Represents a metric time series."""

    metric_type: str
    resource_type: str
    metric_labels: Dict[str, str] = field(default_factory=dict)
    resource_labels: Dict[str, str] = field(default_factory=dict)
    points: List[MetricPoint] = field(default_factory=list)

    def add_point(self, point: MetricPoint):
        """Add a point to the series."""
        self.points.append(point)

    def get_values(self) -> List[float]:
        """Get list of values from points."""
        return [point.value for point in self.points]

    def get_timestamps(self) -> List[datetime]:
        """Get list of timestamps from points."""
        return [point.timestamp for point in self.points]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "metric_type": self.metric_type,
            "resource_type": self.resource_type,
            "metric_labels": self.metric_labels,
            "resource_labels": self.resource_labels,
            "points": [point.to_dict() for point in self.points],
        }


@dataclass
class MetricQueryRequest:
    """Request model for metric queries."""

    metric_name: str
    start_time: datetime
    end_time: datetime
    project_id: Optional[str] = None
    dimension_filters: Dict[str, str] = field(default_factory=dict)
    aggregation: MetricAggregation = MetricAggregation.MEAN
    aggregation_period_seconds: int = 60

    def validate(self) -> bool:
        """Validate the request."""
        if not self.metric_name:
            return False
        if self.start_time >= self.end_time:
            return False
        return True


@dataclass
class MetricQueryResponse:
    """Response model for metric queries."""

    request: MetricQueryRequest
    series: List[MetricSeries] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        """Check if query was successful."""
        return self.error is None

    def get_all_points(self) -> List[MetricPoint]:
        """Get all points from all series."""
        points = []
        for series in self.series:
            points.extend(series.points)
        return points

    def get_aggregated_values(self) -> List[float]:
        """Get aggregated values from all series."""
        return [point.value for point in self.get_all_points()]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "error": self.error,
            "request": {
                "metric_name": self.request.metric_name,
                "start_time": self.request.start_time.isoformat(),
                "end_time": self.request.end_time.isoformat(),
                "dimension_filters": self.request.dimension_filters,
            },
            "series_count": len(self.series),
            "total_points": len(self.get_all_points()),
            "series": [series.to_dict() for series in self.series],
        }


@dataclass
class MetricComparison:
    """Model for comparing two metric series."""

    metric_name: str
    window_start: datetime
    window_end: datetime
    series_a: MetricSeries
    series_b: MetricSeries
    statistics: Dict[str, Any] = field(default_factory=dict)

    def calculate_statistics(self):
        """Calculate comparison statistics."""
        values_a = self.series_a.get_values()
        values_b = self.series_b.get_values()

        if not values_a or not values_b:
            return

        mean_a = sum(values_a) / len(values_a)
        mean_b = sum(values_b) / len(values_b)

        self.statistics = {
            "mean_a": mean_a,
            "mean_b": mean_b,
            "mean_difference": mean_a - mean_b,
            "mean_percentage_diff": ((mean_a - mean_b) / mean_b * 100)
            if mean_b != 0
            else None,
            "a_vs_b_ratio": mean_a / mean_b if mean_b != 0 else None,
            "count_a": len(values_a),
            "count_b": len(values_b),
            "max_a": max(values_a) if values_a else None,
            "max_b": max(values_b) if values_b else None,
            "min_a": min(values_a) if values_a else None,
            "min_b": min(values_b) if values_b else None,
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "metric_name": self.metric_name,
            "window": {
                "start": self.window_start.isoformat(),
                "end": self.window_end.isoformat(),
            },
            "series_a": self.series_a.to_dict(),
            "series_b": self.series_b.to_dict(),
            "statistics": self.statistics,
        }


def normalize_google_monitoring_series(google_series) -> MetricSeries:
    """Normalize Google Cloud Monitoring series to our model."""
    from google.protobuf.timestamp_pb2 import Timestamp

    series = MetricSeries(
        metric_type=google_series.metric.type,
        resource_type=google_series.resource.type,
        metric_labels=dict(google_series.metric.labels),
        resource_labels=dict(google_series.resource.labels),
    )

    for point in google_series.points:
        timestamp = point.interval.end_time.ToDatetime()

        if point.value.HasField("double_value"):
            value = point.value.double_value
        elif point.value.HasField("int64_value"):
            value = float(point.value.int64_value)
        elif point.value.HasField("bool_value"):
            value = 1.0 if point.value.bool_value else 0.0
        else:
            value = 0.0

        metric_point = MetricPoint(timestamp=timestamp, value=value, labels={})

        series.add_point(metric_point)

    return series
