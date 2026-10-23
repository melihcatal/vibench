from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class MetricQuery:
    namespace: str
    metric_name: str
    start_time: float
    end_time: float
    period_seconds: int = 60
    statistics: List[str] = None
    dimensions: Dict[str, str] = None

    def __post_init__(self):
        if self.statistics is None:
            self.statistics = ["Average"]
        if self.dimensions is None:
            self.dimensions = {}


@dataclass
class MetricDatapoint:
    timestamp: float
    value: float


@dataclass
class MetricStatistics:
    datapoints: List[MetricDatapoint]
    label: str
