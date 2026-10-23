from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence


@dataclass
class MetricWindowRequest:
    metric_name: str
    start_time: datetime
    end_time: datetime
    period: int = 300
    dimensions: dict[str, str] = field(default_factory=dict)
    statistic: str = "Average"


@dataclass
class MetricSeriesPoint:
    timestamp: datetime
    value: float
    unit: str | None = None
    dimensions: dict[str, str] = field(default_factory=dict)


@dataclass
class MetricStatistics:
    metric_name: str
    start_time: datetime
    end_time: datetime
    minimum: float | None = None
    maximum: float | None = None
    average: float | None = None
    sum: float | None = None
    sample_count: float | None = None
    unit: str | None = None


@dataclass
class MetricComparison:
    metric_name: str
    left_label: str
    right_label: str
    points_left: list[MetricSeriesPoint]
    points_right: list[MetricSeriesPoint]


@dataclass
class MetricSummary:
    metric_name: str
    trend: str
    anomaly_score: float
    latest_value: float | None
    window_start: datetime
    window_end: datetime


@dataclass
class SafetyResult:
    text: str
    is_safe: bool
    reasons: list[str] = field(default_factory=list)


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str


@dataclass
class ExportResult:
    bucket: str
    object_key: str
    etag: str | None = None
    uri: str | None = None


def normalize_datetime(value: datetime | str | int | float) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value, tz=timezone.utc)
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def normalize_dimensions(raw: Mapping[str, Any] | Sequence[tuple[str, Any]] | None) -> dict[str, str]:
    if raw is None:
        return {}
    if isinstance(raw, Mapping):
        return {str(k): str(v) for k, v in raw.items()}
    return {str(k): str(v) for k, v in raw}
