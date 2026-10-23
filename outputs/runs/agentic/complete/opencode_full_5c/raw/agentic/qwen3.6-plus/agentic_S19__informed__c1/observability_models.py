from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MetricQueryRequest:
    metric: str
    start_ts: int
    end_ts: int
    query_type: str = "timeseries"
    rollup_interval: int = 60
    aggregator: str = "avg"
    dimensions: dict[str, str] = field(default_factory=dict)

    def to_datadog_query(self) -> str:
        dim_parts = [f"{k}:{v}" for k, v in self.dimensions.items()]
        base = f"{self.aggregator}:{self.metric}"
        if dim_parts:
            base += "{" + ",".join(dim_parts) + "}"
        return base

    def to_datadog_payload(self) -> dict[str, Any]:
        return {
            "query": self.to_datadog_query(),
            "from": self.start_ts,
            "to": self.end_ts,
        }


@dataclass
class DataPoint:
    timestamp: int
    value: float


@dataclass
class MetricSeries:
    metric: str
    display_name: str
    expression: str
    unit: str
    scope: str
    start_ts: int
    end_ts: int
    interval: int
    points: list[DataPoint] = field(default_factory=list)
    tag_set: dict[str, str] = field(default_factory=dict)


@dataclass
class AggregationStats:
    metric: str
    start_ts: int
    end_ts: int
    avg: float | None = None
    sum_: float | None = None
    min_: float | None = None
    max_: float | None = None
    count: int = 0
    p50: float | None = None
    p95: float | None = None
    p99: float | None = None


@dataclass
class DimensionFilter:
    metric: str
    dimensions: dict[str, str]
    start_ts: int
    end_ts: int
    aggregator: str = "avg"
    rollup_interval: int = 60


@dataclass
class MetricComparisonResult:
    metric: str
    start_ts: int
    end_ts: int
    series_a: MetricSeries
    series_b: MetricSeries
    diff_avg: float = 0.0
    diff_pct: float = 0.0
    correlation: float = 0.0


def normalize_datadog_series(
    raw_series: dict[str, Any], metric_name: str
) -> MetricSeries:
    points_raw = raw_series.get("pointlist", [])
    points = [
        DataPoint(timestamp=int(ts), value=float(val) if val is not None else 0.0)
        for ts, val in points_raw
        if ts is not None
    ]
    tag_set = {}
    scope = raw_series.get("scope", "")
    for token in scope.split(","):
        token = token.strip()
        if ":" in token:
            k, v = token.split(":", 1)
            tag_set[k.strip()] = v.strip()
    return MetricSeries(
        metric=metric_name,
        display_name=raw_series.get("display_name", metric_name),
        expression=raw_series.get("expression", ""),
        unit=raw_series.get("unit", ""),
        scope=scope,
        start_ts=int(raw_series.get("start", 0)),
        end_ts=int(raw_series.get("end", 0)),
        interval=int(raw_series.get("interval", 60)),
        points=points,
        tag_set=tag_set,
    )


def compute_aggregation(series: MetricSeries) -> AggregationStats:
    values = [p.value for p in series.points]
    if not values:
        return AggregationStats(
            metric=series.metric,
            start_ts=series.start_ts,
            end_ts=series.end_ts,
        )
    sorted_vals = sorted(values)
    count = len(sorted_vals)
    p50_idx = max(0, int(count * 0.50) - 1)
    p95_idx = max(0, int(count * 0.95) - 1)
    p99_idx = max(0, int(count * 0.99) - 1)
    return AggregationStats(
        metric=series.metric,
        start_ts=series.start_ts,
        end_ts=series.end_ts,
        avg=sum(values) / count,
        sum_=sum(values),
        min_=min(values),
        max_=max(values),
        count=count,
        p50=sorted_vals[p50_idx],
        p95=sorted_vals[p95_idx],
        p99=sorted_vals[p99_idx],
    )


def compute_comparison(
    series_a: MetricSeries, series_b: MetricSeries
) -> MetricComparisonResult:
    vals_a = [p.value for p in series_a.points]
    vals_b = [p.value for p in series_b.points]
    avg_a = sum(vals_a) / len(vals_a) if vals_a else 0.0
    avg_b = sum(vals_b) / len(vals_b) if vals_b else 0.0
    diff = avg_a - avg_b
    pct = (diff / avg_b * 100.0) if avg_b != 0 else 0.0
    min_len = min(len(vals_a), len(vals_b))
    if min_len > 1:
        mean_a = sum(vals_a[:min_len]) / min_len
        mean_b = sum(vals_b[:min_len]) / min_len
        cov = (
            sum((vals_a[i] - mean_a) * (vals_b[i] - mean_b) for i in range(min_len))
            / min_len
        )
        std_a = (sum((v - mean_a) ** 2 for v in vals_a[:min_len]) / min_len) ** 0.5
        std_b = (sum((v - mean_b) ** 2 for v in vals_b[:min_len]) / min_len) ** 0.5
        corr = cov / (std_a * std_b) if std_a > 0 and std_b > 0 else 0.0
    else:
        corr = 0.0
    return MetricComparisonResult(
        metric=series_a.metric,
        start_ts=series_a.start_ts,
        end_ts=series_a.end_ts,
        series_a=series_a,
        series_b=series_b,
        diff_avg=diff,
        diff_pct=pct,
        correlation=corr,
    )


def format_metric_timeline(series: MetricSeries, max_points: int = 50) -> str:
    points = (
        series.points[-max_points:]
        if len(series.points) > max_points
        else series.points
    )
    lines = [f"Metric: {series.metric} ({series.unit})"]
    lines.append(f"Window: {series.start_ts} - {series.end_ts}")
    lines.append(f"Scope: {series.scope}")
    lines.append("---")
    for p in points:
        ts_str = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(p.timestamp))
        lines.append(f"  {ts_str}  {p.value:.4f}")
    return "\n".join(lines)
