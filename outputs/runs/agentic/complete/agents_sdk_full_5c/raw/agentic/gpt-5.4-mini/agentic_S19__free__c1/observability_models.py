from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Mapping, Optional


@dataclass
class MetricWindowRequest:
    metric_type: str
    minutes: int
    resource_labels: Dict[str, str] = field(default_factory=dict)
    alignment_period_seconds: int = 60


@dataclass
class AggregatedMetricStatsRequest:
    metric_type: str
    minutes: int
    reduction: str = "mean"
    resource_labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricSeriesComparisonRequest:
    metric_type: str
    minutes: int
    left_labels: Dict[str, str] = field(default_factory=dict)
    right_labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricAnnotationRequest:
    text: str
    locale: str = "en"


@dataclass
class MetricSummaryResult:
    metric_type: str
    points: List[float]
    start_time: datetime
    end_time: datetime
    summary: Dict[str, Any]


@dataclass
class NormalizedSeries:
    metric_type: str
    values: List[float]
    timestamps: List[datetime]


def normalize_time_series(response: Any) -> NormalizedSeries:
    values: List[float] = []
    timestamps: List[datetime] = []
    metric_type = getattr(response, "metric_type", "unknown")
    for ts in getattr(response, "time_series", []):
        metric_type = getattr(getattr(ts, "metric", None), "type", metric_type)
        for point in getattr(ts, "points", []):
            value = getattr(getattr(point, "value", None), "double_value", None)
            if value is None:
                value = getattr(getattr(point, "value", None), "int64_value", 0)
            values.append(float(value))
            end_time = getattr(getattr(point, "interval", None), "end_time", None)
            if end_time is not None:
                timestamps.append(end_time)
    return NormalizedSeries(metric_type=metric_type, values=values, timestamps=timestamps)
