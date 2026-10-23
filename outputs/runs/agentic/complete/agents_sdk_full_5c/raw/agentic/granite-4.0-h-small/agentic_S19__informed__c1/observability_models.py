# HELPER: observability_models.py
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class MetricQueryRequest:
    metric: str
    window: Any = None  # for simple start/end queries
    filter: List[Dict[str, Any]] = None
    limit: int = 100
    start: str = None
    end: str = None

class AggregationType:
    AVG = "avg"
    MAX = "max"
    MIN = "min"
    SUM = "sum"

@dataclass
class MetricStatsRequest:
    metric: str
    start: str
    end: str
    granularity: str = "1m"
    aggregations: List[str] = None

@dataclass
class FilteredMetricQuery:
    metric: str
    filter: List[Dict[str, Any]]
    start: str
    end: str
