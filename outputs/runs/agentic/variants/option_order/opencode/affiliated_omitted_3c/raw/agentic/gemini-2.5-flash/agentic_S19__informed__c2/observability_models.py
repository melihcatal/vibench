import datetime
from typing import Dict, Any, List, Optional, TypedDict


class MetricQuery(TypedDict):
    namespace: str
    metric_name: str
    dimensions: Optional[List[Dict[str, str]]]
    period: int  # in seconds
    start_time: datetime.datetime
    end_time: datetime.datetime
    statistics: List[str]  # e.g., ['Average', 'Sum']


class MetricDataPoint(TypedDict):
    timestamp: datetime.datetime
    value: float
    unit: str


class MetricDataResult(TypedDict):
    label: str
    datapoints: List[MetricDataPoint]


class AggregatedMetricStats(TypedDict):
    timestamp: datetime.datetime
    average: Optional[float]
    sum: Optional[float]
    unit: Optional[str]
