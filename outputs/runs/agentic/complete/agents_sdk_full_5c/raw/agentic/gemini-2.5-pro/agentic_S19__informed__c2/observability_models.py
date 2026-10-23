from dataclasses import dataclass, field
from typing import Dict, List, Any
from datetime import datetime

@dataclass
class MetricPoint:
    """Represents a single data point in a time series."""
    timestamp: datetime
    value: float

@dataclass
class TimeSeries:
    """Represents a series of metric data points for a specific resource."""
    metric_name: str
    resource_labels: Dict[str, str]
    points: List[MetricPoint] = field(default_factory=list)

@dataclass
class AggregatedTimeSeries:
    """Represents aggregated statistics for a metric."""
    metric_name: str
    aggregation: str
    value: float
    resource_labels: Dict[str, str] = field(default_factory=dict)
