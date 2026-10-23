from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class MetricAggregation(Enum):
    """Aggregation methods for metric data."""

    MEAN = "mean"
    SUM = "sum"
    COUNT = "count"
    MIN = "min"
    MAX = "max"
    PERCENTILE_50 = "p50"
    PERCENTILE_95 = "p95"
    PERCENTILE_99 = "p99"


class TimeWindowUnit(Enum):
    """Time window units for metric queries."""

    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"


@dataclass
class MetricQueryRequest:
    """Request model for metric queries."""

    metric_type: str
    time_window: int = 30
    time_unit: TimeWindowUnit = TimeWindowUnit.MINUTES
    filters: Dict[str, str] = field(default_factory=dict)
    aggregation: MetricAggregation = MetricAggregation.MEAN
    alignment_period_seconds: int = 60

    def to_google_filter(self) -> str:
        """Convert to Google Cloud Monitoring filter string."""
        filter_parts = [f'metric.type = "{self.metric_type}"']

        for key, value in self.filters.items():
            if key.startswith("resource."):
                filter_parts.append(f'{key} = "{value}"')
            else:
                filter_parts.append(f'metric.labels.{key} = "{value}"')

        return " AND ".join(filter_parts)

    def get_time_window_minutes(self) -> int:
        """Convert time window to minutes."""
        if self.time_unit == TimeWindowUnit.MINUTES:
            return self.time_window
        elif self.time_unit == TimeWindowUnit.HOURS:
            return self.time_window * 60
        elif self.time_unit == TimeWindowUnit.DAYS:
            return self.time_window * 24 * 60
        return self.time_window


@dataclass
class MetricDataPoint:
    """Model for a single metric data point."""

    timestamp: datetime
    value: float
    metric_type: str
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str] = field(default_factory=dict)

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
class MetricSeries:
    """Model for a metric time series."""

    metric_type: str
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]
    points: List[MetricDataPoint] = field(default_factory=list)

    def add_point(self, point: MetricDataPoint):
        """Add a data point to the series."""
        self.points.append(point)

    def get_values(self) -> List[float]:
        """Extract values from all points."""
        return [point.value for point in self.points]

    def get_statistics(self) -> Dict[str, Optional[float]]:
        """Calculate basic statistics for the series."""
        values = self.get_values()
        if not values:
            return {"count": 0, "min": None, "max": None, "avg": None, "sum": None}

        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "sum": sum(values),
        }


@dataclass
class MetricComparisonResult:
    """Result model for metric comparisons."""

    metric_type: str
    time_window_minutes: int
    filter_a: Dict[str, str]
    filter_b: Dict[str, str]
    series_a: Optional[MetricSeries] = None
    series_b: Optional[MetricSeries] = None
    statistics_a: Dict[str, Optional[float]] = field(default_factory=dict)
    statistics_b: Dict[str, Optional[float]] = field(default_factory=dict)
    difference: Optional[float] = None
    percent_difference: Optional[float] = None

    def calculate_differences(self):
        """Calculate differences between the two series."""
        if not self.series_a or not self.series_b:
            return

        stats_a = self.series_a.get_statistics()
        stats_b = self.series_b.get_statistics()

        self.statistics_a = stats_a
        self.statistics_b = stats_b

        if stats_a["avg"] is not None and stats_b["avg"] is not None:
            self.difference = stats_a["avg"] - stats_b["avg"]
            if stats_b["avg"] != 0:
                self.percent_difference = (self.difference / stats_b["avg"]) * 100


@dataclass
class AggregatedMetricStats:
    """Model for aggregated metric statistics."""

    metric_type: str
    time_window_minutes: int
    count: int
    min_value: Optional[float]
    max_value: Optional[float]
    avg_value: Optional[float]
    sum_value: Optional[float]
    percentile_50: Optional[float] = None
    percentile_95: Optional[float] = None
    percentile_99: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "metric": self.metric_type,
            "window_minutes": self.time_window_minutes,
            "count": self.count,
            "min": self.min_value,
            "max": self.max_value,
            "avg": self.avg_value,
            "sum": self.sum_value,
            "p50": self.percentile_50,
            "p95": self.percentile_95,
            "p99": self.percentile_99,
        }
