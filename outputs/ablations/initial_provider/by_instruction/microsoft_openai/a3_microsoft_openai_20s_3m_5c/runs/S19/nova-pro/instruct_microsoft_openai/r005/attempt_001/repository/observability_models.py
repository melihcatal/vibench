from typing import Any, Dict

class MetricQuery:
    def __init__(self, metric_name: str, aggregation: Dict[str, Any], timespan: str):
        self.metric_name = metric_name
        self.aggregation = aggregation
        self.timespan = timespan

class MetricResponse:
    def __init__(self, name: str, timeseries: Dict[str, Any]):
        self.name = name
        self.timeseries = timeseries