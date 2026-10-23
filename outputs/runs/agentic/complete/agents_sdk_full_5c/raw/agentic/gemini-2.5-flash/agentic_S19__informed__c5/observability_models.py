from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class TimeSeriesPoint:
    value: float
    timestamp: str  # ISO 8601 format

@dataclass
class TimeSeries:
    metric_type: str
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]
    points: List[TimeSeriesPoint]

@dataclass
class MetricQueryRequest:
    project_id: str
    metric_type: str
    interval_start_time: str
    interval_end_time: str
    filter_string: str = ""
    aggregation_period_seconds: int = 0
    aggregation_reducer: str = "REDUCE_NONE"
    aggregation_cross_series_reducer: str = "REDUCE_NONE"

@dataclass
class MetricQueryResponse:
    time_series: List[TimeSeries]
    next_page_token: str = ""

