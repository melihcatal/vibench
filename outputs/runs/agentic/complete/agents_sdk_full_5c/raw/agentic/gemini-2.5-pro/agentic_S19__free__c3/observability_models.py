from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class MetricDataPoint:
    timestamp: str
    value: float

@dataclass
class TimeSeries:
    metric_name: str
    resource_labels: Dict[str, str]
    points: List[MetricDataPoint]

@dataclass
class AnnotationSafetyRequest:
    text: str
    session_id: str

@dataclass
class AnnotationSafetyResult:
    toxicity_score: float
    is_unsafe: bool
