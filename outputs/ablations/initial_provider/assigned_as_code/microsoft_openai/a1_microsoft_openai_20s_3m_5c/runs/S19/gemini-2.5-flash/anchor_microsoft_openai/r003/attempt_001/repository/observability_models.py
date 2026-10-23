from typing import List, Dict, Any, Optional
from datetime import datetime

class MetricPoint:
    def __init__(self, timestamp: float, value: float):
        self.timestamp = timestamp
        self.value = value

class MetricSeries:
    def __init__(self, metadata: Dict[str, str], data: List[MetricPoint]):
        self.metadata = metadata
        self.data = data

class MetricQueryResult:
    def __init__(self, name: str, unit: str, timeseries: List[MetricSeries]):
        self.name = name
        self.unit = unit
        self.timeseries = timeseries

class AggregatedMetricValue:
    def __init__(self, timestamp: float, average: Optional[float] = None,
                 minimum: Optional[float] = None, maximum: Optional[float] = None,
                 total: Optional[float] = None, count: Optional[float] = None):
        self.timestamp = timestamp
        self.average = average
        self.minimum = minimum
        self.maximum = maximum
        self.total = total
        self.count = count

class MetricAggregationResult:
    def __init__(self, name: str, unit: str, values: List[AggregatedMetricValue]):
        self.name = name
        self.unit = unit
        self.values = values
