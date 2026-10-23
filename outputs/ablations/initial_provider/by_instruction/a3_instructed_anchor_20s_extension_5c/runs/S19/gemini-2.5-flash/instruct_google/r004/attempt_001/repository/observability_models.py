from datetime import datetime
from typing import List, Dict, Any

class MetricPoint:
    def __init__(self, value: float, timestamp: datetime):
        self.value = value
        self.timestamp = timestamp

    def to_dict(self):
        return {"value": self.value, "timestamp": self.timestamp.isoformat()}

class TimeSeries:
    def __init__(self, metric_type: str, resource_labels: Dict[str, str], points: List[MetricPoint]):
        self.metric_type = metric_type
        self.resource_labels = resource_labels
        self.points = points

    def to_dict(self):
        return {
            "metric_type": self.metric_type,
            "resource_labels": self.resource_labels,
            "points": [point.to_dict() for point in self.points]
        }

def normalize_time_series_response(response) -> List[TimeSeries]:
    """Normalizes Google Cloud Monitoring ListTimeSeriesResponse to a list of TimeSeries objects."""
    normalized_data = []
    for ts_data in response:
        metric_type = ts_data.metric.type
        resource_labels = dict(ts_data.resource.labels)
        points = []
        for point in ts_data.points:
            # Google Cloud Monitoring timestamps are protobuf Timestamp objects
            # Convert to datetime object for easier handling
            timestamp_dt = datetime.fromtimestamp(point.interval.end_time.timestamp())
            value = point.value.double_value # Assuming double_value for simplicity
            points.append(MetricPoint(value, timestamp_dt))
        normalized_data.append(TimeSeries(metric_type, resource_labels, points))
    return normalized_data
