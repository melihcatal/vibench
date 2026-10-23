from typing import List, Dict, Any
from datetime import datetime

# These models are simplified representations for demonstration purposes.
# In a full-fledged application, these would mirror the actual API response structures
# or be designed for specific application-level data transfer.

class TimeSeriesPoint:
    def __init__(self, timestamp: datetime, value: float):
        self.timestamp = timestamp
        self.value = value

    def to_dict(self):
        return {"timestamp": self.timestamp.isoformat(), "value": self.value}

class MetricTimeSeries:
    def __init__(self, resource_labels: Dict[str, str], points: List[TimeSeriesPoint]):
        self.resource_labels = resource_labels
        self.points = points

    def to_dict(self):
        return {
            "resource_labels": self.resource_labels,
            "points": [p.to_dict() for p in self.points]
        }

class MetricAggregationResult:
    def __init__(self, min_val: float, max_val: float, mean_val: float, sum_val: float):
        self.min_val = min_val
        self.max_val = max_val
        self.mean_val = mean_val
        self.sum_val = sum_val

    def to_dict(self):
        return {
            "min": self.min_val,
            "max": self.max_val,
            "mean": self.mean_val,
            "sum": self.sum_val
        }

