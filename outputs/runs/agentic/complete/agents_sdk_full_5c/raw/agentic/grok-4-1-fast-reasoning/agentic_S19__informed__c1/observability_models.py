from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any

@dataclass
class MetricDatapoint:
    timestamp: datetime
    value: float
    unit: str = ""

@dataclass
class MetricDimension:
    name: str
    value: str

@dataclass
class MetricQuery:
    namespace: str
    metric_name: str
    dimensions: List[MetricDimension] = None
