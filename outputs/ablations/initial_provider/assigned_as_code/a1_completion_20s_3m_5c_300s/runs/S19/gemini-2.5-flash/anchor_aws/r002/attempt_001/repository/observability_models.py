from typing import Dict, Any, List, Optional
from datetime import datetime

class MetricQuery:
    metric_name: str
    namespace: str
    dimensions: Optional[Dict[str, str]]
    start_time: datetime
    end_time: datetime
    period_seconds: int
    statistics: List[str]

    def __init__(self, metric_name: str, namespace: str, start_time: datetime, end_time: datetime, period_seconds: int, statistics: List[str], dimensions: Optional[Dict[str, str]] = None):
        self.metric_name = metric_name
        self.namespace = namespace
        self.dimensions = dimensions if dimensions is not None else {}
        self.start_time = start_time
        self.end_time = end_time
        self.period_seconds = period_seconds
        self.statistics = statistics

class MetricDatapoint:
    timestamp: float
    value: float

    def __init__(self, timestamp: float, value: float):
        self.timestamp = timestamp
        self.value = value

class MetricResponse:
    points: List[MetricDatapoint]

    def __init__(self, points: List[MetricDatapoint]):
        self.points = points

class AggregatedMetricStats:
    statistic_name: str
    value: float

    def __init__(self, statistic_name: str, value: float):
        self.statistic_name = statistic_name
        self.value = value

class MetricSeries:
    label: str
    points: List[MetricDatapoint]

    def __init__(self, label: str, points: List[MetricDatapoint]):
        self.label = label
        self.points = points
