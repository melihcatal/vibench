from typing import Dict, List, Optional, Union
from datetime import datetime


class MetricRequest:
    def __init__(
        self,
        metric_name: str,
        namespace: str,
        start_time: datetime,
        end_time: datetime,
        dimensions: Optional[List[Dict[str, str]]] = None,
    ):
        self.metric_name = metric_name
        self.namespace = namespace
        self.start_time = start_time
        self.end_time = end_time
        self.dimensions = dimensions or []


class MetricDatapoint:
    def __init__(
        self,
        timestamp: datetime,
        average: Optional[float] = None,
        sum: Optional[float] = None,
        minimum: Optional[float] = None,
        maximum: Optional[float] = None,
        sample_count: Optional[float] = None,
    ):
        self.timestamp = timestamp
        self.average = average
        self.sum = sum
        self.minimum = minimum
        self.maximum = maximum
        self.sample_count = sample_count

    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "average": self.average,
            "sum": self.sum,
            "minimum": self.minimum,
            "maximum": self.maximum,
            "sample_count": self.sample_count,
        }


class MetricResponse:
    def __init__(
        self, metric_name: str, namespace: str, datapoints: List[MetricDatapoint]
    ):
        self.metric_name = metric_name
        self.namespace = namespace
        self.datapoints = datapoints

    def to_dict(self) -> Dict:
        return {
            "metric_name": self.metric_name,
            "namespace": self.namespace,
            "datapoints": [dp.to_dict() for dp in self.datapoints],
        }


class MetricComparison:
    def __init__(self, series_a: Dict, series_b: Dict):
        self.series_a = series_a
        self.series_b = series_b

    def to_dict(self) -> Dict:
        return {"series_a": self.series_a, "series_b": self.series_b}
