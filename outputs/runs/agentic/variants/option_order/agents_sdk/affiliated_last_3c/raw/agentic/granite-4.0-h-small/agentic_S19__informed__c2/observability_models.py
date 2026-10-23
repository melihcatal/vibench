# [HELPER] observability_models.py

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class MetricQueryRequest:
    namespace: str
    metric_name: str
    start_time: str # e.g. '2025-08-15T00:00:00Z'
    end_time: str
    period: int
    statistics: List[str]

@dataclass
class MetricQueryResponse:
    datapoints: List[Dict]
    label: str = ''

@dataclass
class MetricStatRequest(MetricQueryRequest):
    pass

@dataclass
class MetricStatResponse:
    datapoints: List[Dict]
    label: str = ''

@dataclass
class MetricFilterRequest:
    namespace: str
    metric_name: str
    start_time: str
    end_time: str
    dimensions: List[Dict[str, str]]
    period: int
    statistics: List[str]

@dataclass
class MetricFilterResponse:
    datapoints: List[Dict]

@dataclass
class MetricCompareRequest(MetricFilterRequest):
    pass

@dataclass
class MetricCompareResponse:
    comparisons: List[Dict]
