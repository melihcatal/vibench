import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional


class MetricAggregation(Enum):
    AVG = "avg"
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    RATE = "rate"


class MetricRollup(Enum):
    AUTO = "auto"
    MIN = "min"
    HOUR = "hour"
    DAY = "day"


@dataclass
class MetricQueryRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    aggregation: MetricAggregation = MetricAggregation.AVG
    rollup: Optional[MetricRollup] = None
    scope: str = "*"

    def to_dict(self) -> dict:
        return {
            "metric_name": self.metric_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "aggregation": self.aggregation.value,
            "rollup": self.rollup.value if self.rollup else None,
            "scope": self.scope,
        }


@dataclass
class MetricDataPoint:
    timestamp: datetime
    value: float

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
        }


@dataclass
class MetricSeries:
    metric_name: str
    scope: str
    aggregation: str
    points: list[MetricDataPoint] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "metric_name": self.metric_name,
            "scope": self.scope,
            "aggregation": self.aggregation,
            "points": [p.to_dict() for p in self.points],
        }


@dataclass
class MetricQueryResponse:
    series: list[MetricSeries]
    query_time_ms: int
    from_ts: int
    to_ts: int
    group_by: Optional[list[str]] = None

    def to_dict(self) -> dict:
        return {
            "series": [s.to_dict() for s in self.series],
            "query_time_ms": self.query_time_ms,
            "from_ts": self.from_ts,
            "to_ts": self.to_ts,
            "group_by": self.group_by or [],
        }


@dataclass
class AggregatedStatsRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    aggregations: list[MetricAggregation] = field(
        default_factory=lambda: [
            MetricAggregation.AVG,
            MetricAggregation.MAX,
            MetricAggregation.MIN,
            MetricAggregation.SUM,
        ]
    )
    scope: str = "*"

    def to_dict(self) -> dict:
        return {
            "metric_name": self.metric_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "aggregations": [a.value for a in self.aggregations],
            "scope": self.scope,
        }


@dataclass
class AggregatedStatsResult:
    metric_name: str
    scope: str
    start_time: datetime
    end_time: datetime
    avg: Optional[float] = None
    max: Optional[float] = None
    min: Optional[float] = None
    sum: Optional[float] = None
    count: Optional[float] = None
    rate: Optional[float] = None
    sample_count: int = 0

    def to_dict(self) -> dict:
        return {
            "metric_name": self.metric_name,
            "scope": self.scope,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "avg": self.avg,
            "max": self.max,
            "min": self.min,
            "sum": self.sum,
            "count": self.count,
            "rate": self.rate,
            "sample_count": self.sample_count,
        }


@dataclass
class DimensionFilter:
    tag_key: str
    tag_value: str

    def to_query_string(self) -> str:
        return f"{self.tag_key}:{self.tag_value}"


@dataclass
class DimensionFilterRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    filters: list[DimensionFilter] = field(default_factory=list)
    aggregation: MetricAggregation = MetricAggregation.AVG
    group_by: Optional[list[str]] = None

    def to_dict(self) -> dict:
        return {
            "metric_name": self.metric_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "filters": [f.to_query_string() for f in self.filters],
            "aggregation": self.aggregation.value,
            "group_by": self.group_by or [],
        }


@dataclass
class DimensionFilterResponse:
    series: list[MetricSeries]
    query_time_ms: int
    filter_expression: str

    def to_dict(self) -> dict:
        return {
            "series": [s.to_dict() for s in self.series],
            "query_time_ms": self.query_time_ms,
            "filter_expression": self.filter_expression,
        }


@dataclass
class MetricComparisonRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    scope_a: str
    scope_b: str
    aggregation: MetricAggregation = MetricAggregation.AVG

    def to_dict(self) -> dict:
        return {
            "metric_name": self.metric_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "scope_a": self.scope_a,
            "scope_b": self.scope_b,
            "aggregation": self.aggregation.value,
        }


@dataclass
class MetricComparisonResult:
    metric_name: str
    aggregation: str
    start_time: datetime
    end_time: datetime
    series_a: MetricSeries
    series_b: MetricSeries
    delta_mean: float
    delta_max: float
    delta_min: float
    correlation: float

    def to_dict(self) -> dict:
        return {
            "metric_name": self.metric_name,
            "aggregation": self.aggregation,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "series_a": self.series_a.to_dict(),
            "series_b": self.series_b.to_dict(),
            "delta_mean": self.delta_mean,
            "delta_max": self.delta_max,
            "delta_min": self.delta_min,
            "correlation": self.correlation,
        }


def normalize_datadog_series(raw_series: list[dict]) -> list[MetricSeries]:
    normalized = []
    for s in raw_series:
        metric_name = s.get("metric", "unknown")
        scope = s.get("scope", "*")
        aggregation = s.get("aggr", "avg")
        point_list = s.get("pointlist", [])
        points = []
        for raw_point in point_list:
            if len(raw_point) >= 2 and raw_point[1] is not None:
                ts = datetime.fromtimestamp(raw_point[0] / 1000.0, tz=timezone.utc)
                points.append(MetricDataPoint(timestamp=ts, value=float(raw_point[1])))
        normalized.append(
            MetricSeries(
                metric_name=metric_name,
                scope=scope,
                aggregation=aggregation,
                points=points,
            )
        )
    return normalized


def compute_aggregated_stats(series: list[MetricSeries]) -> list[AggregatedStatsResult]:
    results = []
    for s in series:
        values = [p.value for p in s.points if p.value is not None]
        if not values:
            results.append(
                AggregatedStatsResult(
                    metric_name=s.metric_name,
                    scope=s.scope,
                    start_time=s.points[0].timestamp
                    if s.points
                    else datetime.now(timezone.utc),
                    end_time=s.points[-1].timestamp
                    if s.points
                    else datetime.now(timezone.utc),
                    sample_count=0,
                )
            )
            continue
        results.append(
            AggregatedStatsResult(
                metric_name=s.metric_name,
                scope=s.scope,
                start_time=s.points[0].timestamp,
                end_time=s.points[-1].timestamp,
                avg=sum(values) / len(values),
                max=max(values),
                min=min(values),
                sum=sum(values),
                count=len(values),
                sample_count=len(values),
            )
        )
    return results


def compute_correlation(series_a: list[float], series_b: list[float]) -> float:
    n = min(len(series_a), len(series_b))
    if n < 2:
        return 0.0
    a = series_a[:n]
    b = series_b[:n]
    mean_a = sum(a) / n
    mean_b = sum(b) / n
    cov = sum((a[i] - mean_a) * (b[i] - mean_b) for i in range(n)) / n
    std_a = (sum((x - mean_a) ** 2 for x in a) / n) ** 0.5
    std_b = (sum((x - mean_b) ** 2 for x in b) / n) ** 0.5
    if std_a == 0 or std_b == 0:
        return 0.0
    return cov / (std_a * std_b)
