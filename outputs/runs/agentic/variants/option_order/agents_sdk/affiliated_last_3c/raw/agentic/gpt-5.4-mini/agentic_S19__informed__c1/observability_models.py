from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class MetricWindow:
    metric_name: str
    start_time: datetime
    end_time: datetime
    dimensions: dict[str, str] = field(default_factory=dict)
    namespace: str | None = None
    statistic: str | None = None
    period_seconds: int = 60

    @classmethod
    def recent(cls, metric_name: str, minutes: int = 60, **kwargs: Any) -> "MetricWindow":
        end = datetime.now(timezone.utc)
        start = end - timedelta(minutes=minutes)
        return cls(metric_name=metric_name, start_time=start, end_time=end, **kwargs)


@dataclass(frozen=True)
class MetricSample:
    timestamp: datetime
    value: float
    unit: str | None = None
    dimensions: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class MetricSeries:
    metric_name: str
    samples: tuple[MetricSample, ...]
    source: str = "datadog"


@dataclass(frozen=True)
class MetricAggregate:
    metric_name: str
    statistic: str
    value: float
    sample_count: int
    source: str = "datadog"


@dataclass(frozen=True)
class MetricComparison:
    metric_name: str
    left_label: str
    right_label: str
    left_value: float
    right_value: float
    delta: float
    ratio: float | None
    source: str = "datadog"


@dataclass(frozen=True)
class MetricSummary:
    metric_name: str
    trend: str
    mean: float | None
    min_value: float | None
    max_value: float | None
    anomaly_score: float | None
    source: str = "openai"


@dataclass(frozen=True)
class SafetyCheckResult:
    text: str
    unsafe: bool
    categories: tuple[str, ...] = ()
    provider: str = "azure-ai-content-safety"


@dataclass(frozen=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_locale: str
    target_locale: str
    provider: str = "deepl"


@dataclass(frozen=True)
class ExportResult:
    bucket: str
    key: str
    etag: str | None = None
    provider: str = "s3"


def normalize_dimensions(dimensions: Mapping[str, Any] | None) -> dict[str, str]:
    if not dimensions:
        return {}
    return {str(k): str(v) for k, v in dimensions.items() if v is not None}


def coerce_float(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, bool):
        return float(int(value))
    return float(value)


def parse_iso8601(dt: str | datetime) -> datetime:
    if isinstance(dt, datetime):
        return dt
    cleaned = dt.replace("Z", "+00:00")
    return datetime.fromisoformat(cleaned)


def to_samples(points: Sequence[Mapping[str, Any]], *, unit: str | None = None) -> tuple[MetricSample, ...]:
    items: list[MetricSample] = []
    for point in points:
        items.append(
            MetricSample(
                timestamp=parse_iso8601(point["timestamp"]),
                value=coerce_float(point["value"]),
                unit=point.get("unit", unit),
                dimensions=normalize_dimensions(point.get("dimensions")),
            )
        )
    return tuple(items)
