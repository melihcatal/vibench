from datetime import datetime
from typing import List, Dict, Any, Optional

class MetricDataPoint:
    def __init__(self, timestamp: datetime, value: float, unit: Optional[str] = None):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "value": self.value,
            "unit": self.unit
        }

class MetricQuery:
    def __init__(self, namespace: str, metric_name: str, dimensions: Optional[Dict[str, str]] = None):
        self.namespace = namespace
        self.metric_name = metric_name
        self.dimensions = dimensions if dimensions is not None else {}

    def to_aws_dimensions(self) -> List[Dict[str, str]]:
        return [{"Name": k, "Value": v} for k, v in self.dimensions.items()]

class MetricDataResponse:
    def __init__(self, metric_query: MetricQuery, datapoints: List[MetricDataPoint], unit: Optional[str] = None):
        self.metric_query = metric_query
        self.datapoints = datapoints
        self.unit = unit

    def to_dict(self):
        return {
            "metric_query": {
                "namespace": self.metric_query.namespace,
                "metric_name": self.metric_query.metric_name,
                "dimensions": self.metric_query.dimensions
            },
            "datapoints": [dp.to_dict() for dp in self.datapoints],
            "unit": self.unit
        }