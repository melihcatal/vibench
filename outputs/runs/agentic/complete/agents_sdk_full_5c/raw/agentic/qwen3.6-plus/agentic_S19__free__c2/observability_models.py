"""
Local request, response, and normalization helpers for Managed Metrics Monitoring.

Provider: Datadog (datadog-api-client)
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class MetricAggregation(str, Enum):
    AVG = "avg"
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    LAST = "last"


class MetricDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"


@dataclass
class MetricTimeWindow:
    """Represents a time window for metric queries."""
    start: datetime
    end: datetime
    interval_seconds: int = 60

    @classmethod
    def from_now(cls, minutes_ago: int = 60, interval_seconds: int = 60) -> "MetricTimeWindow":
        now = datetime.utcnow()
        return cls(
            start=now - timedelta(minutes=minutes_ago),
            end=now,
            interval_seconds=interval_seconds,
        )

    def to_datadog_timestamps(self) -> Tuple[int, int]:
        """Convert to Unix epoch seconds for Datadog API."""
        return (int(self.start.timestamp()), int(self.end.timestamp()))


@dataclass
class MetricQueryRequest:
    """Request parameters for a metric query."""
    metric_name: str
    time_window: MetricTimeWindow
    aggregation: MetricAggregation = MetricAggregation.AVG
    tags: Dict[str, str] = field(default_factory=dict)
    group_by: Optional[List[str]] = None
    rollup_interval: Optional[int] = None

    def to_datadog_query_string(self) -> str:
        """Build Datadog-formatted metric query string."""
        base = f"{self.aggregation.value}:{self.metric_name}"
        if self.tags:
            tag_parts = [f"{k}:{v}" for k, v in self.tags.items()]
            base += f"{{{','.join(tag_parts)}}}"
        if self.group_by:
            base += f" by {{{','.join(self.group_by)}}}"
        if self.rollup_interval:
            base += f".rollup({self.rollup_interval})"
        return base


@dataclass
class MetricDataPoint:
    """Represents a single metric data point."""
    timestamp: datetime
    value: float
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeries:
    """Represents a metric series with expression and scope."""
    expression: str
    scope: Optional[str] = None
    data_points: List[MetricDataPoint] = field(default_factory=list)


@dataclass
class MetricAggregateStats:
    """Aggregated statistics for a metric over a window."""
    metric_name: str
    aggregation: MetricAggregation
    window: MetricTimeWindow
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    avg_value: Optional[float] = None
    sum_value: Optional[float] = None
    count: Optional[int] = None
    p50: Optional[float] = None
    p95: Optional[float] = None
    p99: Optional[float] = None


@dataclass
class DimensionFilter:
    """Filter definition for metric dimensions/tags."""
    dimension_key: str
    dimension_values: List[str]
    operator: str = "in"  # in, not_in, exists


@dataclass
class MetricComparisonResult:
    """Result of comparing two metric series."""
    series_a: MetricSeries
    series_b: MetricSeries
    correlation: Optional[float] = None
    mean_difference: Optional[float] = None
    relative_change_pct: Optional[float] = None


@dataclass
class MetricAnnotation:
    """Metric annotation or dashboard note."""
    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    source: str = ""


def normalize_datadog_response(raw_response: Dict[str, Any]) -> List[MetricDataPoint]:
    """Normalize Datadog API response into MetricDataPoint list."""
    points = []
    series_list = raw_response.get("series", [])
    for series in series_list:
        expression = series.get("expression", "")
        scope = series.get("scope", "")
        point_list = series.get("pointlist", [])
        for pt in point_list:
            if len(pt) >= 2 and pt[1] is not None:
                ts = datetime.utcfromtimestamp(pt[0] / 1000.0)
                points.append(MetricDataPoint(
                    timestamp=ts,
                    value=float(pt[1]),
                    tags={"expression": expression, "scope": scope},
                ))
    return points


def normalize_aggregate_response(raw_response: Dict[str, Any], metric_name: str,
                                  aggregation: MetricAggregation,
                                  window: MetricTimeWindow) -> MetricAggregateStats:
    """Normalize Datadog aggregate API response."""
    series_list = raw_response.get("series", [])
    stats = MetricAggregateStats(
        metric_name=metric_name,
        aggregation=aggregation,
        window=window,
    )
    if series_list:
        pointlist = series_list[0].get("pointlist", [])
        if pointlist:
            values = [float(p[1]) for p in pointlist if p[1] is not None]
            if values:
                stats.min_value = min(values)
                stats.max_value = max(values)
                stats.avg_value = sum(values) / len(values)
                stats.sum_value = sum(values)
                stats.count = len(values)
                sorted_vals = sorted(values)
                stats.p50 = _percentile(sorted_vals, 0.50)
                stats.p95 = _percentile(sorted_vals, 0.95)
                stats.p99 = _percentile(sorted_vals, 0.99)
    return stats


def _percentile(sorted_values: List[float], percentile: float) -> float:
    """Calculate percentile from sorted list."""
    if not sorted_values:
        return 0.0
    k = (len(sorted_values) - 1) * percentile
    f = int(k)
    c = f + 1
    if c >= len(sorted_values):
        return sorted_values[-1]
    return sorted_values[f] + (k - f) * (sorted_values[c] - sorted_values[f])
