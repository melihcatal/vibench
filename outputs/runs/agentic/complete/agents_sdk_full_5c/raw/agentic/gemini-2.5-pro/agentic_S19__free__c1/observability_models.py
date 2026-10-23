
from dataclasses import dataclass, field
from typing import Any, Dict, List, Union


@dataclass
class TimeSeriesPoint:
    """Represents a single data point in a time series."""
    timestamp: str
    value: Union[float, int, bool, str]


@dataclass
class MetricSeries:
    """
    Represents a time series for a specific metric and resource.
    """
    name: str
    labels: Dict[str, Any] = field(default_factory=dict)
    resource_labels: Dict[str, Any] = field(default_factory=dict)
    points: List[TimeSeriesPoint] = field(default_factory=list)

