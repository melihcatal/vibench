from dataclasses import dataclass
from typing import List
import datetime

@dataclass
class TimeInterval:
    start_time: datetime.datetime
    end_time: datetime.datetime

@dataclass
class MetricQuery:
    metric_type: str
    filter_str: str = ""
    aggregation: dict = None

@dataclass
class TimeSeriesPoint:
    timestamp: datetime.datetime
    value: float

@dataclass
class MetricResponse:
    points: List[TimeSeriesPoint]