from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict


@dataclass
class MetricQueryRequest:
    metric_type: str
    start_time: datetime
    end_time: datetime


@dataclass
class MetricDataPoint:
    timestamp: datetime
    value: float
    resource_labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricStats:
    count: int = 0
    sum: float = 0.0
    avg: float = 0.0
    min: float = float('inf')
    max: float = float('-inf')


@dataclass
class MetricComparisonResult:
    series_a_values: List[float] = field(default_factory=list)
    series_b_values: List[float] = field(default_factory=list)
    avg_a: float = 0.0
    avg_b: float = 0.0
    diff: float = 0.0