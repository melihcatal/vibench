from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import statistics


@dataclass
class MetricQueryRequest:
    """Request model for metric queries."""

    metric_type: str
    window_minutes: int = 30
    filters: Dict[str, str] = field(default_factory=dict)
    aggregation: Optional[str] = None
    alignment_period_seconds: int = 300

    def to_filter_string(self) -> str:
        """Convert filters to Google Cloud Monitoring filter string."""
        filter_parts = [f'metric.type = "{self.metric_type}"']

        for key, value in self.filters.items():
            if key.startswith("resource."):
                filter_parts.append(f'resource.labels.{key[9:]} = "{value}"')
            elif key.startswith("metric."):
                filter_parts.append(f'metric.labels.{key[7:]} = "{value}"')
            else:
                filter_parts.append(f'metric.labels.{key} = "{value}"')

        return " AND ".join(filter_parts)


@dataclass
class MetricPoint:
    """Model for a single metric data point."""

    timestamp: datetime
    value: float
    labels: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "labels": self.labels,
        }


@dataclass
class MetricSeries:
    """Model for a metric time series."""

    metric_type: str
    resource_type: str
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]
    points: List[MetricPoint] = field(default_factory=list)

    def add_point(self, point: MetricPoint):
        """Add a data point to the series."""
        self.points.append(point)

    def get_statistics(self) -> Dict[str, Any]:
        """Calculate statistics for the series."""
        if not self.points:
            return {}

        values = [point.value for point in self.points]

        return {
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "min": min(values),
            "max": max(values),
            "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "metric_type": self.metric_type,
            "resource_type": self.resource_type,
            "resource_labels": self.resource_labels,
            "metric_labels": self.metric_labels,
            "points": [point.to_dict() for point in self.points],
            "statistics": self.get_statistics(),
        }


@dataclass
class AggregationResult:
    """Model for aggregated metric results."""

    metric_type: str
    window_minutes: int
    aggregation_type: str
    series_count: int
    datapoint_count: int
    aggregated_value: float
    statistics: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "metric_type": self.metric_type,
            "window_minutes": self.window_minutes,
            "aggregation_type": self.aggregation_type,
            "series_count": self.series_count,
            "datapoint_count": self.datapoint_count,
            "aggregated_value": self.aggregated_value,
            "statistics": self.statistics,
        }


@dataclass
class ComparisonResult:
    """Model for metric comparison results."""

    metric_type: str
    window_minutes: int
    filter_a: Dict[str, str]
    filter_b: Dict[str, str]
    series_a_stats: Dict[str, Any]
    series_b_stats: Dict[str, Any]
    difference: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "metric_type": self.metric_type,
            "window_minutes": self.window_minutes,
            "filter_a": self.filter_a,
            "filter_b": self.filter_b,
            "series_a": self.series_a_stats,
            "series_b": self.series_b_stats,
            "difference": self.difference,
        }


def normalize_google_metric_response(time_series_response) -> List[MetricSeries]:
    """Normalize Google Cloud Monitoring TimeSeries response to local models."""
    series_list = []

    for ts in time_series_response:
        series = MetricSeries(
            metric_type=ts.metric.type,
            resource_type=ts.resource.type,
            resource_labels=dict(ts.resource.labels),
            metric_labels=dict(ts.metric.labels),
        )

        for point in ts.points:
            timestamp = point.interval.end_time.ToDatetime()

            if point.value.HasField("double_value"):
                value = point.value.double_value
            elif point.value.HasField("int64_value"):
                value = float(point.value.int64_value)
            elif point.value.HasField("bool_value"):
                value = 1.0 if point.value.bool_value else 0.0
            elif point.value.HasField("string_value"):
                try:
                    value = float(point.value.string_value)
                except ValueError:
                    value = 0.0
            else:
                value = 0.0

            series.add_point(
                MetricPoint(
                    timestamp=timestamp, value=value, labels=dict(ts.metric.labels)
                )
            )

        series_list.append(series)

    return series_list


def calculate_aggregation_stats(
    series_list: List[MetricSeries], aggregation_type: str = "avg"
) -> AggregationResult:
    """Calculate aggregation statistics from a list of metric series."""
    if not series_list:
        return AggregationResult(
            metric_type="",
            window_minutes=0,
            aggregation_type=aggregation_type,
            series_count=0,
            datapoint_count=0,
            aggregated_value=0.0,
        )

    all_values = []
    total_points = 0

    for series in series_list:
        total_points += len(series.points)
        all_values.extend([point.value for point in series.points])

    if not all_values:
        aggregated_value = 0.0
    elif aggregation_type == "avg":
        aggregated_value = statistics.mean(all_values)
    elif aggregation_type == "max":
        aggregated_value = max(all_values)
    elif aggregation_type == "min":
        aggregated_value = min(all_values)
    elif aggregation_type == "sum":
        aggregated_value = sum(all_values)
    else:
        aggregated_value = statistics.mean(all_values)

    stats = {}
    if all_values:
        stats = {
            "mean": statistics.mean(all_values),
            "median": statistics.median(all_values),
            "min": min(all_values),
            "max": max(all_values),
            "stdev": statistics.stdev(all_values) if len(all_values) > 1 else 0.0,
        }

    return AggregationResult(
        metric_type=series_list[0].metric_type,
        window_minutes=30,  # Default, should be passed as parameter
        aggregation_type=aggregation_type,
        series_count=len(series_list),
        datapoint_count=total_points,
        aggregated_value=aggregated_value,
        statistics=stats,
    )
