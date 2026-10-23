
from datetime import datetime
from typing import Dict, Any, List, Optional

class MetricRequest:
    """
    Defines the structure for a metric monitoring request.
    """
    def __init__(self, metric_name: str, start_time: datetime, end_time: datetime,
                 dimensions: Optional[Dict[str, str]] = None,
                 resource_labels: Optional[Dict[str, str]] = None):
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

class MetricPoint:
    """
    Represents a single data point for a metric.
    """
    def __init__(self, timestamp: datetime, value: float, unit: Optional[str] = None):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "unit": self.unit
        }

class MetricResponse:
    """
    Defines the structure for a metric monitoring response.
    """
    def __init__(self, metric_name: str, data_points: List[MetricPoint],
                 dimensions: Optional[Dict[str, str]] = None,
                 resource_labels: Optional[Dict[str, str]] = None,
                 query_time: Optional[datetime] = None):
        self.metric_name = metric_name
        self.data_points = data_points
        self.dimensions = dimensions if dimensions is not None else {}
        self.resource_labels = resource_labels if resource_labels is not None else {}
        self.query_time = query_time if query_time is not None else datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "data_points": [dp.to_dict() for dp in self.data_points],
            "dimensions": self.dimensions,
            "resource_labels": self.resource_labels,
            "query_time": self.query_time.isoformat()
        }

def normalize_metric_data(raw_data: List[Dict[str, Any]]) -> List[MetricPoint]:
    """
    Normalizes raw metric data from a monitoring service into a list of MetricPoint objects.
    Assumes raw_data is a list of dictionaries, where each dictionary has at least
    'timestamp' (ISO format string) and 'value' (numeric).
    """
    normalized_points = []
    for item in raw_data:
        try:
            timestamp = datetime.fromisoformat(item["timestamp"])
            value = float(item["value"])
            unit = item.get("unit")
            normalized_points.append(MetricPoint(timestamp=timestamp, value=value, unit=unit))
        except (ValueError, KeyError) as e:
            # In a real-world scenario, you might log this error or handle it more gracefully
            print(f"Error normalizing metric data point: {item}. Error: {e}")
            continue
    return normalized_points
