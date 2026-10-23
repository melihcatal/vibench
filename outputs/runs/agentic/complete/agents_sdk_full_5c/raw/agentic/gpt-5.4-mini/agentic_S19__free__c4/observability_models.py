from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class MetricWindowRequest:
    metric_type: str
    minutes: int = 60
    filter_expression: Optional[str] = None
    alignment_period_seconds: Optional[int] = None


@dataclass
class MetricSeriesRequest:
    metric_type: str
    start_time: datetime
    end_time: datetime
    filter_expression: Optional[str] = None
    group_by_fields: List[str] = field(default_factory=list)


@dataclass
class MetricPointSummary:
    timestamp: datetime
    value: float
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricAggregation:
    metric_type: str
    count: int
    minimum: float
    maximum: float
    average: float
    sum: float


@dataclass
class NormalizedMetricSeries:
    series_key: str
    points: List[MetricPointSummary]


@dataclass
class SafetyCheckResult:
    content: str
    safe: bool
    reason: str


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class ArchiveResult:
    bucket: str
    object_name: str
    size: int


def ensure_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def normalize_point(point: Any) -> MetricPointSummary:
    timestamp = getattr(point, "interval").end_time or getattr(point, "interval").start_time
    value = 0.0
    if hasattr(point, "value"):
        v = point.value
        for attr in ("double_value", "int64_value", "distribution_value"):
            if hasattr(v, attr):
                candidate = getattr(v, attr)
                if attr == "distribution_value":
                    value = float(getattr(candidate, "count", 0) or 0)
                else:
                    value = float(candidate)
                break
    labels = dict(getattr(point, "resource", {}).labels) if hasattr(point, "resource") else {}
    return MetricPointSummary(timestamp=timestamp, value=value, labels=labels)
