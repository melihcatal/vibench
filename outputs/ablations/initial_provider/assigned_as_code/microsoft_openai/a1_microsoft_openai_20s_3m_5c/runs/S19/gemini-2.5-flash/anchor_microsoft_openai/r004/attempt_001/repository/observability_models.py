from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class MetricPoint:
    timestamp: float
    value: float

@dataclass
class MetricSeries:
    name: str
    points: List[MetricPoint]
    dimensions: Dict[str, str] = field(default_factory=dict)

@dataclass
class MetricQueryResult:
    metric_name: str
    timeseries: List[MetricSeries]

@dataclass
class MetricStats:
    min: Optional[float]
    max: Optional[float]
    avg: Optional[float]
    sum: Optional[float]
    count: Optional[int]
