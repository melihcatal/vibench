from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class MetricQueryRequest:
    metric_name: str
    start_time: str
    end_time: str
    interval: str = "PT1M"  # 1 minute interval
    filter: str = ""
    aggregation: str = "Average"

@dataclass
class MetricQueryResponse:
    timeseries: List[Dict[str, Any]]

@dataclass
class MetricStatRequest:
    metric_name: str
    start_time: str
    end_time: str
    interval: str = "PT1M"
    filter: str = ""
    aggregation: str = "Average"

@dataclass
class MetricStatResponse:
    value: float
    unit: str

@dataclass
class MetricDimensionRequest:
    metric_name: str
    start_time: str
    end_time: str
    dimensions: Dict[str, str]

@dataclass
class MetricDimensionResponse:
    timeseries: List[Dict[str, Any]]

@dataclass
class MetricComparisonRequest:
    metric_name: str
    start_time: str
    end_time: str
    filter1: str
    filter2: str

@dataclass
class MetricComparisonResponse:
    comparison_result: Dict[str, Any]
