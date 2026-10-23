from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class MetricQuery:
    project_id: str
    metric_type: str
    interval_start_time: str # RFC3339 format
    interval_end_time: str   # RFC3339 format
    filter: Optional[str] = None
    aggregation_period_seconds: Optional[int] = None
    group_by_fields: Optional[List[str]] = None
    reduce_series_to_one: Optional[str] = None # 'REDUCE_NONE', 'REDUCE_MEAN', etc.

@dataclass
class TimeSeriesPoint:
    value: Any # can be double, int64, string, bool
    timestamp: str # RFC3339 format

@dataclass
class TimeSeries:
    metric: Dict[str, str]
    resource: Dict[str, str]
    points: List[TimeSeriesPoint]
    metric_kind: str
    value_type: str

@dataclass
class MetricResponse:
    time_series: List[TimeSeries] = field(default_factory=list)
