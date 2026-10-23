"""
observability_models.py
Define local request, response, and normalization helpers for Managed Metrics Monitoring.
Provides data classes and normalization utilities for Datadog metric operations.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime


@dataclass
class MetricQueryRequest:
    """Request model for querying metric data points."""
    metric_name: str
    start_time: float  # epoch seconds
    end_time: float    # epoch seconds
    aggregation: str = "avg"
    rollup_interval: Optional[int] = None  # seconds
    host_filter: Optional[str] = None
    tag_filters: Optional[List[str]] = None

    def to_datadog_query(self) -> str:
        """Build a Datadog query string."""
        query = self.metric_name
        if self.host_filter:
            query = f"{query}{{host:{self.host_filter}}}"
        if self.tag_filters:
            tag_str = ",".join(self.tag_filters)
            if self.host_filter:
                query = query.replace("}", f",{tag_str}}}")
            else:
                query = f"{query}{{{tag_str}}}"
        if self.aggregation:
            query = f"{self.aggregation}:{query}"
        if self.rollup_interval:
            query = f"rollup({query}, {self.rollup_interval})"
        return query


@dataclass
class Datapoint:
    """A single metric data point."""
    timestamp: float
    value: Optional[float]
    metric_name: str
    tags: Optional[Dict[str, str]] = None


@dataclass
class MetricSeries:
    """A time series of metric data."""
    metric_name: str
    display_name: str
    tags: Optional[Dict[str, str]] = None
    datapoints: List[Datapoint] = field(default_factory=list)
    start_time: float = 0.0
    end_time: float = 0.0
    aggregation: str = "avg"

    def values(self) -> List[Optional[float]]:
        return [dp.value for dp in self.datapoints]

    def timestamps(self) -> List[float]:
        return [dp.timestamp for dp in self.datapoints]

    def non_null_values(self) -> List[float]:
        return [v for v in self.values() if v is not None]


@dataclass
class MetricStats:
    """Aggregated statistics for a metric over a window."""
    metric_name: str
    start_time: float
    end_time: float
    aggregation: str
    count: int
    avg: Optional[float]
    min: Optional[float]
    max: Optional[float]
    sum: Optional[float]
    std_dev: Optional[float] = None
    p50: Optional[float] = None
    p95: Optional[float] = None
    p99: Optional[float] = None


@dataclass
class MetricComparisonResult:
    """Comparison between two metric series."""
    series_a_name: str
    series_b_name: str
    series_a: Optional[MetricSeries] = None
    series_b: Optional[MetricSeries] = None
    correlation: Optional[float] = None
    mean_diff: Optional[float] = None
    std_diff: Optional[float] = None
    overlap_pct: Optional[float] = None
    comparison_window: Tuple[float, float] = (0.0, 0.0)


@dataclass
class MetricSummary:
    """Summary of metric trends and anomalies."""
    metric_name: str
    window_start: float
    window_end: float
    trend: str  # "increasing", "decreasing", "stable", "unknown"
    anomaly_count: int
    anomaly_timestamps: List[float]
    current_value: Optional[float]
    baseline_value: Optional[float]
    deviation_pct: Optional[float]


@dataclass
class MetricAnnotation:
    """Annotation or note attached to metric data."""
    text: str
    timestamp: float
    author: Optional[str] = None
    tags: Optional[List[str]] = None
    safety_checked: bool = False
    translation_locale: Optional[str] = None


def normalize_datadog_series_to_metric_series(
    raw_series: Dict[str, Any],
    metric_name: str,
    start_time: float = 0.0,
    end_time: float = 0.0,
) -> MetricSeries:
    """Convert a raw Datadog series response to a MetricSeries object."""
    tags = {}
    raw_tags = raw_series.get("tag_set", raw_series.get("tags", []))
    if isinstance(raw_tags, dict):
        tags = raw_tags
    elif isinstance(raw_tags, list):
        for t in raw_tags:
            if ":" in t:
                k, v = t.split(":", 1)
                tags[k] = v
            else:
                tags[t] = "true"

    display_name = raw_series.get("display_name", raw_series.get("metric", metric_name))
    aggregation = raw_series.get("aggr", "avg")

    datapoints = []
    for point in raw_series.get("pointlist", raw_series.get("points", [])):
        if isinstance(point, (list, tuple)) and len(point) >= 2:
            ts = float(point[0])
            val = point[1]
            if val is not None:
                try:
                    val = float(val)
                except (ValueError, TypeError):
                    val = None
            datapoints.append(Datapoint(timestamp=ts, value=val, metric_name=metric_name, tags=dict(tags)))

    return MetricSeries(
        metric_name=metric_name,
        display_name=display_name,
        tags=tags if tags else None,
        datapoints=datapoints,
        start_time=start_time,
        end_time=end_time,
        aggregation=aggregation,
    )


def compute_stats_from_series(series: MetricSeries) -> MetricStats:
    """Compute aggregated statistics from a MetricSeries."""
    values = series.non_null_values()
    if not values:
        return MetricStats(
            metric_name=series.metric_name,
            start_time=series.start_time,
            end_time=series.end_time,
            aggregation=series.aggregation,
            count=0, avg=None, min=None, max=None, sum=None, std_dev=None,
            p50=None, p95=None, p99=None,
        )

    count = len(values)
    avg_val = sum(values) / count
    min_val = min(values)
    max_val = max(values)
    sum_val = sum(values)
    variance = sum((v - avg_val) ** 2 for v in values) / max(count - 1, 1)
    std_val = variance ** 0.5

    sorted_vals = sorted(values)
    p50 = sorted_vals[int(count * 0.5)]
    p95 = sorted_vals[min(int(count * 0.95), count - 1)]
    p99 = sorted_vals[min(int(count * 0.99), count - 1)]

    return MetricStats(
        metric_name=series.metric_name,
        start_time=series.start_time,
        end_time=series.end_time,
        aggregation=series.aggregation,
        count=count,
        avg=round(avg_val, 4),
        min=min_val,
        max=max_val,
        sum=round(sum_val, 4),
        std_dev=round(std_val, 4),
        p50=p50,
        p95=p95,
        p99=p99,
    )


def build_datadog_query_body(
    metric_name: str,
    start_ts: float,
    end_ts: float,
    aggregation: str = "avg",
    tags: Optional[List[str]] = None,
    group_by: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Build a Datadog API v2 query request body."""
    query_body = {
        "data": {
            "type": "metric_content_item",
            "attributes": {
                "formula": "a",
                "queries": [
                    {
                        "data_source": "metrics",
                        "query": f"{aggregation}:{metric_name}" + (f"{{{','.join(tags)}}}" if tags else ""),
                        "name": "a",
                        "aggregator": aggregation,
                    }
                ],
            },
        }
    }
    if start_ts > 0:
        query_body["data"]["attributes"]["from_timestamp"] = int(start_ts)
    if end_ts > 0:
        query_body["data"]["attributes"]["to_timestamp"] = int(end_ts)
    return query_body
