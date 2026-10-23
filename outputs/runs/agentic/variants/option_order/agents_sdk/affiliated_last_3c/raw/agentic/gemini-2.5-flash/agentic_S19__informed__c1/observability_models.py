import datetime
from typing import Dict, Any, List, Optional

# Using simple dictionaries to represent models for this exercise.
# In a real-world scenario, you might use dataclasses or Pydantic models.

class MetricPoint:
    def __init__(self, value: Any, timestamp: str, metric_labels: Dict[str, str], resource_labels: Dict[str, str]):
        self.value = value
        self.timestamp = timestamp
        self.metric_labels = metric_labels
        self.resource_labels = resource_labels

    def to_dict(self):
        return {
            "value": self.value,
            "timestamp": self.timestamp,
            "metric_labels": self.metric_labels,
            "resource_labels": self.resource_labels,
        }

class TimeSeriesData:
    def __init__(self, points: List[MetricPoint], metric_type: str, resource_type: str):
        self.points = points
        self.metric_type = metric_type
        self.resource_type = resource_type

    def to_dict(self):
        return {
            "metric_type": self.metric_type,
            "resource_type": self.resource_type,
            "points": [p.to_dict() for p in self.points],
        }

class MetricQueryRequest:
    def __init__(self, project_id: str, metric_type: str, end_time: datetime.datetime, duration_minutes: int, filters: Optional[Dict[str, str]] = None, aggregation: Optional[Dict[str, Any]] = None):
        self.project_id = project_id
        self.metric_type = metric_type
        self.end_time = end_time
        self.duration_minutes = duration_minutes
        self.filters = filters if filters is not None else {}
        self.aggregation = aggregation if aggregation is not None else {}

    def to_dict(self):
        return {
            "project_id": self.project_id,
            "metric_type": self.metric_type,
            "end_time": self.end_time.isoformat(),
            "duration_minutes": self.duration_minutes,
            "filters": self.filters,
            "aggregation": self.aggregation,
        }

# Example usage (for local testing/understanding, not part of the core helper)
if __name__ == "__main__":
    point1 = MetricPoint(10.5, datetime.datetime.utcnow().isoformat(), {"state": "active"}, {"instance": "i-123"})
    point2 = MetricPoint(12.1, (datetime.datetime.utcnow() - datetime.timedelta(minutes=5)).isoformat(), {"state": "active"}, {"instance": "i-123"})
    ts_data = TimeSeriesData([point1, point2], "cpu/utilization", "gce_instance")
    print(ts_data.to_dict())

    req = MetricQueryRequest(
        project_id="my-project",
        metric_type="cpu/usage",
        end_time=datetime.datetime.utcnow(),
        duration_minutes=30,
        filters={
            "resource.labels.zone": "us-central1-a"
        },
        aggregation={
            "aligner": "ALIGN_MEAN"
        }
    )
    print(req.to_dict())
