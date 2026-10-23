import dataclasses
from typing import List, Dict, Any, Optional


@dataclasses.dataclass
class TimeWindow:
    start_time: str
    end_time: str


@dataclasses.dataclass
class Dimension:
    name: str
    value: str


@dataclasses.dataclass
class MetricQuery:
    namespace: str
    metric_name: str
    dimensions: Optional[List[Dimension]] = None
    period: int = 300  # seconds
    stat: str = "Average"


@dataclasses.dataclass
class MetricDataPoint:
    timestamp: str
    value: float
    unit: str


@dataclasses.dataclass
class MetricData:
    label: str
    datapoints: List[MetricDataPoint]


@dataclasses.dataclass
class MetricStatistics:
    label: str
    datapoints: List[
        Dict[str, Any]
    ]  # CloudWatch returns timestamps and values directly
