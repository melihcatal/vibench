from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class MetricQuery:
    project_id: str
    metric_type: str
    end_time: str
    start_time: str
    interval_seconds: int = 300  # Default to 5 minutes
    filter: Optional[str] = None
    aggregation_aligner: Optional[str] = None
    aggregation_reducer: Optional[str] = None
    group_by: Optional[List[str]] = None


@dataclass
class TimeSeriesPoint:
    value: Any
    timestamp: str


@dataclass
class TimeSeries:
    metric_labels: Dict[str, str]
    resource_labels: Dict[str, str]
    points: List[TimeSeriesPoint]


@dataclass
class MetricData:
    time_series: List[TimeSeries] = field(default_factory=list)


@dataclass
class MetricAggregation:
    metric_type: str
    aggregation_period: str  # e.g., "60s" for 1 minute
    statistic: str  # e.g., "mean", "max", "min", "sum"
    value: Optional[float] = None
    timestamp: Optional[str] = None
