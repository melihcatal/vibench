import datetime
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from google.cloud import monitoring_v3

@dataclass
class MetricDatapoint:
    timestamp: float
    value: float | int | bool

@dataclass
class MetricSeries:
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]
    datapoints: List[MetricDatapoint]

@dataclass
class MetricQuery:
    project_id: str
    metric_type: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    interval_seconds: int = 60
    filter_string: Optional[str] = None # For Cloud Monitoring MQL-like filters
    agg_aligner: Optional[monitoring_v3.Aggregation.Aligner] = None
    agg_reducer: Optional[monitoring_v3.Aggregation.Reducer] = None
    agg_period_seconds: Optional[int] = None
    group_by_fields: List[str] = field(default_factory=list)
