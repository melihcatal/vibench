from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

@dataclass
class TimeSeriesDataPoint:
    timestamp: str  # RFC3339 format
    value: float

@dataclass
class TimeSeries:
    metric: Dict[str, str]
    resource: Dict[str, str]
    points: List[TimeSeriesDataPoint]

@dataclass
class MetricQueryRequest:
    metric_type: str
    project_id: str
    interval_start_time: str # RFC3339 format
    interval_end_time: str   # RFC3339 format
    filter_string: Optional[str] = None
    aggregation_period_seconds: Optional[int] = None
    group_by_fields: Optional[List[str]] = None
    view: Optional[int] = monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL

@dataclass
class MetricQueryResponse:
    time_series: List[TimeSeries]

@dataclass
class MetricExportSnapshot:
    metric_name: str
    timestamp: str
    data: Dict[str, Any]
