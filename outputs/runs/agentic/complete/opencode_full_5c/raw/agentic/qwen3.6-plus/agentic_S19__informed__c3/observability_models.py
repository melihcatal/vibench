import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AggregationType(str, Enum):
    AVG = "avg"
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    LAST = "last"
    PERCENTILE_50 = "p50"
    PERCENTILE_95 = "p95"
    PERCENTILE_99 = "p99"


@dataclass
class MetricQueryRequest:
    metric_name: str
    start_timestamp: int
    end_timestamp: int
    aggregation: AggregationType = AggregationType.AVG
    interval_seconds: int = 60
    dimensions: dict[str, str] = field(default_factory=dict)
    host: str = ""
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "start_timestamp": self.start_timestamp,
            "end_timestamp": self.end_timestamp,
            "aggregation": self.aggregation.value,
            "interval_seconds": self.interval_seconds,
            "dimensions": self.dimensions,
            "host": self.host,
            "tags": self.tags,
        }


@dataclass
class MetricDataPoint:
    timestamp: int
    value: float
    tags: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "value": self.value,
            "tags": self.tags,
        }


@dataclass
class MetricTimeSeries:
    metric_name: str
    expression: str
    points: list[MetricDataPoint]
    unit: str = ""
    scope: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "expression": self.expression,
            "points": [p.to_dict() for p in self.points],
            "unit": self.unit,
            "scope": self.scope,
        }


@dataclass
class MetricAggregationResult:
    metric_name: str
    start_timestamp: int
    end_timestamp: int
    aggregation_type: AggregationType
    value: float
    sample_count: int = 0
    min_value: float = 0.0
    max_value: float = 0.0
    avg_value: float = 0.0
    sum_value: float = 0.0
    unit: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "start_timestamp": self.start_timestamp,
            "end_timestamp": self.end_timestamp,
            "aggregation_type": self.aggregation_type.value,
            "value": self.value,
            "sample_count": self.sample_count,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "avg_value": self.avg_value,
            "sum_value": self.sum_value,
            "unit": self.unit,
        }


@dataclass
class MetricDimensionFilter:
    metric_name: str
    start_timestamp: int
    end_timestamp: int
    tag_filters: list[str]
    aggregation: AggregationType = AggregationType.AVG
    interval_seconds: int = 60

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "start_timestamp": self.start_timestamp,
            "end_timestamp": self.end_timestamp,
            "tag_filters": self.tag_filters,
            "aggregation": self.aggregation.value,
            "interval_seconds": self.interval_seconds,
        }


@dataclass
class MetricComparisonResult:
    series_a_name: str
    series_b_name: str
    series_a: MetricTimeSeries
    series_b: MetricTimeSeries
    correlation: float = 0.0
    mean_difference: float = 0.0
    max_difference: float = 0.0
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "series_a_name": self.series_a_name,
            "series_b_name": self.series_b_name,
            "series_a": self.series_a.to_dict(),
            "series_b": self.series_b.to_dict(),
            "correlation": self.correlation,
            "mean_difference": self.mean_difference,
            "max_difference": self.max_difference,
            "summary": self.summary,
        }


@dataclass
class MetricSnapshot:
    snapshot_id: str
    metric_name: str
    start_timestamp: int
    end_timestamp: int
    data: list[MetricDataPoint]
    aggregation_results: list[MetricAggregationResult] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)
    created_at: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "metric_name": self.metric_name,
            "start_timestamp": self.start_timestamp,
            "end_timestamp": self.end_timestamp,
            "data": [p.to_dict() for p in self.data],
            "aggregation_results": [r.to_dict() for r in self.aggregation_results],
            "metadata": self.metadata,
            "created_at": self.created_at,
        }


def normalize_timestamps(start: int, end: int) -> tuple[int, int]:
    if start > end:
        start, end = end, start
    return start, end


def build_datadog_query_expression(
    metric_name: str,
    aggregation: AggregationType,
    tags: list[str] | None = None,
    rollup_seconds: int = 60,
) -> str:
    agg_func = aggregation.value
    tag_clause = ""
    if tags:
        tag_clause = "{" + ",".join(tags) + "}"
    expr = f"{agg_func}:{metric_name}{tag_clause}"
    if rollup_seconds:
        expr += f".rollup({rollup_seconds})"
    return expr


def parse_datadog_series_response(
    response_data: dict[str, Any], metric_name: str
) -> MetricTimeSeries:
    series_list = response_data.get("series", [])
    if not series_list:
        return MetricTimeSeries(metric_name=metric_name, expression="", points=[])
    first_series = series_list[0]
    expression = first_series.get("expression", "")
    unit = first_series.get("unit", "")
    scope = first_series.get("scope", "")
    pointlist = first_series.get("pointlist", [])
    points = []
    for point in pointlist:
        if len(point) >= 2 and point[1] is not None:
            points.append(
                MetricDataPoint(
                    timestamp=int(point[0]),
                    value=float(point[1]),
                )
            )
    return MetricTimeSeries(
        metric_name=metric_name,
        expression=expression,
        points=points,
        unit=unit,
        scope=scope,
    )
