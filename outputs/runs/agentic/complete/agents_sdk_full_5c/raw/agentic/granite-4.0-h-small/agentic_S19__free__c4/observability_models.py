# HELPER
from dataclasses import dataclass
from typing import Any, Dict, List

dict_type = Dict[str, Any]

@dataclass
class MetricRequest:
    metric_name: str
    start_time: str  # RFC3339 timestamp
    end_time: str    # RFC3339 timestamp
    limit: int = 100
    dimension_filter: str = ''

@dataclass
class MetricResponse:
    points: List[dict_type] = None  # [{'interval': {...}, 'value': {...}}]

@dataclass
class StatResult:
    count: int
    sum: float
    mean: float
    min: float = None
    max: float = None

@dataclass
class DimensionFilter:
    filter_expr: str

@dataclass
class CompareRequest:
    metric_name: str
    dimension_a: DimensionFilter
    dimension_b: DimensionFilter
    start_time: str
    end_time: str
    limit: int
