from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def to_rfc3339(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_rfc3339(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


@dataclass
class MetricWindowRequest:
    project_id: str
    metric_type: str
    minutes: int
    resource_type: Optional[str] = None
    alignment_period_seconds: int = 60
    per_series_aligner: str = "ALIGN_MEAN"
    cross_series_reducer: Optional[str] = None
    group_by_fields: List[str] = field(default_factory=list)
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class MetricPoint:
    metric_type: str
    resource_type: str
    resource_labels: Dict[str, str]
    metric_labels: Dict[str, str]
    interval_start: Optional[str]
    interval_end: str
    value: float
    value_type: str


@dataclass
class MetricWindowResponse:
    series: List[MetricPoint]
    next_page_token: Optional[str] = None


@dataclass
class AggregatedMetricStats:
    metric_type: str
    start_time: str
    end_time: str
    point_count: int
    minimum: Optional[float]
    maximum: Optional[float]
    average: Optional[float]
    total: Optional[float]


@dataclass
class CompareMetricSeriesRequest:
    base_request: MetricWindowRequest
    left_labels: Dict[str, str]
    right_labels: Dict[str, str]


@dataclass
class ComparedMetricSeries:
    left_label_filter: Dict[str, str]
    right_label_filter: Dict[str, str]
    left_points: List[MetricPoint]
    right_points: List[MetricPoint]
    left_average: Optional[float]
    right_average: Optional[float]
    average_delta: Optional[float]


@dataclass
class MetricSummary:
    summary_text: str
    detected_anomalies: List[str]
    provider_model: str


@dataclass
class AnnotationSafetyResult:
    is_safe: bool
    flagged_categories: Dict[str, float]
    provider: str


@dataclass
class TranslationResult:
    translated_text: str
    target_language: str
    provider: str


@dataclass
class ArchiveResult:
    bucket: str
    object_name: str
    uri: str
    metadata: Dict[str, Any]


def point_to_dict(point: MetricPoint) -> Dict[str, Any]:
    return {
        "metric_type": point.metric_type,
        "resource_type": point.resource_type,
        "resource_labels": point.resource_labels,
        "metric_labels": point.metric_labels,
        "interval_start": point.interval_start,
        "interval_end": point.interval_end,
        "value": point.value,
        "value_type": point.value_type,
    }


def values_from_points(points: List[MetricPoint]) -> List[float]:
    return [point.value for point in points]
