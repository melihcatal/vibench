"""
observability_models.py - Local request, response, and normalization helpers
for Managed Metrics Monitoring.
Provider-agnostic normalization layer over Datadog Metrics API responses.
"""

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class MetricQueryRequest:
    """Normalized request parameters for querying metric data."""
    metric_name: str
    from_ts: int
    to_ts: int
    aggregation: Optional[str] = None
    rollup: Optional[int] = None
    tags: Optional[List[str]] = None
    host: Optional[str] = None
    sources: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "query": self.metric_name,
            "from": self.from_ts,
            "to": self.to_ts,
        }
        if self.aggregation:
            data["aggregation"] = self.aggregation
        if self.rollup:
            data["rollup"] = self.rollup
        if self.tags:
            data["tags"] = ",".join(self.tags)
        return data


@dataclass
class MetricPoint:
    """A single metric datapoint."""
    timestamp: int
    value: float
    tags: Optional[Dict[str, str]] = field(default_factory=dict)


@dataclass
class MetricSeries:
    """A time series of metric points."""
    metric_name: str
    display_name: str
    points: List[MetricPoint]
    expression: Optional[str] = None
    aggregation: Optional[str] = None
    unit: Optional[str] = None
    scope: Optional[str] = None

    def values(self) -> List[float]:
        return [p.value for p in self.points]

    def timestamps(self) -> List[int]:
        return [p.timestamp for p in self.points]


@dataclass
class MetricStats:
    """Aggregated statistics for a metric series."""
    metric_name: str
    count: int
    avg: float
    sum: float
    min: float
    max: float
    stddev: Optional[float] = None
    window_from: int = 0
    window_to: int = 0
    unit: Optional[str] = None


@dataclass
class MetricQueryResponse:
    """Normalized response from a metric query."""
    series: List[MetricSeries]
    query: str
    from_ts: int
    to_ts: int
    resolution: Optional[int] = None
    status: str = "ok"


def normalize_datadog_points(raw_points: List[List[Any]]) -> List[MetricPoint]:
    """Convert Datadog raw [timestamp, value] pairs to MetricPoint objects."""
    points = []
    for ts, val in raw_points:
        if val is not None:
            points.append(MetricPoint(timestamp=int(ts), value=float(val)))
    return points


def build_metric_series_from_datadog(
    raw_series: Dict[str, Any],
) -> MetricSeries:
    """Build a normalized MetricSeries from a Datadog API series object."""
    display_name = raw_series.get("display_name", raw_series.get("metric", ""))
    metric_name = raw_series.get("metric", display_name)
    expression = raw_series.get("expression")
    scope = raw_series.get("scope")
    unit = raw_series.get("unit")

    raw_points = raw_series.get("pointlist", [])
    points = normalize_datadog_points(raw_points)

    return MetricSeries(
        metric_name=metric_name,
        display_name=display_name,
        points=points,
        expression=expression,
        unit=unit,
        scope=scope,
    )


def compute_series_stats(series: MetricSeries) -> MetricStats:
    """Compute aggregated statistics from a MetricSeries."""
    values = series.values()
    if not values:
        return MetricStats(
            metric_name=series.metric_name,
            count=0,
            avg=0.0,
            sum=0.0,
            min=0.0,
            max=0.0,
        )

    total = sum(values)
    count = len(values)
    avg = total / count
    min_val = min(values)
    max_val = max(values)

    variance = sum((v - avg) ** 2 for v in values) / count if count > 1 else 0.0
    stddev = variance ** 0.5

    return MetricStats(
        metric_name=series.metric_name,
        count=count,
        avg=avg,
        sum=total,
        min=min_val,
        max=max_val,
        stddev=stddev,
    )


def time_window_to_epoch_minutes(
    window_minutes: int,
    to_ts: Optional[int] = None,
) -> tuple[int, int]:
    """Convert a window in minutes to (from_ts, to_ts) epoch seconds."""
    if to_ts is None:
        to_ts = int(datetime.datetime.now(datetime.timezone.utc).timestamp())
    from_ts = to_ts - (window_minutes * 60)
    return from_ts, to_ts
