from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum


class MetricKind(Enum):
    """Metric kind enumeration matching Google Cloud Monitoring."""

    GAUGE = "GAUGE"
    DELTA = "DELTA"
    CUMULATIVE = "CUMULATIVE"


class ValueType(Enum):
    """Value type enumeration matching Google Cloud Monitoring."""

    BOOL = "BOOL"
    INT64 = "INT64"
    DOUBLE = "DOUBLE"
    STRING = "STRING"
    DISTRIBUTION = "DISTRIBUTION"
    MONEY = "MONEY"


class AggregationAligner(Enum):
    """Aggregation aligner enumeration."""

    ALIGN_NONE = "ALIGN_NONE"
    ALIGN_DELTA = "ALIGN_DELTA"
    ALIGN_RATE = "ALIGN_RATE"
    ALIGN_INTERPOLATE = "ALIGN_INTERPOLATE"
    ALIGN_NEXT_OLDER = "ALIGN_NEXT_OLDER"
    ALIGN_MIN = "ALIGN_MIN"
    ALIGN_MAX = "ALIGN_MAX"
    ALIGN_MEAN = "ALIGN_MEAN"
    ALIGN_COUNT = "ALIGN_COUNT"
    ALIGN_SUM = "ALIGN_SUM"
    ALIGN_STDDEV = "ALIGN_STDDEV"
    ALIGN_COUNT_TRUE = "ALIGN_COUNT_TRUE"
    ALIGN_COUNT_FALSE = "ALIGN_COUNT_FALSE"
    ALIGN_FRACTION_TRUE = "ALIGN_FRACTION_TRUE"
    ALIGN_PERCENTILE_99 = "ALIGN_PERCENTILE_99"
    ALIGN_PERCENTILE_95 = "ALIGN_PERCENTILE_95"
    ALIGN_PERCENTILE_50 = "ALIGN_PERCENTILE_50"
    ALIGN_PERCENTILE_05 = "ALIGN_PERCENTILE_05"
    ALIGN_PERCENT_CHANGE = "ALIGN_PERCENT_CHANGE"


class AggregationReducer(Enum):
    """Aggregation reducer enumeration."""

    REDUCE_NONE = "REDUCE_NONE"
    REDUCE_MEAN = "REDUCE_MEAN"
    REDUCE_MIN = "REDUCE_MIN"
    REDUCE_MAX = "REDUCE_MAX"
    REDUCE_SUM = "REDUCE_SUM"
    REDUCE_STDDEV = "REDUCE_STDDEV"
    REDUCE_COUNT = "REDUCE_COUNT"
    REDUCE_COUNT_TRUE = "REDUCE_COUNT_TRUE"
    REDUCE_COUNT_FALSE = "REDUCE_COUNT_FALSE"
    REDUCE_FRACTION_TRUE = "REDUCE_FRACTION_TRUE"
    REDUCE_PERCENTILE_99 = "REDUCE_PERCENTILE_99"
    REDUCE_PERCENTILE_95 = "REDUCE_PERCENTILE_95"
    REDUCE_PERCENTILE_50 = "REDUCE_PERCENTILE_50"
    REDUCE_PERCENTILE_05 = "REDUCE_PERCENTILE_05"


@dataclass
class TimeWindow:
    """Time window for metric queries."""

    start_time: datetime
    end_time: datetime

    def duration_seconds(self) -> float:
        """Get duration in seconds."""
        return (self.end_time - self.start_time).total_seconds()

    def duration_minutes(self) -> float:
        """Get duration in minutes."""
        return self.duration_seconds() / 60

    def duration_hours(self) -> float:
        """Get duration in hours."""
        return self.duration_minutes() / 60


@dataclass
class MetricPoint:
    """Single metric data point."""

    timestamp: datetime
    value: Optional[float] = None
    metric_type: Optional[str] = None
    resource_type: Optional[str] = None
    resource_labels: Dict[str, str] = field(default_factory=dict)
    metric_labels: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "metric_type": self.metric_type,
            "resource_type": self.resource_type,
            "resource_labels": self.resource_labels,
            "metric_labels": self.metric_labels,
        }


@dataclass
class MetricSeries:
    """Series of metric points."""

    metric_type: str
    resource_type: str
    resource_labels: Dict[str, str] = field(default_factory=dict)
    metric_labels: Dict[str, str] = field(default_factory=dict)
    points: List[MetricPoint] = field(default_factory=list)

    def add_point(self, point: MetricPoint):
        """Add a point to the series."""
        self.points.append(point)

    def get_values(self) -> List[float]:
        """Get list of values (excluding None)."""
        return [p.value for p in self.points if p.value is not None]

    def get_timestamps(self) -> List[datetime]:
        """Get list of timestamps."""
        return [p.timestamp for p in self.points]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "metric_type": self.metric_type,
            "resource_type": self.resource_type,
            "resource_labels": self.resource_labels,
            "metric_labels": self.metric_labels,
            "points": [p.to_dict() for p in self.points],
            "point_count": len(self.points),
        }


@dataclass
class MetricStatistics:
    """Statistical summary of metric values."""

    count: int
    mean: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    sum: Optional[float] = None
    stddev: Optional[float] = None
    percentile_95: Optional[float] = None
    percentile_99: Optional[float] = None

    @classmethod
    def from_values(cls, values: List[float]) -> "MetricStatistics":
        """Create statistics from a list of values."""
        if not values:
            return cls(count=0)

        import statistics

        return cls(
            count=len(values),
            mean=statistics.mean(values),
            min=min(values),
            max=max(values),
            sum=sum(values),
            stddev=statistics.stdev(values) if len(values) > 1 else 0.0,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "count": self.count,
            "mean": self.mean,
            "min": self.min,
            "max": self.max,
            "sum": self.sum,
            "stddev": self.stddev,
            "percentile_95": self.percentile_95,
            "percentile_99": self.percentile_99,
        }


@dataclass
class MetricQueryRequest:
    """Request for metric queries."""

    metric_type: str
    time_window: TimeWindow
    project_id: str
    filters: Dict[str, str] = field(default_factory=dict)
    aggregation_period_seconds: int = 60
    aggregation_aligner: AggregationAligner = AggregationAligner.ALIGN_MEAN
    aggregation_reducer: AggregationReducer = AggregationReducer.REDUCE_NONE

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "metric_type": self.metric_type,
            "time_window": {
                "start_time": self.time_window.start_time.isoformat(),
                "end_time": self.time_window.end_time.isoformat(),
            },
            "project_id": self.project_id,
            "filters": self.filters,
            "aggregation_period_seconds": self.aggregation_period_seconds,
            "aggregation_aligner": self.aggregation_aligner.value,
            "aggregation_reducer": self.aggregation_reducer.value,
        }


@dataclass
class MetricQueryResponse:
    """Response from metric queries."""

    request: MetricQueryRequest
    series: List[MetricSeries] = field(default_factory=list)
    statistics: Optional[MetricStatistics] = None
    error: Optional[str] = None

    def get_all_points(self) -> List[MetricPoint]:
        """Get all points from all series."""
        points = []
        for series in self.series:
            points.extend(series.points)
        return points

    def get_all_values(self) -> List[float]:
        """Get all values from all series."""
        values = []
        for series in self.series:
            values.extend(series.get_values())
        return values

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {
            "request": self.request.to_dict(),
            "series_count": len(self.series),
            "total_points": sum(len(s.points) for s in self.series),
        }

        if self.series:
            result["series"] = [s.to_dict() for s in self.series]

        if self.statistics:
            result["statistics"] = self.statistics.to_dict()

        if self.error:
            result["error"] = self.error

        return result


@dataclass
class MetricComparison:
    """Comparison between two metric series."""

    series_a: MetricSeries
    series_b: MetricSeries
    time_window: TimeWindow
    comparison_stats: Dict[str, Any] = field(default_factory=dict)
    aligned_points: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "time_window": {
                "start_time": self.time_window.start_time.isoformat(),
                "end_time": self.time_window.end_time.isoformat(),
            },
            "series_a": self.series_a.to_dict(),
            "series_b": self.series_b.to_dict(),
            "comparison_stats": self.comparison_stats,
            "aligned_points": self.aligned_points,
            "aligned_point_count": len(self.aligned_points),
        }


def normalize_metric_response(raw_response: Dict[str, Any]) -> MetricQueryResponse:
    """
    Normalize raw metric API response to standard format.

    Args:
        raw_response: Raw response from monitoring API

    Returns:
        Normalized MetricQueryResponse
    """
    # This is a placeholder for actual normalization logic
    # In practice, this would convert provider-specific responses to our standard format

    return MetricQueryResponse(
        request=MetricQueryRequest(
            metric_type=raw_response.get("metric_type", ""),
            time_window=TimeWindow(
                start_time=datetime.fromisoformat(
                    raw_response.get("time_window", {}).get(
                        "start", datetime.utcnow().isoformat()
                    )
                ),
                end_time=datetime.fromisoformat(
                    raw_response.get("time_window", {}).get(
                        "end", datetime.utcnow().isoformat()
                    )
                ),
            ),
            project_id=raw_response.get("project_id", ""),
        ),
        error=raw_response.get("error"),
    )


def validate_metric_filters(filters: Dict[str, str]) -> bool:
    """
    Validate metric filter dictionary.

    Args:
        filters: Filter dictionary

    Returns:
        True if valid, False otherwise
    """
    if not isinstance(filters, dict):
        return False

    for key, value in filters.items():
        if not isinstance(key, str) or not isinstance(value, str):
            return False

        if not key.strip() or not value.strip():
            return False

    return True


def calculate_percentiles(
    values: List[float], percentiles: List[float] = [50, 95, 99]
) -> Dict[float, float]:
    """
    Calculate percentiles for a list of values.

    Args:
        values: List of numeric values
        percentiles: List of percentiles to calculate

    Returns:
        Dictionary mapping percentiles to values
    """
    if not values:
        return {}

    sorted_values = sorted(values)
    n = len(sorted_values)

    result = {}
    for p in percentiles:
        if p < 0 or p > 100:
            continue

        index = (p / 100) * (n - 1)
        lower_index = int(index)
        upper_index = min(lower_index + 1, n - 1)

        if lower_index == upper_index:
            result[p] = sorted_values[lower_index]
        else:
            weight = index - lower_index
            result[p] = (
                sorted_values[lower_index] * (1 - weight)
                + sorted_values[upper_index] * weight
            )

    return result
