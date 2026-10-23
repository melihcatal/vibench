# observability_models.py
from typing import NamedTuple, List, Dict, Any

# Generic request/response wrappers that can be subclassed for each provider.

class MetricQueryRequest(NamedTuple):
    metric: str
    start: str  # ISO8601 timestamp
    end: str    # ISO8601 timestamp
    tags: List[str] = None

class MetricQueryResponse(NamedTuple):
    series: List[Dict[str, Any]]
    metadata: Dict[str, Any] = None

class MetricStatsRequest(NamedTuple):
    namespace: str
    metric_name: str
    dimensions: Dict[str, str]
    start: str
    end: str
    period: int
    statistics: List[str]

class MetricStatsResponse(NamedTuple):
    datapoints: List[Dict[str, Any]]
    metadata: Dict[str, Any] = None

class FilterMetricRequest(NamedTuple):
    metric_type: str
    filter_expr: str
    start_time: str
    end_time: str
    page_size: int = 100

class FilterMetricResponse(NamedTuple):
    time_series: List[Dict[str, Any]]
    next_page_token: str = None

class CompareMetricRequest(NamedTuple):
    resource_a: str
    resource_b: str
    metric: str
    start: str
    end: str
    tags_a: List[str] = None
    tags_b: List[str] = None

class CompareMetricResponse(NamedTuple):
    series_a: Dict[str, Any]
    series_b: Dict[str, Any]
    delta: Dict[str, Any]  # simple numeric delta or percentage
    metadata: Dict[str, Any] = None
