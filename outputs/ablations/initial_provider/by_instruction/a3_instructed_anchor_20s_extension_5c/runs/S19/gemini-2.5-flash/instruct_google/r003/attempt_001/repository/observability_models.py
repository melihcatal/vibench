from typing import Dict, Any, List

class MetricRequest:
    def __init__(self, project_id: str, metric_type: str, interval_start: str, interval_end: str,
                 filter_str: str = None, aggregations: List[Dict[str, Any]] = None):
        self.project_id = project_id
        self.metric_type = metric_type
        self.interval_start = interval_start
        self.interval_end = interval_end
        self.filter_str = filter_str
        self.aggregations = aggregations

class TimeSeriesPoint:
    def __init__(self, value: Any, timestamp: str):
        self.value = value
        self.timestamp = timestamp

class TimeSeries:
    def __init__(self, metric_labels: Dict[str, str], resource_labels: Dict[str, str], points: List[TimeSeriesPoint]):
        self.metric_labels = metric_labels
        self.resource_labels = resource_labels
        self.points = points

class MetricResponse:
    def __init__(self, time_series: List[TimeSeries]):
        self.time_series = time_series