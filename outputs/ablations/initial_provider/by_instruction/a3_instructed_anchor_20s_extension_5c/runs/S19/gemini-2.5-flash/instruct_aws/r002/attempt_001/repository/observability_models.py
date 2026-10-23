from datetime import datetime
from typing import List, Dict, Any

class MetricDatapoint:
    def __init__(self, timestamp: datetime, value: float):
        self.timestamp = timestamp
        self.value = value

    def to_dict(self):
        return {"timestamp": self.timestamp.isoformat(), "value": self.value}

class MetricQuery:
    def __init__(self, metric_name: str, namespace: str, dimensions: Dict[str, str] = None):
        self.metric_name = metric_name
        self.namespace = namespace
        self.dimensions = dimensions if dimensions is not None else {}

    def to_cloudwatch_metric(self):
        metric = {
            'Namespace': self.namespace,
            'MetricName': self.metric_name,
        }
        if self.dimensions:
            metric['Dimensions'] = [{'Name': k, 'Value': v} for k, v in self.dimensions.items()]
        return metric
