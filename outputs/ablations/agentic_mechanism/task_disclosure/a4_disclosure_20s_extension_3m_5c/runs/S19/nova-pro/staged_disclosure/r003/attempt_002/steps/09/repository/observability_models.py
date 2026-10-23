from typing import Any, Dict


class ManagedMetricsRequest:
    def __init__(self, metric_name: str, metric_value: float, timestamp: int):
        self.metric_name = metric_name
        self.metric_value = metric_value
        self.timestamp = timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'timestamp': self.timestamp,
        }


class ManagedMetricsResponse:
    def __init__(self, status: str, message: str):
        self.status = status
        self.message = message

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data['status'], data['message'])


def normalize_metric_name(metric_name: str) -> str:
    return metric_name.lower().replace(' ', '_')


def normalize_metric_value(metric_value: float) -> float:
    return round(metric_value, 2)
