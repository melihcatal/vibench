from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class MetricDataPoint:
    timestamp: int
    value: float


@dataclass
class MetricSeries:
    metric_name: str
    points: List[MetricDataPoint]
    tags: Optional[List[str]] = None


@dataclass
class MetricStatistics:
    metric_name: str
    statistic: str
    value: float
    tags: Optional[List[str]] = None
