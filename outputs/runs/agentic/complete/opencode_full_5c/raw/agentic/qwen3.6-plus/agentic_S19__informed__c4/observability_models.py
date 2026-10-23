import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class AggregationFunction(str, Enum):
    AVG = "avg"
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    MEDIAN = "median"
    P95 = "p95"
    P99 = "p99"


class MetricType(str, Enum):
    GAUGE = "gauge"
    RATE = "rate"
    COUNTER = "counter"


@dataclass
class MetricQuery:
    metric_name: str
    start_ts: int
    end_ts: int
    aggregation: AggregationFunction = AggregationFunction.AVG
    interval: int = 60
    dimensions: dict[str, str] = field(default_factory=dict)
    metric_type: Optional[MetricType] = None


@dataclass
class DimensionFilter:
    dimension_key: str
    dimension_value: str
    operator: str = "eq"


@dataclass
class MetricComparison:
    metric_name: str
    start_ts: int
    end_ts: int
    series_a: dict[str, str]
    series_b: dict[str, str]
    aggregation: AggregationFunction = AggregationFunction.AVG
    interval: int = 60


@dataclass
class Datapoint:
    timestamp: int
    value: float
    dimensions: dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeries:
    metric_name: str
    datapoints: list[Datapoint]
    aggregation: str
    interval: int
    start_ts: int
    end_ts: int


@dataclass
class AggregatedStats:
    metric_name: str
    avg: float
    sum_value: float
    min_value: float
    max_value: float
    count: int
    p95: Optional[float] = None
    p99: Optional[float] = None
    start_ts: int
    end_ts: int


@dataclass
class MetricWindowResponse:
    series: list[MetricSeries]
    query: MetricQuery
    status: str = "ok"
    error_message: Optional[str] = None


@dataclass
class MetricAggregationResponse:
    stats: AggregatedStats
    query: MetricQuery
    status: str = "ok"
    error_message: Optional[str] = None


@dataclass
class MetricComparisonResponse:
    series_a: MetricSeries
    series_b: MetricSeries
    comparison: MetricComparison
    delta_avg: float
    delta_pct: float
    status: str = "ok"
    error_message: Optional[str] = None


@dataclass
class MetricSummaryRequest:
    metric_name: str
    trend_data: list[Datapoint]
    anomalies: list[dict[str, Any]] = field(default_factory=list)
    time_window_hours: int = 24


@dataclass
class MetricSummaryResponse:
    summary_text: str
    anomaly_descriptions: list[str]
    trend_direction: str
    status: str = "ok"


@dataclass
class AnnotationSafetyRequest:
    text: str
    categories: list[str] = field(
        default_factory=lambda: ["TOXICITY", "SEVERE_TOXICITY", "THREAT", "INSULT"]
    )


@dataclass
class AnnotationSafetyResponse:
    text: str
    scores: dict[str, float]
    is_safe: bool
    flagged_categories: list[str]
    status: str = "ok"


@dataclass
class DashboardNoteTranslateRequest:
    note_text: str
    source_locale: str = "en"
    target_locale: str = "es"


@dataclass
class DashboardNoteTranslateResponse:
    original_text: str
    translated_text: str
    source_locale: str
    target_locale: str
    status: str = "ok"


@dataclass
class MetricsExportRequest:
    metric_name: str
    snapshot_data: list[Datapoint]
    export_timestamp: int
    bucket_name: str
    object_key_prefix: str = "metrics/snapshots"


@dataclass
class MetricsExportResponse:
    bucket_name: str
    object_key: str
    export_timestamp: int
    size_bytes: int
    status: str = "ok"


def normalize_query_params(
    metric_name: str, start_ts: int, end_ts: int, interval: int = 60
) -> dict:
    return {
        "metric": metric_name,
        "from": start_ts,
        "to": end_ts,
        "interval": interval,
    }


def normalize_dimensions(dimensions: dict[str, str]) -> list[str]:
    return [f"{key}:{value}" for key, value in sorted(dimensions.items())]


def normalize_aggregation(func: AggregationFunction) -> str:
    return func.value


def build_datapoint_list(raw_points: list[dict]) -> list[Datapoint]:
    return [
        Datapoint(
            timestamp=int(p.get("timestamp", 0)),
            value=float(p.get("value", 0.0)),
            dimensions=p.get("tags", {}),
        )
        for p in raw_points
    ]


def build_metric_series(
    metric_name: str,
    raw_series: dict,
    aggregation: str,
    interval: int,
    start_ts: int,
    end_ts: int,
) -> MetricSeries:
    datapoints = build_datapoint_list(raw_series.get("pointlist", []))
    return MetricSeries(
        metric_name=metric_name,
        datapoints=datapoints,
        aggregation=aggregation,
        interval=interval,
        start_ts=start_ts,
        end_ts=end_ts,
    )
