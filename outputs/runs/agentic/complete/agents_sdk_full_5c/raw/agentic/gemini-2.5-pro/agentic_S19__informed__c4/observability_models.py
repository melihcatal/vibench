from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class TimeSeriesPoint:
    timestamp: str
    value: float

@dataclass
class TimeSeriesData:
    metric_name: str
    resource_labels: Dict[str, str]
    points: List[TimeSeriesPoint]

@dataclass
class MetricStat:
    metric_name: str
    statistic: str
    value: float
    start_time: str
    end_time: str
