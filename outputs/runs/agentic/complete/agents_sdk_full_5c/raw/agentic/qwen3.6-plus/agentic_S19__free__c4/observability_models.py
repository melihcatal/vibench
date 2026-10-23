"""
Define local request, response, and normalization helpers for Managed Metrics Monitoring.

Provides dataclasses for metric queries, aggregated stats, and CloudWatch-specific
response parsing utilities.

Provider: AWS CloudWatch (boto3 'monitoring' service).
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


@dataclass
class MetricQueryRequest:
    """Request model for querying a metric over a time window."""
    metric_name: str
    namespace: str
    start_time: datetime
    end_time: datetime
    period: int = 60
    statistic: str = "Average"
    dimensions: Optional[Dict[str, str]] = None
    unit: Optional[str] = None


@dataclass
class AggregationRequest:
    """Request model for aggregated metric statistics."""
    metric_name: str
    namespace: str
    start_time: datetime
    end_time: datetime
    period: int = 300
    statistics: List[str] = field(default_factory=lambda: ["Average", "Sum", "Maximum", "Minimum", "SampleCount"])
    extended_statistics: Optional[List[str]] = None
    dimensions: Optional[Dict[str, str]] = None


@dataclass
class MetricDataPoint:
    """Normalized metric data point."""
    timestamp: datetime
    value: float
    unit: str
    sample_count: Optional[int] = None


@dataclass
class AggregatedStats:
    """Aggregated statistics for a metric over a time window."""
    metric_name: str
    namespace: str
    start_time: datetime
    end_time: datetime
    average: Optional[float] = None
    sum_value: Optional[float] = None
    maximum: Optional[float] = None
    minimum: Optional[float] = None
    sample_count: Optional[int] = None
    p50: Optional[float] = None
    p90: Optional[float] = None
    p95: Optional[float] = None
    p99: Optional[float] = None


@dataclass
class MetricComparisonResult:
    """Result of comparing two metric series."""
    series_a_label: str
    series_b_label: str
    series_a_values: List[float]
    series_b_values: List[float]
    timestamps: List[datetime]
    delta_values: List[float]
    correlation: Optional[float] = None


@dataclass
class CloudWatchMetricQuery:
    """CloudWatch-specific metric query definition for GetMetricData API."""
    query_id: str
    metric_name: str
    namespace: str
    dimensions: Optional[Dict[str, str]] = None
    statistic: str = "Average"
    period: int = 60
    unit: Optional[str] = None
    return_data: bool = True


def normalize_metric_datapoints(raw_datapoints: List[Dict[str, Any]]) -> List[MetricDataPoint]:
    """Normalize raw CloudWatch datapoints into MetricDataPoint objects."""
    normalized = []
    for dp in raw_datapoints:
        point = MetricDataPoint(
            timestamp=dp.get("Timestamp", datetime.utcnow()),
            value=dp.get("Average", dp.get("Sum", dp.get("Maximum", dp.get("Minimum", 0.0)))),
            unit=dp.get("Unit", "None"),
            sample_count=dp.get("SampleCount"),
        )
        normalized.append(point)
    return sorted(normalized, key=lambda p: p.timestamp)


def build_get_metric_data_query(query: CloudWatchMetricQuery) -> Dict[str, Any]:
    """Build a CloudWatch GetMetricData query entry."""
    metric_query = {
        "Id": query.query_id,
        "MetricStat": {
            "Metric": {
                "Namespace": query.namespace,
                "MetricName": query.metric_name,
            },
            "Period": query.period,
            "Stat": query.statistic,
        },
        "ReturnData": query.return_data,
    }
    if query.dimensions:
        dims = [{"Name": k, "Value": v} for k, v in query.dimensions.items()]
        metric_query["MetricStat"]["Metric"]["Dimensions"] = dims
    if query.unit:
        metric_query["MetricStat"]["Metric"]["Unit"] = query.unit
    return metric_query


def parse_aggregated_stats_response(
    metric_name: str,
    namespace: str,
    start_time: datetime,
    end_time: datetime,
    raw_datapoints: List[Dict[str, Any]],
) -> AggregatedStats:
    """Parse CloudWatch ListMetrics/GetMetricStatistics response into AggregatedStats."""
    stats = AggregatedStats(
        metric_name=metric_name,
        namespace=namespace,
        start_time=start_time,
        end_time=end_time,
    )
    for dp in raw_datapoints:
        if "Average" in dp:
            stats.average = dp["Average"]
        if "Sum" in dp:
            stats.sum_value = dp["Sum"]
        if "Maximum" in dp:
            stats.maximum = dp["Maximum"]
        if "Minimum" in dp:
            stats.minimum = dp["Minimum"]
        if "SampleCount" in dp:
            stats.sample_count = dp["SampleCount"]
    return stats


def build_time_window(duration_minutes: int = 60) -> tuple:
    """Build (start_time, end_time) for a recent time window."""
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=duration_minutes)
    return start_time, end_time
