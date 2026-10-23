from typing import Dict, Any

class ManagedMetricsRequest:
    def __init__(self, metric_name: str, start_time: str, end_time: str):
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self) -> Dict[str, Any]:
        return {
            'metric_name': self.metric_name,
            'start_time': self.start_time,
            'end_time': self.end_time
        }

class ManagedMetricsResponse:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ManagedMetricsResponse':
        return ManagedMetricsResponse(data)

    def normalize(self) -> Dict[str, Any]:
        normalized_data = {}
        for key, value in self.data.items():
            normalized_data[key.lower()] = value
        return normalized_data
