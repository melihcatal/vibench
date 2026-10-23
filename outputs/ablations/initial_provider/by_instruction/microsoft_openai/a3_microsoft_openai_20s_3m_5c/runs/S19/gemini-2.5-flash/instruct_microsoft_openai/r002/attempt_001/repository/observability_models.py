import dataclasses
from typing import List, Dict, Any

@dataclasses.dataclass
class MetricDatapoint:
    timestamp: str
    value: float

@dataclasses.dataclass
class MetricQueryResult:
    metric_name: str
    start_time: str
    end_time: str
    datapoints: List[MetricDatapoint]
    # In a real scenario, this could also include dimensions, resource_id, etc.

@dataclasses.dataclass
class MetricStatsResult:
    metric_name: str
    start_time: str
    end_time: str
    average: float
    minimum: float
    maximum: float
    count: int
    sum: float

@dataclasses.dataclass
class DimensionFilter:
    name: str
    value: str

@dataclasses.dataclass
class MetricComparisonResult:
    metric_name: str
    start_time: str
    end_time: str
    series_a: List[MetricDatapoint]
    series_b: List[MetricDatapoint]
    comparison_summary: str # e.g., "Series A is consistently higher than Series B"
