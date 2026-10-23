from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import json


class MetricAggregation(Enum):
    """Aggregation methods for metric data."""

    MEAN = "mean"
    SUM = "sum"
    COUNT = "count"
    MIN = "min"
    MAX = "max"
    P95 = "p95"
    P99 = "p99"


class TimeWindow:
    """Represents a time window for metric queries."""

    def __init__(self, start_time: datetime, end_time: datetime):
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary with ISO format timestamps."""
        return {"start": self.start_time.isoformat(), "end": self.end_time.isoformat()}

    @property
    def duration_hours(self) -> float:
        """Get duration in hours."""
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 3600


@dataclass
class MetricQuery:
    """Request model for metric queries."""

    metric_name: str
    start_time: datetime
    end_time: datetime
    dimension_filters: Optional[Dict[str, str]] = None
    aggregation_period_seconds: int = 60
    aggregation_method: MetricAggregation = MetricAggregation.MEAN

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "metric_name": self.metric_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "dimension_filters": self.dimension_filters or {},
            "aggregation_period_seconds": self.aggregation_period_seconds,
            "aggregation_method": self.aggregation_method.value,
        }


@dataclass
class DataPoint:
    """Represents a single metric data point."""

    timestamp: datetime
    value: float
    labels: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result = {"timestamp": self.timestamp.isoformat(), "value": self.value}
        if self.labels:
            result["labels"] = self.labels
        return result


@dataclass
class TimeSeries:
    """Represents a time series of metric data."""

    metric_type: str
    resource_type: str
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]
    points: List[DataPoint]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "metric_type": self.metric_type,
            "resource_type": self.resource_type,
            "resource_labels": self.resource_labels,
            "metric_labels": self.metric_labels,
            "points": [point.to_dict() for point in self.points],
            "point_count": len(self.points),
        }

    @property
    def values(self) -> List[float]:
        """Get list of values from points."""
        return [point.value for point in self.points]

    def get_statistics(self) -> Dict[str, Optional[float]]:
        """Calculate basic statistics for the time series."""
        if not self.points:
            return {
                "count": 0,
                "mean": None,
                "min": None,
                "max": None,
                "p95": None,
                "p99": None,
            }

        values = self.values
        sorted_values = sorted(values)
        n = len(values)

        return {
            "count": n,
            "mean": sum(values) / n,
            "min": min(values),
            "max": max(values),
            "p95": sorted_values[int(0.95 * n) - 1] if n >= 20 else None,
            "p99": sorted_values[int(0.99 * n) - 1] if n >= 100 else None,
        }


@dataclass
class MetricStatistics:
    """Aggregated statistics for a metric."""

    metric_name: str
    time_window: TimeWindow
    series_count: int
    total_points: int
    mean: Optional[float]
    min: Optional[float]
    max: Optional[float]
    p95: Optional[float]
    p99: Optional[float]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "metric_name": self.metric_name,
            "time_window": self.time_window.to_dict(),
            "series_count": self.series_count,
            "total_points": self.total_points,
            "mean": self.mean,
            "min": self.min,
            "max": self.max,
            "p95": self.p95,
            "p99": self.p99,
        }


@dataclass
class SeriesComparison:
    """Comparison results between two time series."""

    metric_name: str
    time_window: TimeWindow
    series_a: Dict[str, Any]
    series_b: Dict[str, Any]
    mean_difference: Optional[float]
    mean_difference_percent: Optional[float]
    a_higher: Optional[bool]
    significant_difference: Optional[bool]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "metric_name": self.metric_name,
            "time_window": self.time_window.to_dict(),
            "series_a": self.series_a,
            "series_b": self.series_b,
            "mean_difference": self.mean_difference,
            "mean_difference_percent": self.mean_difference_percent,
            "a_higher": self.a_higher,
            "significant_difference": self.significant_difference,
        }


class ResponseNormalizer:
    """Helper for normalizing responses from Google Cloud Monitoring."""

    @staticmethod
    def normalize_time_series(cloud_time_series) -> TimeSeries:
        """Normalize Google Cloud Monitoring TimeSeries to our model."""
        points = []
        for point in cloud_time_series.points:
            point_time = point.interval.end_time.ToDatetime()
            point_value = point.value.double_value or point.value.int64_value or 0.0

            points.append(
                DataPoint(
                    timestamp=point_time,
                    value=float(point_value),
                    labels=dict(cloud_time_series.metric.labels),
                )
            )

        return TimeSeries(
            metric_type=cloud_time_series.metric.type,
            resource_type=cloud_time_series.resource.type,
            resource_labels=dict(cloud_time_series.resource.labels),
            metric_labels=dict(cloud_time_series.metric.labels),
            points=points,
        )

    @staticmethod
    def normalize_statistics(
        metric_name: str,
        start_time: datetime,
        end_time: datetime,
        time_series_list: List[TimeSeries],
    ) -> MetricStatistics:
        """Calculate normalized statistics from multiple time series."""
        all_values = []
        for series in time_series_list:
            all_values.extend(series.values)

        if not all_values:
            return MetricStatistics(
                metric_name=metric_name,
                time_window=TimeWindow(start_time, end_time),
                series_count=len(time_series_list),
                total_points=0,
                mean=None,
                min=None,
                max=None,
                p95=None,
                p99=None,
            )

        sorted_values = sorted(all_values)
        n = len(sorted_values)

        return MetricStatistics(
            metric_name=metric_name,
            time_window=TimeWindow(start_time, end_time),
            series_count=len(time_series_list),
            total_points=n,
            mean=sum(all_values) / n,
            min=min(all_values),
            max=max(all_values),
            p95=sorted_values[int(0.95 * n) - 1] if n >= 20 else None,
            p99=sorted_values[int(0.99 * n) - 1] if n >= 100 else None,
        )


def serialize_response(obj: Any) -> str:
    """Serialize response objects to JSON string."""
    if hasattr(obj, "to_dict"):
        data = obj.to_dict()
    elif isinstance(obj, (dict, list, str, int, float, bool, type(None))):
        data = obj
    else:
        data = asdict(obj) if hasattr(obj, "__dataclass_fields__") else str(obj)

    return json.dumps(data, indent=2, default=str)
