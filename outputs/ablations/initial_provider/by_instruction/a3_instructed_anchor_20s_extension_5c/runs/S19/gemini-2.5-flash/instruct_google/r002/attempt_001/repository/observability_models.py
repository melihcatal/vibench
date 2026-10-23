from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List, Optional

@dataclass
class MetricQueryRequest:
    project_id: str
    metric_type: str
    end_time: datetime
    start_time: datetime
    interval_minutes: int = 5
    filter: Optional[str] = None
    group_by: Optional[List[str]] = None
    aligner: Optional[str] = None
    reducer: Optional[str] = None

@dataclass
class TimeSeriesPoint:
    timestamp: datetime
    value: float

@dataclass
class TimeSeries:
    metric_labels: Dict[str, str]
    resource_labels: Dict[str, str]
    points: List[TimeSeriesPoint]

@dataclass
class MetricQueryResponse:
    time_series: List[TimeSeries]

@dataclass
class MetricStatsResponse:
    metric_type: str
    start_time: datetime
    end_time: datetime
    average: Optional[float] = None
    min: Optional[float] = None
    max: Optional[float] = None
    sum: Optional[float] = None
    count: Optional[int] = None

@dataclass
class MetricComparisonResponse:
    metric_type: str
    start_time: datetime
    end_time: datetime
    series_a: TimeSeries
    series_b: TimeSeries
    difference: Optional[float] = None
    percentage_difference: Optional[float] = None
