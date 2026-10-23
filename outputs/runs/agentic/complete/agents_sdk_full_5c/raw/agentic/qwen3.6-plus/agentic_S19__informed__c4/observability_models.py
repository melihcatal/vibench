"""
Data models and normalization helpers for Managed Metrics Monitoring.

Defines request/response dataclasses and payload normalization utilities
used across metric query, aggregation, and comparison integrations.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import time


@dataclass
class MetricQueryRequest:
    """Request parameters for querying metric datapoints."""
    metric_name: str
    start_ts: int  # epoch seconds
    end_ts: int    # epoch seconds
    aggregation: str = "avg"
    rollup: int = 60  # seconds
    dimensions: Optional[Dict[str, str]] = None
    group_by: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "start_ts": self.start_ts,
            "end_ts": self.end_ts,
            "aggregation": self.aggregation,
            "rollup": self.rollup,
            "dimensions": self.dimensions,
            "group_by": self.group_by,
        }


@dataclass
class MetricDatapoint:
    """A single metric datapoint with timestamp and value."""
    timestamp: int  # epoch seconds
    value: float
    metric: str = ""
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeries:
    """A time series of metric datapoints, identified by display name and tags."""
    metric_name: str
    display_name: str
    datapoints: List[MetricDatapoint] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)
    aggregation: str = "avg"


@dataclass
class MetricQueryResponse:
    """Response wrapper for metric query results."""
    series: List[MetricSeries] = field(default_factory=list)
    query: str = ""
    from_ts: int = 0
    to_ts: int = 0
    group_by: List[str] = field(default_factory=list)
    message: str = ""

    @property
    def total_datapoints(self) -> int:
        return sum(len(s.datapoints) for s in self.series)


@dataclass
class MetricAggregationStats:
    """Aggregated statistics for a metric over a time window."""
    metric_name: str
    min: float = 0.0
    max: float = 0.0
    avg: float = 0.0
    sum: float = 0.0
    count: int = 0
    percentile_50: float = 0.0
    percentile_95: float = 0.0
    percentile_99: float = 0.0
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricComparisonResult:
    """Comparison result between two metric series."""
    series_a: MetricSeries
    series_b: MetricSeries
    diff_per_point: List[float] = field(default_factory=list)
    mean_diff: float = 0.0
    max_diff: float = 0.0
    min_diff: float = 0.0
    correlation: float = 0.0
    correlation_computed: bool = False


def parse_datadog_query_response(raw_json: Dict[str, Any]) -> MetricQueryResponse:
    """Parse a Datadog /api/v1/query response into MetricQueryResponse.

    Args:
        raw_json: JSON response from Datadog metrics query endpoint.

    Returns:
        Normalized MetricQueryResponse object.
    """
    response = MetricQueryResponse(
        query=raw_json.get("query", ""),
        from_ts=raw_json.get("from_date", 0),
        to_ts=raw_json.get("to_date", 0),
        group_by=raw_json.get("group_by", []),
        message=raw_json.get("message", ""),
    )

    for series_raw in raw_json.get("series", []):
        series = MetricSeries(
            metric_name=series_raw.get("metric", ""),
            display_name=series_raw.get("display_name", ""),
            tags=series_raw.get("tag_set", {}),
            aggregation=series_raw.get("aggr", "avg"),
        )

        for point_raw in series_raw.get("pointlist", []):
            if point_raw[1] is not None:
                ts = int(point_raw[0] / 1000) if point_raw[0] > 1e12 else int(point_raw[0])
                series.datapoints.append(MetricDatapoint(
                    timestamp=ts,
                    value=float(point_raw[1]),
                    metric=series.metric_name,
                    tags=dict(series.tags),
                ))

        response.series.append(series)

    return response


def normalize_dimensions(dimensions: Optional[Dict[str, str]]) -> Dict[str, str]:
    """Normalize dimension/tag dictionary for Datadog query construction.

    Ensures all keys and values are strings and strips whitespace.

    Args:
        dimensions: Raw dimension mapping.

    Returns:
        Normalized dict suitable for Datadog tag filters.
    """
    if dimensions is None:
        return {}

    return {
        str(k).strip().lower(): str(v).strip().lower()
        for k, v in dimensions.items()
        if k and v
    }


def compute_aggregation_stats(datapoints: List[MetricDatapoint]) -> MetricAggregationStats:
    """Compute aggregated statistics from a list of datapoints.

    Args:
        datapoints: List of MetricDatapoint objects.

    Returns:
        MetricAggregationStats with computed statistics.
    """
    if not datapoints:
        return MetricAggregationStats(metric_name="")

    values = sorted([dp.value for dp in datapoints])
    count = len(values)
    total = sum(values)

    def percentile(sorted_vals: List[float], pct: float) -> float:
        if not sorted_vals:
            return 0.0
        idx = int(len(sorted_vals) * pct / 100.0)
        idx = min(idx, len(sorted_vals) - 1)
        return sorted_vals[idx]

    return MetricAggregationStats(
        metric_name=datapoints[0].metric,
        min=values[0],
        max=values[-1],
        avg=total / count,
        sum=total,
        count=count,
        percentile_50=percentile(values, 50),
        percentile_95=percentile(values, 95),
        percentile_99=percentile(values, 99),
        tags=dict(datapoints[0].tags) if datapoints[0].tags else {},
    )
