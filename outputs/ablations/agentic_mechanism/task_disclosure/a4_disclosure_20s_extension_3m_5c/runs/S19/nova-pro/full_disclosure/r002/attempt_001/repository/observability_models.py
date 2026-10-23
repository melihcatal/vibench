from typing import Any, Dict, List


class ManagedMetricsRequest:
    def __init__(self, metric_name: str, time_window: str):
        self.metric_name = metric_name
        self.time_window = time_window

    def to_dict(self) -> Dict[str, Any]:
        return {
            'metric_name': self.metric_name,
            'time_window': self.time_window
        }


class ManagedMetricsResponse:
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ManagedMetricsResponse':
        return cls(data['data'])


def normalize_metric_data(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized_data = []
    for item in data:
        normalized_item = {
            'timestamp': item.get('timestamp', ''),
            'value': item.get('value', 0)
        }
        normalized_data.append(normalized_item)
    return normalized_data