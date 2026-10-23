from dataclasses import dataclass
from typing import List, Dict, Any, Union

@dataclass
class TimeSeriesPoint:
    timestamp: str
    value: Union[float, int]

@dataclass
class MetricTimeSeries:
    metric_kind: str
    value_type: str
    points: List[TimeSeriesPoint]
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]

@dataclass
class AggregatedValue:
    group_by: Dict[str, str]
    value: Union[float, int]
