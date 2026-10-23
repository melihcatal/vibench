from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class MetricQueryRequest:
    metric_name: str
    start_time: str
    end_time: str
    interval: str = "PT5M"  # PT5M for 5 minutes
    dimensions: Dict[str, str] = None

@dataclass
class MetricDatapoint:
    timestamp: str
    value: float
    dimensions: Dict[str, str] = None

@dataclass
class MetricQueryResult:
    metric_name: str
    datapoints: List[MetricDatapoint]
