from typing import Dict, List, Optional, Any
from datetime import datetime

class MetricQuery:
    metric_name: str
    namespace: str
    dimensions: Optional[Dict[str, str]]
    start_time: datetime
    end_time: datetime
    period: int # in seconds
    statistics: List[str]

    def __init__(self, metric_name: str, namespace: str, start_time: datetime, end_time: datetime, period: int, statistics: List[str], dimensions: Optional[Dict[str, str]] = None):
        self.metric_name = metric_name
        self.namespace = namespace
        self.dimensions = dimensions
        self.start_time = start_time
        self.end_time = end_time
        self.period = period
        self.statistics = statistics

class MetricDatapoint:
    timestamp: datetime
    value: float
    unit: Optional[str]

    def __init__(self, timestamp: datetime, value: float, unit: Optional[str] = None):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit

class MetricQueryResult:
    metric_name: str
    namespace: str
    datapoints: List[MetricDatapoint]
    dimensions: Optional[Dict[str, str]]

    def __init__(self, metric_name: str, namespace: str, datapoints: List[MetricDatapoint], dimensions: Optional[Dict[str, str]] = None):
        self.metric_name = metric_name
        self.namespace = namespace
        self.datapoints = datapoints
        self.dimensions = dimensions

class MetricStatisticsResult:
    metric_name: str
    namespace: str
    statistics: Dict[str, float]
    dimensions: Optional[Dict[str, str]]

    def __init__(self, metric_name: str, namespace: str, statistics: Dict[str, float], dimensions: Optional[Dict[str, str]] = None):
        self.metric_name = metric_name
        self.namespace = namespace
        self.statistics = statistics
        self.dimensions = dimensions

class MetricCompareResult:
    metric_name: str
    namespace: str
    series_a_datapoints: List[MetricDatapoint]
    series_b_datapoints: List[MetricDatapoint]
    series_a_dimensions: Optional[Dict[str, str]]
    series_b_dimensions: Optional[Dict[str, str]]

    def __init__(self, metric_name: str, namespace: str, series_a_datapoints: List[MetricDatapoint], series_b_datapoints: List[MetricDatapoint], series_a_dimensions: Optional[Dict[str, str]] = None, series_b_dimensions: Optional[Dict[str, str]] = None):
        self.metric_name = metric_name
        self.namespace = namespace
        self.series_a_datapoints = series_a_datapoints
        self.series_b_datapoints = series_b_datapoints
        self.series_a_dimensions = series_a_dimensions
        self.series_b_dimensions = series_b_dimensions
