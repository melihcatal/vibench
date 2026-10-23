"""
Define local request, response, and normalization helpers for Managed Metrics Monitoring.
Provides dataclasses and utility functions for CloudWatch metrics data structures.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class MetricStat(Enum):
    """CloudWatch metric statistics types."""
    AVERAGE = "Average"
    SUM = "Sum"
    MINIMUM = "Minimum"
    MAXIMUM = "Maximum"
    SAMPLE_COUNT = "SampleCount"
    EXTREME_VALUES = "tm99"


class MetricNamespace(Enum):
    """Common AWS CloudWatch metric namespaces."""
    EC2 = "AWS/EC2"
    RDS = "AWS/RDS"
    ELB = "AWS/ELB"
    LAMBDA = "AWS/Lambda"
    S3 = "AWS/S3"
    CUSTOM = "Custom"


@dataclass
class MetricQueryRequest:
    """Request parameters for querying CloudWatch metrics."""
    metric_name: str
    namespace: str
    start_time: datetime
    end_time: datetime
    period: int = 300  # seconds, default 5 minutes
    dimensions: Optional[List[Dict[str, str]]] = None
    statistics: Optional[List[str]] = None
    unit: Optional[str] = None

    def to_cloudwatch_params(self) -> Dict[str, Any]:
        """Convert to AWS CloudWatch get_metric_data parameters."""
        params = {
            "MetricDataQueries": [
                {
                    "Id": "metric_query_1",
                    "MetricStat": {
                        "Metric": {
                            "Namespace": self.namespace,
                            "MetricName": self.metric_name,
                        },
                        "Period": self.period,
                        "Stat": self.statistics[0] if self.statistics else "Average",
                    },
                }
            ],
            "StartTime": self.start_time,
            "EndTime": self.end_time,
        }
        if self.dimensions:
            params["MetricDataQueries"][0]["MetricStat"]["Metric"]["Dimensions"] = self.dimensions
        if self.unit:
            params["MetricDataQueries"][0]["MetricStat"]["Unit"] = self.unit
        return params


@dataclass
class MetricDataPoint:
    """Represents a single CloudWatch metric data point."""
    timestamp: datetime
    value: float
    unit: str = "Count"
    sample_count: Optional[int] = None

    @classmethod
    def from_cloudwatch_response(cls, datapoint: Dict[str, Any]) -> "MetricDataPoint":
        """Create from a CloudWatch API response data point."""
        return cls(
            timestamp=datapoint.get("Timestamp", datetime.now()),
            value=datapoint.get("Average", datapoint.get("Sum", 0.0)),
            unit=datapoint.get("Unit", "Count"),
            sample_count=datapoint.get("SampleCount"),
        )


@dataclass
class MetricSeries:
    """A time series of metric data points for a specific resource/dimension set."""
    metric_name: str
    namespace: str
    dimensions: List[Dict[str, str]]
    datapoints: List[MetricDataPoint] = field(default_factory=list)
    statistics: List[str] = field(default_factory=list)

    @property
    def values(self) -> List[float]:
        """Extract just the values from all datapoints."""
        return [dp.value for dp in self.datapoints]

    @property
    def timestamps(self) -> List[datetime]:
        """Extract just the timestamps from all datapoints."""
        return [dp.timestamp for dp in self.datapoints]


@dataclass
class MetricComparisonResult:
    """Result of comparing two metric series."""
    series_a: MetricSeries
    series_b: MetricSeries
    correlation: Optional[float] = None
    percent_difference: Optional[float] = None
    summary: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert comparison result to a dictionary."""
        return {
            "metric_name": self.series_a.metric_name,
            "namespace": self.series_a.namespace,
            "series_a_dimensions": self.series_a.dimensions,
            "series_b_dimensions": self.series_b.dimensions,
            "series_a_avg": sum(self.series_a.values) / len(self.series_a.values) if self.series_a.values else 0,
            "series_b_avg": sum(self.series_b.values) / len(self.series_b.values) if self.series_b.values else 0,
            "correlation": self.correlation,
            "percent_difference": self.percent_difference,
            "summary": self.summary,
        }


@dataclass
class MetricAggregationResult:
    """Aggregated statistics for a metric over a time window."""
    metric_name: str
    namespace: str
    start_time: datetime
    end_time: datetime
    period: int
    statistics: Dict[str, float]
    datapoint_count: int
    unit: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert aggregation result to dictionary."""
        return {
            "metric_name": self.metric_name,
            "namespace": self.namespace,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "period": self.period,
            "statistics": self.statistics,
            "datapoint_count": self.datapoint_count,
            "unit": self.unit,
        }


def normalize_metric_value(value: Any, unit: str = "Count") -> float:
    """
    Normalize a metric value to a float, handling CloudWatch unit conversions.

    Args:
        value: Raw metric value.
        unit: CloudWatch unit string.

    Returns:
        Normalized float value.
    """
    if value is None:
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def build_dimension_filter(dimension_name: str, dimension_values: List[str]) -> List[Dict[str, str]]:
    """
    Build a dimension filter for CloudWatch queries.

    Args:
        dimension_name: Name of the dimension (e.g., 'InstanceId').
        dimension_values: List of values to filter by.

    Returns:
        List of dimension dictionaries for CloudWatch API.
    """
    return [
        {"Name": dimension_name, "Value": val}
        for val in dimension_values
    ]


def merge_metric_series(series_list: List[MetricSeries]) -> Dict[str, MetricSeries]:
    """
    Merge multiple metric series by dimension set.

    Args:
        series_list: List of MetricSeries objects.

    Returns:
        Dictionary mapping dimension signature to merged MetricSeries.
    """
    merged = {}
    for series in series_list:
        dim_key = str(sorted(series.dimensions))
        if dim_key not in merged:
            merged[dim_key] = MetricSeries(
                metric_name=series.metric_name,
                namespace=series.namespace,
                dimensions=series.dimensions,
                datapoints=[],
            )
        merged[dim_key].datapoints.extend(series.datapoints)
    return merged
