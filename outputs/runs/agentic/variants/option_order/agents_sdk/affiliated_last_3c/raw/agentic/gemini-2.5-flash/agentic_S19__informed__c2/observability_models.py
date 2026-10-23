from typing import List, Dict, Any
from datetime import datetime

class MetricDataPoint:
    """Represents a single data point for a metric."""
    def __init__(self, timestamp: datetime, value: float, labels: Dict[str, str] = None):
        self.timestamp = timestamp
        self.value = value
        self.labels = labels if labels is not None else {}

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "labels": self.labels
        }

class MetricSeries:
    """Represents a series of metric data points."""
    def __init__(self, metric_type: str, resource_labels: Dict[str, str], points: List[MetricDataPoint]):
        self.metric_type = metric_type
        self.resource_labels = resource_labels
        self.points = points

    def to_dict(self):
        return {
            "metric_type": self.metric_type,
            "resource_labels": self.resource_labels,
            "points": [p.to_dict() for p in self.points]
        }

class MetricSummary:
    """Represents a summary of metric trends or anomalies."""
    def __init__(self, summary_text: str, detected_anomalies: List[Dict[str, Any]] = None):
        self.summary_text = summary_text
        self.detected_anomalies = detected_anomalies if detected_anomalies is not None else []

    def to_dict(self):
        return {
            "summary_text": self.summary_text,
            "detected_anomalies": self.detected_anomalies
        }
