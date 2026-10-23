from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime


@dataclass
class MetricPoint:
    value: float
    timestamp: datetime
    labels: Dict[str, str]


@dataclass
class MetricSeries:
    metric_type: str
    points: List[MetricPoint]


@dataclass
class MetricStats:
    count: int
    mean: float
    min: float
    max: float
    sum: float


@dataclass
class MetricComparison:
    series_a: MetricSeries
    series_b: MetricSeries
    diff_stats: MetricStats


def normalize_labels(labels: Dict[str, str]) -> Dict[str, str]:
    return {k.replace("-", "_"): v for k, v in labels.items()}
