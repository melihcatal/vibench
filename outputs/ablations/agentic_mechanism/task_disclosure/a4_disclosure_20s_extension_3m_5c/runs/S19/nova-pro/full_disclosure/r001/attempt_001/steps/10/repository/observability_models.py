from typing import Any, Dict, List


class MetricRequest:
    def __init__(self, namespace: str, metric_name: str, dimensions: Dict[str, str], start_time: str, end_time: str, period: int, statistics: List[str]):
        self.namespace = namespace
        self.metric_name = metric_name
        self.dimensions = dimensions
        self.start_time = start_time
        self.end_time = end_time
        self.period = period
        self.statistics = statistics

    def to_dict(self) -> Dict[str, Any]:
        return {
            'Namespace': self.namespace,
            'MetricName': self.metric_name,
            'Dimensions': [{'Name': k, 'Value': v} for k, v in self.dimensions.items()],
            'StartTime': self.start_time,
            'EndTime': self.end_time,
            'Period': self.period,
            'Statistics': self.statistics
        }


class MetricResponse:
    def __init__(self, label: str, timestamp: str, value: float):
        self.label = label
        self.timestamp = timestamp
        self.value = value

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'MetricResponse':
        return MetricResponse(
            label=data.get('Label', ''),
            timestamp=data.get('Timestamp', ''),
            value=data.get('Value', 0.0)
        )


def normalize_metric_data(data: List[Dict[str, Any]]) -> List[MetricResponse]:
    return [MetricResponse.from_dict(item) for item in data]