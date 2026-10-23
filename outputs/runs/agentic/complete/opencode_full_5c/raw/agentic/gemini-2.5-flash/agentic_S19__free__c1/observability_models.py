from typing import List, Dict, Any


class MetricDataPoint:
    def __init__(self, timestamp: str, value: Any):
        self.timestamp = timestamp
        self.value = value

    def to_dict(self):
        return {"timestamp": self.timestamp, "value": self.value}


class MetricSeries:
    def __init__(
        self,
        metric_type: str,
        resource_labels: Dict[str, str],
        points: List[MetricDataPoint],
    ):
        self.metric_type = metric_type
        self.resource_labels = resource_labels
        self.points = points

    def to_dict(self):
        return {
            "metric_type": self.metric_type,
            "resource_labels": self.resource_labels,
            "points": [p.to_dict() for p in self.points],
        }


class MetricQueryResponse:
    def __init__(self, series: List[MetricSeries]):
        self.series = series

    def to_dict(self):
        return {"series": [s.to_dict() for s in self.series]}


class MetricSnapshot:
    def __init__(self, timestamp: str, metrics: List[Dict[str, Any]]):
        self.timestamp = timestamp
        self.metrics = metrics

    def to_dict(self):
        return {"timestamp": self.timestamp, "metrics": self.metrics}
