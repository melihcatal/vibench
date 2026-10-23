"""
Define local request, response, and normalization helpers for Managed Metrics Monitoring.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple


@dataclass
class MetricQueryRequest:
    """Request parameters for querying metric data."""
    metric_name: str
    start_ts: int
    end_ts: int
    aggregation: str = "avg"
    filter_tags: Optional[Dict[str, str]] = None
    rollup_interval: Optional[int] = None
    granularity_seconds: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "start_ts": self.start_ts,
            "end_ts": self.end_ts,
            "aggregation": self.aggregation,
            "filter_tags": self.filter_tags or {},
            "rollup_interval": self.rollup_interval,
            "granularity_seconds": self.granularity_seconds,
        }


@dataclass
class MetricDataPoint:
    """A single metric data point."""
    timestamp: int
    value: float

    @property
    def as_datetime(self) -> datetime:
        return datetime.utcfromtimestamp(self.timestamp)


@dataclass
class MetricSeries:
    """A series of metric data points with metadata."""
    metric: str
    display_name: str
    scope: str
    aggregation: str
    unit: Optional[str]
    points: List[MetricDataPoint] = field(default_factory=list)

    @property
    def point_count(self) -> int:
        return len(self.points)

    def values(self) -> List[float]:
        return [p.value for p in self.points]

    def timestamps(self) -> List[int]:
        return [p.timestamp for p in self.points]


@dataclass
class MetricQueryResponse:
    """Normalized response from a metric query."""
    series: List[MetricSeries] = field(default_factory=list)
    query: str = ""
    res_type: str = ""
    message: str = ""
    error: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return self.error is None and len(self.series) > 0


@dataclass
class MetricAggregationStats:
    """Aggregated statistics for a metric over a time window."""
    metric_name: str
    count: int
    sum_value: float
    avg_value: float
    min_value: float
    max_value: float
    p50_value: Optional[float] = None
    p90_value: Optional[float] = None
    p99_value: Optional[float] = None
    start_ts: int = 0
    end_ts: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "count": self.count,
            "sum_value": self.sum_value,
            "avg_value": self.avg_value,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "p50_value": self.p50_value,
            "p90_value": self.p90_value,
            "p99_value": self.p99_value,
            "start_ts": self.start_ts,
            "end_ts": self.end_ts,
        }


@dataclass
class MetricComparisonResult:
    """Result of comparing two metric series."""
    series_a_name: str
    series_b_name: str
    series_a_avg: float
    series_b_avg: float
    absolute_diff: float
    percent_diff: float
    series_a_max: float
    series_b_max: float
    series_a_min: float
    series_b_min: float
    series_a_count: int
    series_b_count: int
    start_ts: int = 0
    end_ts: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "series_a_name": self.series_a_name,
            "series_b_name": self.series_b_name,
            "series_a_avg": self.series_a_avg,
            "series_b_avg": self.series_b_avg,
            "absolute_diff": self.absolute_diff,
            "percent_diff": self.percent_diff,
            "series_a_max": self.series_a_max,
            "series_b_max": self.series_b_max,
            "series_a_min": self.series_a_min,
            "series_b_min": self.series_b_min,
            "series_a_count": self.series_a_count,
            "series_b_count": self.series_b_count,
            "start_ts": self.start_ts,
            "end_ts": self.end_ts,
        }


@dataclass
class MetricTrendSummary:
    """Summary of metric trends or anomalies over a time window."""
    metric_name: str
    overall_trend: str  # "increasing", "decreasing", "stable", "volatile"
    anomaly_count: int
    anomaly_details: List[Dict[str, Any]] = field(default_factory=list)
    avg_value: float = 0.0
    latest_value: float = 0.0
    start_ts: int = 0
    end_ts: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "overall_trend": self.overall_trend,
            "anomaly_count": self.anomaly_count,
            "anomaly_details": self.anomaly_details,
            "avg_value": self.avg_value,
            "latest_value": self.latest_value,
            "start_ts": self.start_ts,
            "end_ts": self.end_ts,
        }


def parse_datadog_response_to_model(raw_response: Any) -> MetricQueryResponse:
    """
    Parse a raw Datadog API response into MetricQueryResponse.
    Handles both datadog_api_client model objects and raw dicts.
    """
    response = MetricQueryResponse()
    response.query = getattr(raw_response, "query", "")
    response.res_type = getattr(raw_response, "res_type", "")
    response.message = getattr(raw_response, "message", "")

    series_list = getattr(raw_response, "series", [])
    for s in series_list:
        metric_series = MetricSeries(
            metric=getattr(s, "metric", ""),
            display_name=getattr(s, "display_name", ""),
            scope=getattr(s, "scope", ""),
            aggregation=getattr(s, "aggr", ""),
            unit=getattr(s, "unit", None),
        )
        pointlist = getattr(s, "pointlist", [])
        for pt in pointlist:
            if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                metric_series.points.append(
                    MetricDataPoint(timestamp=int(pt[0]), value=float(pt[1]))
                )
        response.series.append(metric_series)

    return response


def compute_percentile(values: List[float], percentile: float) -> Optional[float]:
    """Compute the given percentile from a list of values."""
    if not values:
        return None
    sorted_vals = sorted(values)
    idx = (percentile / 100.0) * (len(sorted_vals) - 1)
    lower = int(idx)
    upper = lower + 1
    if upper >= len(sorted_vals):
        return sorted_vals[-1]
    frac = idx - lower
    return sorted_vals[lower] * (1 - frac) + sorted_vals[upper] * frac
