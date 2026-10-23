from typing import Dict, Any


class MetricRequest:
    def __init__(self, namespace: str, metric_name: str, dimensions: Dict[str, str], start_time: str, end_time: str, period: int, statistics: list):
        self.namespace = namespace
        self.metric_name = metric_name
        self.dimensions = dimensions
        self.start_time = start_time
        self.end_time = end_time
        self.period = period
        self.statistics = statistics


class MetricResponse:
    def __init__(self, label: str, timestamp: str, value: float):
        self.label = label
        self.timestamp = timestamp
        self.value = value


def normalize_metric_data(data: Dict[str, Any]) -> Dict[str, Any]:
    normalized_data = {
        'label': data.get('label', ''),
        'timestamp': data.get('timestamp', ''),
        'value': data.get('value', 0.0)
    }
    return normalized_data
