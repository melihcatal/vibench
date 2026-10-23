
import datetime
from typing import Dict, Any, List, Optional

class MetricRequest:
    """
    Represents a request for metric data.
    """
    def __init__(self, metric_name: str, start_time: datetime.datetime, end_time: datetime.datetime,
                 dimensions: Optional[Dict[str, str]] = None, resource_labels: Optional[Dict[str, str]] = None):
        self.metric_name = metric_name
        self.start_time = start_time
        self.end_time = end_time
        self.dimensions = dimensions if dimensions is not None else {}
        self.resource_labels = resource_labels if resource_labels is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "dimensions": self.dimensions,
            "resource_labels": self.resource_labels
        }

class MetricResponse:
    """
    Represents a response containing metric data.
    """
    def __init__(self, metric_name: str, data_points: List[Dict[str, Any]],
                 dimensions: Optional[Dict[str, str]] = None, resource_labels: Optional[Dict[str, str]] = None):
        self.metric_name = metric_name
        self.data_points = data_points
        self.dimensions = dimensions if dimensions is not None else {}
        self.resource_labels = resource_labels if resource_labels is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "data_points": self.data_points,
            "dimensions": self.dimensions,
            "resource_labels": self.resource_labels
        }

def normalize_metric_data(response_data: Dict[str, Any]) -> MetricResponse:
    """
    Normalizes raw metric response data into a MetricResponse object.
    """
    metric_name = response_data.get("metric_name", "unknown_metric")
    data_points = response_data.get("data_points", [])
    dimensions = response_data.get("dimensions", {})
    resource_labels = response_data.get("resource_labels", {})
    return MetricResponse(metric_name, data_points, dimensions, resource_labels)

