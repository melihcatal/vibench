from typing import Any, Dict


class MetricRequest:
    def __init__(self, namespace: str, metric_name: str, dimensions: Dict[str, str]):
        self.namespace = namespace
        self.metric_name = metric_name
        self.dimensions = dimensions


class MetricResponse:
    def __init__(self, datapoints: Dict[str, Any]):
        self.datapoints = datapoints
