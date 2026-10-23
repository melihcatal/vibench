from dataclasses import dataclass
from typing import List, Dict, Any
from datetime import datetime

@dataclass
class MetricDimension:
    Name: str
    Value: str

@dataclass
class MetricQuery:
    metric_name: str
    namespace: str
    start_time: datetime
    end_time: datetime
    period: int
    dimensions: List[MetricDimension]

@dataclass
class MetricDatapoint:
    Timestamp: datetime
    Value: float
    Unit: str

@dataclass
class MetricResult:
    Id: str
    Label: str
    Timestamps: List[datetime]
    Values: List[float]
    StatusCode: str

