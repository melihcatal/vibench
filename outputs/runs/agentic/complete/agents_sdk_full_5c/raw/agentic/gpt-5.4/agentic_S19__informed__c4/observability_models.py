from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional


RFC3339_UTC = "%Y-%m-%dT%H:%M:%SZ"


@dataclass
class MetricWindowRequest:
    project_id: str
    metric_type: str
    minutes: int = 15
    resource_type: Optional[str] = None
    alignment_period_seconds: int = 60
    per_series_aligner: str = "ALIGN_MEAN"
    cross_series_reducer: Optional[str] = None
    group_by_fields: List[str] = field(default_factory=list)
    filter_expression: Optional[str] = None
    view: str = "FULL"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MetricPoint:
    interval_start: Optional[str]
    interval_end: Optional[str]
    value: Optional[float]
    value_type: Optional[str]
    labels: Dict[str, str] = field(default_factory=dict)
    metric_kind: Optional[str] = None
    unit: Optional[str] = None


@dataclass
class MetricSeries:
    metric_type: str
    resource_type: Optional[str]
    metric_labels: Dict[str, str] = field(default_factory=dict)
    resource_labels: Dict[str, str] = field(default_factory=dict)
    points: List[MetricPoint] = field(default_factory=list)


@dataclass
class AggregatedMetricResponse:
    metric_type: str
    series_count: int
    points: List[MetricPoint]


@dataclass
class MetricComparisonResponse:
    left: MetricSeries
    right: MetricSeries
    deltas: List[Dict[str, Any]]


@dataclass
class SummaryResult:
    summary_text: str
    detected_trend: str
    anomaly_flag: bool
    supporting_points: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SafetyResult:
    is_safe: bool
    scores: Dict[str, float]
    flagged_categories: List[str]
    provider: str = "Perspective API"


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str]
    target_language: str
    provider: str = "DeepL"


@dataclass
class ArchiveResult:
    bucket: str
    object_name: str
    generation: Optional[str]
    uri: str
    provider: str = "Google Cloud Storage"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def to_rfc3339(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime(RFC3339_UTC)


def extract_numeric_value(point_value: Any) -> tuple[Optional[float], Optional[str]]:
    for key in ("double_value", "int64_value", "distribution_value", "bool_value"):
        if hasattr(point_value, key):
            raw = getattr(point_value, key)
            if raw is None:
                continue
            if key == "distribution_value":
                count = getattr(raw, "count", None)
                mean = getattr(raw, "mean", None)
                return float(mean if mean is not None else count) if (mean is not None or count is not None) else None, key
            if key == "bool_value":
                return float(raw), key
            return float(raw), key
    return None, None


def normalize_time_series(series: Any) -> MetricSeries:
    metric = getattr(series, "metric", None)
    resource = getattr(series, "resource", None)
    value_type = getattr(series, "value_type", None)
    metric_kind = getattr(series, "metric_kind", None)
    unit = getattr(series, "unit", None)

    normalized_points: List[MetricPoint] = []
    for point in list(getattr(series, "points", []) or []):
        interval = getattr(point, "interval", None)
        point_value = getattr(point, "value", None)
        numeric, detected_type = extract_numeric_value(point_value)
        normalized_points.append(
            MetricPoint(
                interval_start=to_rfc3339(getattr(interval, "start_time", utc_now())) if interval and getattr(interval, "start_time", None) else None,
                interval_end=to_rfc3339(getattr(interval, "end_time", utc_now())) if interval and getattr(interval, "end_time", None) else None,
                value=numeric,
                value_type=detected_type or (str(value_type) if value_type is not None else None),
                labels=dict(getattr(metric, "labels", {}) or {}) | dict(getattr(resource, "labels", {}) or {}),
                metric_kind=str(metric_kind) if metric_kind is not None else None,
                unit=unit,
            )
        )

    return MetricSeries(
        metric_type=getattr(metric, "type", ""),
        resource_type=getattr(resource, "type", None),
        metric_labels=dict(getattr(metric, "labels", {}) or {}),
        resource_labels=dict(getattr(resource, "labels", {}) or {}),
        points=normalized_points,
    )


def series_to_dict(series: MetricSeries) -> Dict[str, Any]:
    return asdict(series)
