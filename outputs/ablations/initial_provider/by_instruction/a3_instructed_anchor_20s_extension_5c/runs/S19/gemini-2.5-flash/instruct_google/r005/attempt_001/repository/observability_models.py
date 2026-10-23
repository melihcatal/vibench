import datetime
from typing import Dict, Any, List, Optional

class MetricDataPoint:
    def __init__(self, timestamp: datetime.datetime, value: float, labels: Optional[Dict[str, str]] = None):
        self.timestamp = timestamp
        self.value = value
        self.labels = labels if labels is not None else {}

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "labels": self.labels
        }

class MetricQueryResult:
    def __init__(self, metric_name: str, resource_labels: Dict[str, str], points: List[MetricDataPoint]):
        self.metric_name = metric_name
        self.resource_labels = resource_labels
        self.points = points

    def to_dict(self):
        return {
            "metric_name": self.metric_name,
            "resource_labels": self.resource_labels,
            "points": [p.to_dict() for p in self.points]
        }
