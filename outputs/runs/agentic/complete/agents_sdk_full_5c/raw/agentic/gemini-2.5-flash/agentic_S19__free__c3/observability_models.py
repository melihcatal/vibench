# This file can be used to define common data models or utility classes
# for consistency across different monitoring interactions.

from typing import Dict, Any, List

class MetricTimeSeries:
    def __init__(self, resource_labels: Dict[str, str], metric_labels: Dict[str, str], points: List[Dict[str, Any]]):
        self.resource_labels = resource_labels
        self.metric_labels = metric_labels
        self.points = points

    def to_dict(self):
        return {
            "resource_labels": self.resource_labels,
            "metric_labels": self.metric_labels,
            "points": self.points
        }

class MetricQueryRequest:
    def __init__(self, project_id: str, metric_type: str, end_time_seconds: int, duration_seconds: int,
                 filter_str: str = None, aggregation: Dict[str, Any] = None):
        self.project_id = project_id
        self.metric_type = metric_type
        self.end_time_seconds = end_time_seconds
        self.duration_seconds = duration_seconds
        self.filter_str = filter_str
        self.aggregation = aggregation
