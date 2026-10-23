from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List

@dataclass
class MetricQuery:
    namespace: str
    metric_name: str
    dimensions: Dict[str, str]
    start_time: datetime
    end_time: datetime
    period: int # in seconds

@dataclass
class MetricDataPoint:
    timestamp: datetime
    value: float
    unit: str

@dataclass
class MetricQueryResult:
    metric_name: str
    datapoints: List[MetricDataPoint]
