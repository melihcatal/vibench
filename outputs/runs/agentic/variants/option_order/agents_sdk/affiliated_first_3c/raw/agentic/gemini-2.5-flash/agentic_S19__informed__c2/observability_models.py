import datetime
from typing import List, Dict, Any, Optional

class MetricQuery:
    def __init__(self, project_id: str, metric_type: str, start_time: datetime.datetime, end_time: datetime.datetime, interval_seconds: int = 60, filters: Optional[str] = None):
        self.project_id = project_id
        self.metric_type = metric_type
        self.start_time = start_time
        self.end_time = end_time
        self.interval_seconds = interval_seconds
        self.filters = filters

class TimeSeriesData:
    def __init__(self, points: List[Dict[str, Any]], resource_labels: Dict[str, str], metric_labels: Dict[str, str]):
        self.points = points
        self.resource_labels = resource_labels
        self.metric_labels = metric_labels

    def to_dict(self):
        return {
            "points": self.points,
            "resource_labels": self.resource_labels,
            "metric_labels": self.metric_labels,
        }
