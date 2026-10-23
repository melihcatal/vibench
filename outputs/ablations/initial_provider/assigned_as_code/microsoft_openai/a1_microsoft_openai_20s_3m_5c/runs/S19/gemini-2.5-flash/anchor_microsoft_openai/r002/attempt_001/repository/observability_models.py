from typing import Dict, Any, List


class MetricPoint:
    def __init__(self, timestamp: float, value: float, dimensions: Dict[str, str] = None):
        self.timestamp = timestamp
        self.value = value
        self.dimensions = dimensions if dimensions is not None else {}

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "value": self.value,
            "dimensions": self.dimensions
        }


class MetricSeries:
    def __init__(self, metric_name: str, points: List[MetricPoint], metadata: Dict[str, str] = None):
        self.metric_name = metric_name
        self.points = points
        self.metadata = metadata if metadata is not None else {}

    def to_dict(self):
        return {
            "metric_name": self.metric_name,
            "points": [p.to_dict() for p in self.points],
            "metadata": self.metadata
        }
