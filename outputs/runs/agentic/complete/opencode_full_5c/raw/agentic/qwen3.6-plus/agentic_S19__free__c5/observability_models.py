from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class MetricQueryRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    aggregation: str = "avg"
    interval: int = 60
    dimensions: Optional[Dict[str, str]] = None
    resource_ids: Optional[List[str]] = None


@dataclass
class MetricDataPoint:
    timestamp: datetime
    value: float
    dimensions: Optional[Dict[str, str]] = None
    resource_id: Optional[str] = None


@dataclass
class MetricAggregation:
    metric_name: str
    start_time: datetime
    end_time: datetime
    aggregation_type: str
    value: float
    sample_count: int
    min_value: float
    max_value: float
    sum_value: float
    avg_value: float
    p50_value: Optional[float] = None
    p90_value: Optional[float] = None
    p99_value: Optional[float] = None


@dataclass
class MetricSeries:
    metric_name: str
    dimensions: Dict[str, str]
    resource_id: Optional[str] = None
    data_points: List[MetricDataPoint] = field(default_factory=list)


@dataclass
class MetricFilter:
    metric_name: str
    start_time: datetime
    end_time: datetime
    dimension_filters: Dict[str, List[str]]
    aggregation: str = "avg"
    interval: int = 60


@dataclass
class MetricComparisonResult:
    series_a: MetricSeries
    series_b: MetricSeries
    delta_values: List[float]
    delta_percentages: List[float]
    correlation: float
    start_time: datetime
    end_time: datetime


@dataclass
class MetricSummary:
    metric_name: str
    period_start: datetime
    period_end: datetime
    current_value: float
    previous_value: float
    trend_direction: str
    anomaly_detected: bool
    anomaly_score: float
    summary_text: str
    data_points_analyzed: int


@dataclass
class MetricAnnotation:
    text: str
    metric_name: Optional[str] = None
    resource_id: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class AnnotationSafetyResult:
    annotation: MetricAnnotation
    is_safe: bool
    safety_score: float
    categories: Dict[str, float]
    flagged_terms: List[str]


@dataclass
class DashboardNote:
    note_text: str
    dashboard_id: Optional[str] = None
    source_locale: str = "en"
    target_locale: str = "es"


@dataclass
class TranslationResult:
    original_note: DashboardNote
    translated_text: str
    source_locale: str
    target_locale: str
    confidence: float


@dataclass
class MetricExportArchive:
    metric_name: str
    start_time: datetime
    end_time: datetime
    data_points: List[MetricDataPoint]
    archive_key: Optional[str] = None
    archive_url: Optional[str] = None
    archived_at: Optional[datetime] = None
    checksum: Optional[str] = None


def normalize_timestamp(ts) -> datetime:
    if isinstance(ts, (int, float)):
        return datetime.utcfromtimestamp(ts)
    if isinstance(ts, str):
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        return datetime.fromisoformat(ts)
    return ts


def normalize_datadog_response(raw_response: Dict[str, Any]) -> List[MetricDataPoint]:
    points = []
    series_list = raw_response.get("series", [])
    for series in series_list:
        metric_name = series.get("metric", "")
        dimensions = series.get("scope", {})
        for raw_point in series.get("pointlist", []):
            ts_raw, value = raw_point[0], raw_point[1]
            if value is not None:
                points.append(
                    MetricDataPoint(
                        timestamp=normalize_timestamp(ts_raw / 1000.0),
                        value=float(value),
                        dimensions=dimensions,
                    )
                )
    return points


def normalize_aggregation_response(raw_response: Dict[str, Any]) -> MetricAggregation:
    agg = raw_response.get("group", {}).get("calc", {})
    return MetricAggregation(
        metric_name=raw_response.get("metric", ""),
        start_time=normalize_timestamp(raw_response.get("from", 0)),
        end_time=normalize_timestamp(raw_response.get("to", 0)),
        aggregation_type=raw_response.get("aggr", "avg"),
        value=agg.get("avg", 0.0),
        sample_count=agg.get("count", 0),
        min_value=agg.get("min", 0.0),
        max_value=agg.get("max", 0.0),
        sum_value=agg.get("sum", 0.0),
        avg_value=agg.get("avg", 0.0),
        p50_value=agg.get("p50"),
        p90_value=agg.get("p90"),
        p99_value=agg.get("p99"),
    )


def build_datadog_query_payload(request: MetricQueryRequest) -> Dict[str, Any]:
    query = f"{request.aggregation}:{request.metric_name}"
    if request.dimensions:
        dim_parts = []
        for k, v in request.dimensions.items():
            dim_parts.append(f"{k}:{v}")
        query = f"{query}{{{' AND '.join(dim_parts)}}}"
    return {
        "query": query,
        "from": int(request.start_time.timestamp()),
        "to": int(request.end_time.timestamp()),
    }


def build_datadog_aggregation_payload(request: MetricQueryRequest) -> Dict[str, Any]:
    query = f"{request.aggregation}:{request.metric_name}"
    if request.dimensions:
        dim_parts = []
        for k, v in request.dimensions.items():
            dim_parts.append(f"{k}:{v}")
        query = f"{query}{{{' AND '.join(dim_parts)}}}"
    return {
        "metric": request.metric_name,
        "aggr": request.aggregation,
        "query": query,
        "from": int(request.start_time.timestamp()),
        "to": int(request.end_time.timestamp()),
    }


def build_datadog_filter_payload(request: MetricFilter) -> Dict[str, Any]:
    query_parts = [request.metric_name]
    filter_clauses = []
    for dim_key, dim_values in request.dimension_filters.items():
        if len(dim_values) == 1:
            filter_clauses.append(f"{dim_key}:{dim_values[0]}")
        else:
            filter_clauses.append(f"{dim_key}:{{{','.join(dim_values)}}}")
    if filter_clauses:
        query_parts.append("{" + " AND ".join(filter_clauses) + "}")
    query_str = f"{request.aggregation}:{' '.join(query_parts)}"
    return {
        "query": query_str,
        "from": int(request.start_time.timestamp()),
        "to": int(request.end_time.timestamp()),
    }
