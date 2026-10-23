from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def ensure_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def to_epoch_seconds(dt: datetime) -> int:
    return int(ensure_utc(dt).timestamp())


def isoformat_utc(dt: datetime) -> str:
    return ensure_utc(dt).isoformat().replace("+00:00", "Z")


def normalize_dimensions(dimensions: dict[str, Any] | None) -> dict[str, str]:
    if not dimensions:
        return {}
    normalized: dict[str, str] = {}
    for key, value in dimensions.items():
        if value is None:
            continue
        normalized[str(key)] = str(value)
    return normalized


@dataclass(slots=True)
class MetricWindowRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    namespace: str = "AWS/EC2"
    period: int = 60
    stat: str = "Average"
    dimensions: dict[str, str] = field(default_factory=dict)

    def normalized_dimensions(self) -> dict[str, str]:
        return normalize_dimensions(self.dimensions)


@dataclass(slots=True)
class MetricPoint:
    timestamp: str
    value: float
    unit: str | None = None
    dimensions: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class MetricSeriesResponse:
    metric_name: str
    namespace: str
    stat: str
    start_time: str
    end_time: str
    period: int
    points: list[MetricPoint]


@dataclass(slots=True)
class AggregateMetricStatsResponse:
    metric_name: str
    namespace: str
    start_time: str
    end_time: str
    sample_count: int
    minimum: float | None
    maximum: float | None
    average: float | None
    sum: float | None
    unit: str | None


@dataclass(slots=True)
class MetricComparisonResponse:
    metric_name: str
    namespace: str
    left_label: str
    right_label: str
    start_time: str
    end_time: str
    stat: str
    left_points: list[MetricPoint]
    right_points: list[MetricPoint]
    left_average: float | None
    right_average: float | None
    delta_average: float | None


@dataclass(slots=True)
class MetricSummaryResponse:
    summary: str
    detected_anomaly: bool
    rationale: str


@dataclass(slots=True)
class SafetyCheckResponse:
    is_safe: bool
    flagged_categories: list[str]
    scores: dict[str, float]


@dataclass(slots=True)
class TranslationResponse:
    translated_text: str
    target_locale: str
    detected_source_locale: str | None = None


@dataclass(slots=True)
class ArchiveResponse:
    bucket: str
    object_key: str
    etag: str | None
    version_id: str | None
